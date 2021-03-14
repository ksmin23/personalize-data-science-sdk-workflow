import os
import json
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    describe_solution_version_response = personalize.describe_solution_version(
        solutionVersionArn = event['solution_version_arn']
    )
    status = describe_solution_version_response["solutionVersion"]["status"]
    print("SolutionVersion Status: {}".format(status))

    return {
        'status': status,
        'solution_version_arn': event['solution_version_arn'] 
    }
