import json
import requests

def lambda_handler(event, context):
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    folder_name = object_key.split('/')[0]
    
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{folder_name}"
    
    # actrecog train url
    api_url = ''
    
    data = {
        's3_url': s3_url
    }
    
    response = requests.post(api_url, json=data)
    
    if response.status_code == 200:
        return {
            'statusCode': 200,
            'body': json.dumps('Successfully sent folder name to API')
        }
    else:
        return {
            'statusCode': response.status_code,
            'body': json.dumps('Failed to send folder name to API')
        }
