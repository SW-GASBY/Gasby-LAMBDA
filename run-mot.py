import json
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    object_key = event['Records'][0]['s3']['object']['key']
    folder_name = '/'.join(object_key.split('/')[:-1])
    
    logger.info(folder_name)
    api_url = ''

    
    payload = {
        'payload': folder_name
    }
    
    headers = {
        'Content-Type': 'application/json'
    }
    api_response = requests.post(api_url, json=payload)
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed the file and sent API request!')
    }