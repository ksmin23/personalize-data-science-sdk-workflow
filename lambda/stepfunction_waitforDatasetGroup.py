import json
import base64
import boto3

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):
    datasetGroupArnVal = event['input']
    describe_dataset_group_response = personalize.describe_dataset_group(
        datasetGroupArn = datasetGroupArnVal
    )

    return_status = False
    status = describe_dataset_group_response["datasetGroup"]["status"]
    print("DatasetGroup: {}".format(status))

    return {
        'status': status,
        'DatasetGroup': status,
        'datasetGroupArn': datasetGroupArnVal,
        'schemaArn': event['schemaArn']
    }
