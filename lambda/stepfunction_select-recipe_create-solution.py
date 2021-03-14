import json
import boto3
import base64

personalize = boto3.client('personalize')
personalize_runtime = boto3.client('personalize-runtime')

def lambda_handler(event, context):

    list_recipes_response = personalize.list_recipes()
    recipe_arn = "arn:aws:personalize:::recipe/aws-user-personalization" # aws-hrnn selected for demo purposes

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
