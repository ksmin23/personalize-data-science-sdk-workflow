import os
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize_runtime = boto3.client('personalize-runtime', region_name=AWS_REGION_NAME)

def lambda_handler(event, context):
    userId = str(event['user_id'])
    itemId = str(event['item_id'])
    campaignArn = event['campaign_arn']

    print("userId={}, itemId={}, campaignArn={}".format(userId, itemId, campaignArn))

    get_recommendations_response = personalize_runtime.get_recommendations(
        campaignArn=campaignArn,
        userId=userId,
        itemId=itemId
    )

    item_list = get_recommendations_response['itemList']
    return {
        'item_list': item_list
    }
