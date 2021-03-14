import os
import json
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    get_solution_metrics_response = personalize.get_solution_metrics(
        solutionVersionArn = event['solution_version_arn']
    )

    create_campaign_response = personalize.create_campaign(
        name = "stepfunction-campaign",
        solutionVersionArn = event['solution_version_arn'],
        minProvisionedTPS = 1
    )

    campaign_arn = create_campaign_response['campaignArn']
    print(json.dumps(create_campaign_response, indent=2))

    return {
        'campaign_arn': campaign_arn,
        'solution_version_arn': event['solution_version_arn']
    }
