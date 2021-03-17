import os
import json
import base64
import random

import boto3

AWS_REGION_NAME = os.getenv('AWS_REGION_NAME', 'us-east-1')
personalize = boto3.client('personalize', region_name=AWS_REGION_NAME)


def get_suffix():
  ret = 0
  for _ in range(5):
    s = str(random.random())
    if len(s) >= 7:
      ret = s[2:7]
      break
  else:
    ret = s.replace('.', str(random.randint(1, 9)))
  return ret


def lambda_handler(event, context):
    datasetArn = event['datasetArn']
    bucket = event['bucket_name']
    filename = event['file_name']
    role_arn = event['role_arn']

    job_name_suffix = get_suffix()
    create_dataset_import_job_response = personalize.create_dataset_import_job(
        jobName = "dataset-import-job-{}".format(job_name_suffix),
        datasetArn = datasetArn,
        dataSource = {
            "dataLocation": "s3://{}/{}".format(bucket, filename)
        },
        roleArn = role_arn
    )

    dataset_import_job_arn = create_dataset_import_job_response['datasetImportJobArn']
    print(json.dumps(create_dataset_import_job_response, indent=2))

    return {
        'statusCode': 200,
        'datasetImportJobArn': dataset_import_job_arn,
        'datasetGroupArn': event['datasetGroupArn']
    }