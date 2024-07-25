import json
import requests

def lambda_handler(event, context):
    object_key = event['Records'][0]['s3']['object']['key']
    folder_name = '/'.join(object_key.split('/')[:-1])
    
    api_url = ''
    
    payload = {
        'uuid': folder_name
    }

    api_response = requests.post(api_url, json=payload)

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed the file and sent API request!')
    }