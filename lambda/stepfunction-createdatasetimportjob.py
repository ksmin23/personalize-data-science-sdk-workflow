import os
import json
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    datasetArn = event['dataset_arn']
    bucket = event['bucket_name']
    filename = event['file_name']
    role_arn = event['role_arn']

    create_dataset_import_job_response = personalize.create_dataset_import_job(
        jobName = "stepfunction-dataset-import-job",
        datasetArn = datasetArn,
        dataSource = {
            "dataLocation": "s3://{}/{}".format(bucket, filename)
        },
        roleArn = role_arn
    )

    dataset_import_job_arn = create_dataset_import_job_response['datasetImportJobArn']
    print(json.dumps(create_dataset_import_job_response, indent=2))

    return {
        'statusCode': 200,
        'dataset_import_job_arn': dataset_import_job_arn,
        'datasetGroupArn': event['datasetGroupArn']
    }
