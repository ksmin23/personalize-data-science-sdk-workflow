import os
import json
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    try:
        create_dataset_group_response = personalize.create_dataset_group(
            name = event['input']
        )

        dataset_group_arn = create_dataset_group_response['datasetGroupArn']
        print(json.dumps(create_dataset_group_response, indent=2))
    except personalize.exceptions.ResourceAlreadyExistsException as ex:
        traceback.print_exc()
        dataset_group_list = personalize.list_dataset_groups()
        dataset_group = [e for e in dataset_group_list['datasetGroups'] if e['name'] == event['input']][0]
        dataset_group_arn = dataset_group['datasetGroupArn']

    return {
        'statusCode': 200,
        'datasetGroupArn':dataset_group_arn,
        'schemaArn': event['schemaArn']
    }
