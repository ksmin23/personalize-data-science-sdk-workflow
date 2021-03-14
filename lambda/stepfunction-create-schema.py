import os
import json
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    schema = {
        "type": "record",
        "name": "Interactions",
        "namespace": "com.amazonaws.personalize.schema",
        "fields": [
            {
                "name": "USER_ID",
                "type": "string"
            },
            {
                "name": "ITEM_ID",
                "type": "string"
            },
            {
                "name": "TIMESTAMP",
                "type": "long"
            }
        ],
        "version": "1.0"
    }

    create_schema_response = personalize.create_schema(
        name = event['input'],
        schema = json.dumps(schema)
    )

    schema_arn = create_schema_response['schemaArn']
    print(json.dumps(create_schema_response, indent=2))

    return {
        'statusCode': 200,
        'schemaArn':schema_arn,
        'output': schema_arn
    }