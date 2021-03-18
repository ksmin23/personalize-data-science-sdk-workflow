import os
import json
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    create_solution_version_response = personalize.create_solution_version(
        solutionArn = event['solution_arn']
    )

    solution_version_arn = create_solution_version_response['solutionVersionArn']
    print(json.dumps(create_solution_version_response, indent=2))

    return {
        'statusCode': 200,
        'solutionVersionArn': solution_version_arn
    }
