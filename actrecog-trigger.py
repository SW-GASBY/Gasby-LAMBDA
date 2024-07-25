import json
import requests
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    bucket_name = 'gasby-actrecog'
    object_key = event['Records'][0]['s3']['object']['key']
    
    file_url = f'https://{bucket_name}.s3.amazonaws.com/{object_key}'
    
    # actrecog predict url
    api_url = ''
    
    payload = {
        'file_url': file_url
    }

    api_response = requests.post(api_url, json=payload)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed the file and sent API request!')
    }
