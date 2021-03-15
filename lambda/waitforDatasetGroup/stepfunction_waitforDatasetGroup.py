import os
import json
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)

def lambda_handler(event, context):
    datasetGroupArnVal = event['input']
    describe_dataset_group_response = personalize.describe_dataset_group(
        datasetGroupArn = datasetGroupArnVal
    )

    status = describe_dataset_group_response["datasetGroup"]["status"]
    print("DatasetGroup Status: {}".format(status))

    return {
        'status': status,
        'DatasetGroup': status,
        'datasetGroupArn': datasetGroupArnVal,
        'schemaArn': event['schemaArn']
    }
