import os
import json
import base64
import traceback

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    get_solution_metrics_response = personalize.get_solution_metrics(
        solutionVersionArn = event['solutionVersionArn']
    )

    try:
        create_campaign_response = personalize.create_campaign(
            name = event['campaign_name'],
            solutionVersionArn = event['solutionVersionArn'],
            minProvisionedTPS = 1
        )

        campaign_arn = create_campaign_response['campaignArn']
        print(json.dumps(create_campaign_response, indent=2))
    except personalize.exceptions.ResourceAlreadyExistsException as ex:
        traceback.print_exc()

        campaign_list = personalize.list_campaigns(
            solutionArn=event['solutionVersionArn']
        )
        campaign_response = [e for e in campaign_list['campaigns'] if e['name'] == event['campaign_name']][0]
        update_campaign_response = personalize.update_campaign(
            campaignArn=campaign_response['campaignArn'],
            solutionVersionArn=event['solutionVersionArn']
        )
        campaign_arn = update_campaign_response['campaignArn']

    return {
        'campaignArn': campaign_arn,
        'solutionVersionArn': event['solutionVersionArn']
    }
