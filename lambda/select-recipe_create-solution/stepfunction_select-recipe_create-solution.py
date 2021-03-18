import os
import json
import base64
import traceback

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def lambda_handler(event, context):
    list_recipes_response = personalize.list_recipes()
    recipe = [e for e in list_recipes_response['recipes'] if e['name'] == event['recipe']]
    recipe_arn = recipe[0]['recipeArn']

    try:
        create_solution_response = personalize.create_solution(
            name = event['solution_name'],
            datasetGroupArn = event['datasetGroupArn'],
            recipeArn = recipe_arn
        )

        solution_arn = create_solution_response['solutionArn']
        print(json.dumps(create_solution_response, indent=2))
    except personalize.exceptions.ResourceAlreadyExistsException as ex:
        traceback.print_exc()
        solution_list = personalize.list_solutions(datasetGroupArn=event['datasetGroupArn'])
        personalize_solution = [e for e in solution_list['solutions'] if e['name'] == event['solution_name']][0]
        solution_arn = personalize_solution['solutionArn']

    return {
        'statusCode': 200,
        'solutionArn': solution_arn
    }
