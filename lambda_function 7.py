import json
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    object_key = event['Records'][0]['s3']['object']['key']
    folder_name = '/'.join(object_key.split('/')[:-1])
    
    logger.info(folder_name)
    # api_url = 'http://210.102.178.186:8080/yolo-predict/upload'
    api_url = 'http://1.238.80.90:4003/yolo-predict/upload'

    
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