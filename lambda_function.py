import json
import requests

def lambda_handler(event, context):
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    folder_name = object_key.split('/')[0]
    
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{folder_name}"
    
    # API 엔드포인트 URL
    api_url = 'actrecog학습 엔드포인트'
    
    # API 요청 데이터
    data = {
        's3_url': s3_url
    }
    
    # API 호출
    response = requests.post(api_url, json=data)
    
    # 응답 처리
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
