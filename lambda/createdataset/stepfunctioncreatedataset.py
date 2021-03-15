import os
import json
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    dataset_type = "INTERACTIONS"
    datasetGroupArn = event['datasetGroupArn']
    create_dataset_response = personalize.create_dataset(
        name = event['name'],
        datasetType = dataset_type,
        datasetGroupArn = datasetGroupArn,
        schemaArn = event['schemaArn']
    )

    dataset_arn = create_dataset_response['datasetArn']
    print(json.dumps(create_dataset_response, indent=2))

    return {
        'statusCode': 200,
        'dataset_arn': dataset_arn,
        'datasetGroupArn': datasetGroupArn 
    }
