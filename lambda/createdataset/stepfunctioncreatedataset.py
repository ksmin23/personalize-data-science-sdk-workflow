import os
import json
import base64
import traceback

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    try:
        dataset_type = event['datasetType']
        datasetGroupArn = event['datasetGroupArn']
        create_dataset_response = personalize.create_dataset(
            name = event['name'],
            datasetType = dataset_type,
            datasetGroupArn = datasetGroupArn,
            schemaArn = event['schemaArn']
        )
        dataset_arn = create_dataset_response['datasetArn']
        print(json.dumps(create_dataset_response, indent=2))
    except personalize.exceptions.ResourceAlreadyExistsException as ex:
        traceback.print_exc()
        datasets_list = personalize.list_datasets()
        dataset = [e for e in datasets_list['datasets'] if e['name'] == event['name'] and e['datasetType'] == dataset_type][0]
        dataset_arn = dataset['datasetArn']

    return {
        'statusCode': 200,
        'datasetArn': dataset_arn,
        'datasetGroupArn': datasetGroupArn 
    }
