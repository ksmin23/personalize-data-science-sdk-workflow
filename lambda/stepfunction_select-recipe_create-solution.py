import os
import json
import base64

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)

def lambda_handler(event, context):
    list_recipes_response = personalize.list_recipes()
    recipe = [e for e in list_recipes_response if e['name'] == event['recipe']]
    recipe_arn = recipe[0]['recipeArn']

    create_solution_response = personalize.create_solution(
        name = "stepfunction-solution",
        datasetGroupArn = event['dataset_group_arn'],
        recipeArn = recipe_arn
    )

    solution_arn = create_solution_response['solutionArn']
    print(json.dumps(create_solution_response, indent=2))

    return {
        'statusCode': 200,
        'solution_arn': solution_arn
    }
