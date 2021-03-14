import os
import json
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    describe_dataset_import_job_response = personalize.describe_dataset_import_job(
        datasetImportJobArn = event['dataset_import_job_arn']
    )
    status = describe_dataset_import_job_response["datasetImportJob"]['status']
    print("DatasetImportJob Status: {}".format(status))

    return {
        'status': status,
        'dataset_import_job_arn': event['dataset_import_job_arn'],
        'datasetGroupArn': event['datasetGroupArn']
    }
