#!/usr/bin/env python3
# vim: tabstop=2 shiftwidth=2 softtabstop=2 expandtab

import os
from datetime import datetime

from aws_cdk import (
  core,
  aws_ec2,
  aws_iam,
  aws_lambda as _lambda,
  aws_logs,
  aws_sagemaker
)

class PersonalizeDSWorkflowStack(core.Stack):

  def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # The code that defines your stack goes here
    vpc_name = self.node.try_get_context("vpc_name")
    vpc = aws_ec2.Vpc.from_lookup(self, "ExistingVPC",
      is_default=True,
      vpc_name=vpc_name)

    sagemaker_notebook_role_policy_doc = aws_iam.PolicyDocument()
    sagemaker_notebook_role_policy_doc.add_statements(aws_iam.PolicyStatement(**{
      "effect": aws_iam.Effect.ALLOW,
      "resources": ["arn:aws:s3:::*"],
      "actions": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ]
    }))

    sagemaker_notebook_role = aws_iam.Role(self, 'SageMakerExecRoleForPersonalize',
      role_name='AmazonSageMakerExecutionRoleForPersonalize',
      assumed_by=aws_iam.ServicePrincipal('sagemaker.amazonaws.com'),
      inline_policies={
        'AmazonSageMaker-ExecutionPolicy': sagemaker_notebook_role_policy_doc
      }
    )

    aws_managed_policy_list = ['IAMFullAccess', 'AmazonS3FullAccess', 'service-role/AmazonPersonalizeFullAccess', 'AWSStepFunctionsFullAccess', 'AmazonSageMakerFullAccess']
    for elem in aws_managed_policy_list:
    	managed_policy = aws_iam.ManagedPolicy.from_aws_managed_policy_name(elem)
    	sagemaker_notebook_role.add_managed_policy(managed_policy)

    sm_nb_lifecycle_content = '''#!/bin/bash
sudo -u ec2-user -i <<'EOF'
echo "export AWS_REGION={AWS_Region}" >> ~/.bashrc
source /home/ec2-user/anaconda3/bin/activate python3
pip install --upgrade stepfunctions
source /home/ec2-user/anaconda3/bin/deactivate
cd /home/ec2-user/SageMaker
wget -N https://raw.githubusercontent.com/ksmin23/personalize-data-science-sdk-workflow/master/Personalize-Stepfunction-Workflow.ipynb
EOF
'''.format(AWS_Region=core.Aws.REGION)

    sm_nb_lifecycle_config_prop = aws_sagemaker.CfnNotebookInstanceLifecycleConfig.NotebookInstanceLifecycleHookProperty(
      content=core.Fn.base64(sm_nb_lifecycle_content)
    )

    sm_nb_lifecycle_config = aws_sagemaker.CfnNotebookInstanceLifecycleConfig(self, 'PersonalizeDataScienceSDKWorkflow',
      notebook_instance_lifecycle_config_name='PersonalizeDataScienceSDKWorkflow',
      on_start=[sm_nb_lifecycle_config_prop]
    )

    sm_nb_instance = aws_sagemaker.CfnNotebookInstance(self, 'PersonalizeWorkflowNB',
      instance_type='ml.t3.xlarge',
      role_arn=sagemaker_notebook_role.role_arn,
      lifecycle_config_name=sm_nb_lifecycle_config.notebook_instance_lifecycle_config_name,
      notebook_instance_name='personalize-data-science-sdk-workflow',
      root_access='Disabled'
    )

    lambda_fn_list = [(root, files[0][:-3]) for root, dirs, files in os.walk('../lambda/') if files]
    for fn_path, fn_name in lambda_fn_list:
      lambda_fn = _lambda.Function(self, '{}'.format(fn_name.title()),
        runtime=_lambda.Runtime.PYTHON_3_8,
        function_name='{}'.format(fn_name),
        handler='{}.lambda_handler'.format(fn_name),
        code=_lambda.Code.asset(fn_path),
        environment={'AWS_REGION_NAME': core.Aws.REGION},
        timeout=core.Duration.minutes(15)
      )

      personalize_full_access_policy = aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AmazonPersonalizeFullAccess')
      lambda_fn.role.add_managed_policy(personalize_full_access_policy)

      log_group = aws_logs.LogGroup(self, '{}LogGroup'.format(fn_name.title()),
        log_group_name='/aws/lambda/{}'.format(fn_name.title()),
        retention=aws_logs.RetentionDays.THREE_DAYS)
      log_group.grant_write(lambda_fn)


app = core.App()
PersonalizeDSWorkflowStack(app, "personalize-ds-wf", env=core.Environment(
  account=os.environ["CDK_DEFAULT_ACCOUNT"],
  region=os.environ["CDK_DEFAULT_REGION"]))

app.synth()
