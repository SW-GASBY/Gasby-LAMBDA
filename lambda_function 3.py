import json
import logging
import os
import requests
from openai import OpenAI
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

AWS_ACCESS_KEY_ID = os.getenv("AWS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SEC")
AWS_DEFAULT_REGION = os.getenv("AWS_REG")

s3_client = boto3.client('s3',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                    region_name=AWS_DEFAULT_REGION
                    )

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    folder_name = object_key.split('/')[0]
    
    duration_bucket = 'gasby-req'
    jsonfile = f'{folder_name}/{folder_name}.json'
    
    response = s3_client.get_object(Bucket=duration_bucket, Key=jsonfile)
    content = response['Body'].read().decode('utf-8')

    json_data = json.loads(content)

    video_duration = json_data.get('video duration')
    language = json_data.get('language')
    fps = json_data.get('fps')
    
    print("duration: ", video_duration)
    
    openai_api_key = os.environ.get('openai_api_key')
    client = OpenAI(api_key=openai_api_key)

    def download_mike_breen_text(url):
        response = requests.get(url)
        response.raise_for_status()
        return response.text

    mike_breen_bucket = 'gasby-actrecog-result'
    mike_breen_text = f'MikeBreen.txt'
    
    txt_response = s3_client.get_object(Bucket=mike_breen_bucket, Key=mike_breen_text)
    txt_content = txt_response['Body'].read().decode('utf-8')

    def download_json_from_s3(bucket_name, object_key):
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        json_data = json.loads(response['Body'].read().decode('utf-8'))
        return json_data
        
    json_data = download_json_from_s3(bucket_name, object_key)
    
    def generate_basketball_commentary(json_data, txt_content, video_duration):
        messages = [
            {'role': 'system', 'content': 'You are a basketball commentator. Your task is to read the data and write a commentary on the basketball game.'},
            {'role': 'system', 'content': 'Generate the commentary based on the following conditions:'},
            {'role': 'system', 'content': '1. Describe the actions of the players.'},
            {'role': 'system', 'content': '2. Mention the player team, and action in each commentary line.'},
            {'role': 'system', 'content': '3. Keep the commentary in chronological order based on the "frame" field.'},
            {'role': 'system', 'content': '4. Each Action label refers to the players\' actions.'},
            {'role': 'system', 'content': '5. Each position label refers to the position of each player.'},
            {'role': 'system', 'content': '6. If a player shoots from the paint, it counts as a 2-point shot, while shots from other positions count as 3-pointers.'},
            {'role': 'system', 'content': '7. The priority of action labels refers to shoot, block, pass, dribble, defense.'},
            {'role': 'system', 'content': '8. Actions not included in the above priority can be skipped in commentary.'},
            {'role': 'system', 'content': '9. Commentary should only include actions that occurred in the JSON data.'},
            {'role': 'system', 'content': '10. Do not mention the number of the player, just mention the team of the player.'},
            {'role': 'system', 'content': '11. Do not include opening or closing scripts.'},
            {'role': 'system', 'content': f'12. Speak in {language}.'},
            {'role': 'user', 'content': f'Generate a short and important basketball commentary script that the narrator can read in {video_duration} seconds based on the following JSON data. Please make it as concise as possible:'},
            {'role': 'user', 'content': json.dumps(json_data)},
            {'role': 'user', 'content': 'Please make it as concise as possible.'},
            {'role': 'user', 'content': 'Follow the commentary style of real NBA commentator Mike Breen with the following text data:'},
            {'role': 'user', 'content': f'Mike Breen Commentary Text: {txt_content}'},
            {'role': 'user', 'content': f'Output the commentary script with timestamps based on a frame rate of {fps} frames per second. Use the format n ~ m seconds: commentary script. Split the commentary into multiple 2-second intervals.'}
        ]
    
        response = client.chat.completions.create(
            model='gpt-4-turbo',
            messages=messages,
            temperature=0.5
        )
    
        return response.choices[0].message['content']

    commentary = generate_basketball_commentary(json_data, txt_content, video_duration)
    
    bucket_name = 'gasby-resp'
    file_name = f'{folder_name}.txt'
    
    s3_client.put_object(Bucket=bucket_name, Key=file_name, Body=commentary)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed the file, generated commentary, and uploaded to S3!')
    }
