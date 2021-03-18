iimport os
import json
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    describe_campaign_response = personalize.describe_campaign(
        campaignArn = event['campaignArn']
    )
    status = describe_campaign_response["campaign"]["status"]
    print("Campaign Status: {}".format(status))

    return {
        'status': status,
        'campaignArn': event['campaignArn']
    }
