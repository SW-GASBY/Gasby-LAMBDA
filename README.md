<div align="center">

# BING: AWS LAMBDA

*BING 서비스 아키텍쳐에 사용된 LAMBDA 코드 입니다.*

[![Static Badge](https://img.shields.io/badge/language-english-red)](./README.md) [![Static Badge](https://img.shields.io/badge/language-korean-blue)](./README-KR.md) [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FSinging-voice-conversion%2Fsingtome-model&count_bg=%23E3E30F&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

</div>

<br>

SW중심대학 디지털 경진대회: SW와 생성 AI의 만남 - SW 부문
팀 GASBY의 BING 서비스
이 리포지토리는 팀 GASBY가 SW중심대학 디지털 경진대회에서 개발한 BING 서비스에 사용된 AWS Lambda 함수의 코드를 포함하고 있습니다. 본 프로젝트는 생성 AI 기술을 활용하여 사용자의 요구에 맞는 다양한 소프트웨어 솔루션을 제공합니다.

프로젝트 개요
BING 서비스는 최신 생성 AI 알고리즘을 사용하여 실시간으로 데이터를 처리하고 사용자에게 맞춤형 결과를 제공합니다. 이 프로젝트는 서버리스 아키텍처를 기반으로 하며, AWS Lambda를 핵심 컴퓨팅 리소스로 사용합니다.

주요 기능
실시간 데이터 처리: 사용자의 요청을 실시간으로 처리하여 빠르고 정확한 결과를 제공합니다.
생성 AI 통합: 최신 AI 모델을 활용하여 사용자 요구에 맞춤형 결과 생성.
서버리스 아키텍처: AWS Lambda를 사용하여 확장성과 비용 효율성을 극대화.

<br>

<div align="center">

<h3> Model part Team members </h3>

| Profile | Name | Role |
| :---: | :---: | :---: |
| <a href="https://github.com/anselmo228"><img src="https://avatars.githubusercontent.com/u/24919880?v=4" height="120px"></a> | Heechan Chung <br> **anselmo**| Create a Docker Image for Inferring UVR Models <br> Manage AWS S3 buckets, Lambda, and API gateways <br> Managing singtome project model experiments|
| <a href="https://github.com/jmin314"><img src="https://avatars.githubusercontent.com/u/30928301?v=4(https://avatars.githubusercontent.com/u/30928301?v=4)" height="120px"></a>| MinSeung Jang <br> **JANG**| Model Pipeline and Architecture Design <br> Creating a Docker Image for RVC Model training and inference<br> Managing and Operating AWS SageMaker |

<br>


</div>

<br>

## 1. LAMBDA 소개

저희는 총 7개의 Lambda 함수를 사용합니다. 각 Lambda 함수는 특정 상황에 따라 동작하며, 각각의 트리거에 따라 작동하여 자동으로 파이프라인이 실행되도록 설계되었습니다. 이로 인해 데이터 처리 및 결과 생성 과정이 원활하고 효율적으로 이루어집니다.
## upload-gasby-request
- **Role**: 유저의 영상 업로드 및 요청
- **Endpoint**: https://nj7ceu0i9c.execute-api.ap-northeast2.amazonaws.com/deploy/request

- **Method**: Post
- Request Example:
    
    ```python
    import requests
    import base64
    
    url = 'https://nj7ceu0i9c.execute-api.ap-northeast-2.amazonaws.com/deploy/request'
    
    # user 요청받아서 만들기
    file_path = '/Users/jungheechan/Desktop/kakao.mp4'
    userId = '1'
    
    # 파일을 base64로 인코딩
    with open(file_path, 'rb') as f:
        file_content = f.read()
        file_content_base64 = base64.b64encode(file_content).decode('utf-8')
    
    # HTTP POST 요청 보내기
    payload = {
        'file': file_content_base64,
        'userId': userId  
    }
    
    response = requests.post(url, json=payload)
    
    # 응답 확인
    print(response.status_code)
    print(response.json())
    ```
    
- **Trigger: API Gateway**

## **run-mot**
- **Role**: 유저의 요청에 따른 MOT predict 실행
- **Endpoint**: Trigger로 작동

- **Trigger: S3- [gasby-req](https://ap-northeast-2.console.aws.amazon.com/s3/buckets/gasby-req?region=ap-northeast-2)**
- Response:
    
    ```python
    {
    'payload': userId
    }
    ```
    

## run-actrecog
- **Role**: 유저의 요청에 따른 action recognition predict 실행
- **Endpoint**: Trigger로 작동

- **Trigger: S3- [gasby-mot-result](https://ap-northeast-2.console.aws.amazon.com/s3/buckets/gasby-mot-result?region=ap-northeast-2)**
- Response:
    
    ```python
    {
    'payload': userId
    }
    ```
    

## mot-trigger
- **Role**: 새로운 pt 파일 생성시 MOT train 실행
- **Endpoint**: Trigger로 작동

- **Trigger: S3- [gasby-mot](https://ap-northeast-2.console.aws.amazon.com/s3/buckets/gasby-mot?region=ap-northeast-2)**
- Response:
    
    ```python
     payload = {
            'file_url': file_url
        }
    ```
    

## actrecog-trigger
- **Role**: 새로운 pt 파일 생성시 action recognition train 실행
- **Endpoint**: Trigger로 작동

- **Trigger: S3 -  [gasby-actrecog](https://ap-northeast-2.console.aws.amazon.com/s3/buckets/gasby-actrecog?region=ap-northeast-2)**
- Response:
    
    ```python
     payload = {
            'file_url': file_url
        }
    ```
    

### GPT
- **Role**: 최종 Action Recog 결과물(action.json)으로 해설 생성
- **Endpoint**: Trigger로 작동

- **Trigger: S3 -** [gasby-actrecog-result](https://ap-northeast-2.console.aws.amazon.com/s3/buckets/gasby-actrecog-result?region=ap-northeast-2)


## 2. Architecture

This project was designed with a real-service environment in mind and selected AWS (Amazon Web Services) to handle all training and inference tasks in the cloud. Utilizing AWS's robust cloud infrastructure, the following services were employed for model training and inference:

1. **Amazon SageMaker**: Used for model training, SageMaker is a fully managed service that allows for the easy and quick construction, training, and deployment of machine learning models.
2. **AWS Lambda**: Employed as a trigger for training and inference tasks, Lambda is an event-driven computing service that runs code without managing servers.

<br>

The cloud-based workflow of this project generally involves the following steps:

1. **Receiving User Requests**: Receives requests for original music conversion from users.
2. **Activating Lambda Triggers**: An AWS Lambda function is triggered to process the request.
3. **Training and Inference in SageMaker**: The Lambda function calls Amazon SageMaker to carry out model training and inference tasks.
4. **Returning Results**: Delivers the converted music file to the user.

<br>

This architecture is designed to leverage the cloud's flexibility and scalability to the fullest, ensuring a high-quality user experience. Model training and inference proceed automatically based on user requests, with all processes managed through cloud services.

<img src="./img/aws_architecture.png" />

<br>

## 3. How does it work?

The model part of the project leverages a range of services provided by AWS, offering high scalability and flexibility in the cloud environment. Here are the key features and processes:

1. **API Gateway**: All requests are received through AWS's API Gateway, which routes each request to the appropriate resource while providing security, monitoring, and usage management.

2. **Amazon SageMaker**: Upon receiving requests, AWS automatically allocates SageMaker instances to perform model training or inference. SageMaker is a fully managed service that facilitates the easy building, training, and deployment of machine learning models.

3. **S3 Bucket Storage**: Trained model parameters or inference results (audio files) are stored in Amazon S3 buckets. Users can access these buckets to download the necessary data.

4. **Spring Boot Backend**: Backend information management (user information, registration details, etc.) is handled by a Spring Boot-based backend. This allows for stable data management separate from the frontend.

5. **Docker and ECR**: To use custom models in Amazon SageMaker, Docker images are uploaded to Amazon Elastic Container Registry (ECR) and then fetched by SageMaker. This approach enhances model management and simplifies modifications to the model's implementation if the input and output formats remain the same.

This structure enables the creation of high-performance, scalable applications through AWS's robust cloud capabilities. Detailed information on additional dependencies and environment settings is provided in the sections below.

<img src="./img/seq_diagram.png" />

<br>

## 4. Environment

All operations were performed within a Docker environment. Therefore, please refer to each `Dockerfile` for the required requirements and base image information. The local GPU and cloud instance information used for training are as follows.

- LOCAL GPU: NVIDIA RTX 4090 x 2
- CLOUD INSTANCE: AWS g4dn.xlarge


### Sample dockerfile
```Dockerfile
# Set the base image
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Set up working directories
RUN mkdir -p /opt/ml/input/data/training
RUN mkdir -p /opt/ml/model
WORKDIR /opt/ml/code

# Install required packages
RUN apt-get update
RUN apt-get install -y build-essential

COPY . .
RUN pip install -r requirements.txt

# Configuration for running training script in SageMaker
ENV SAGEMAKER_PROGRAM rvc_train.py
ENV SAGEMAKER_SUBMIT_DIRECTORY /opt/ml/code
ENV SM_MODEL_DIR /opt/ml/model
ENV SM_CHANNEL_TRAINING /opt/ml/input/data/training/

# ENTRYPOINT configuration (command to run during training)
ENTRYPOINT ["python", "rvc_train.py"]
```

### Run container
```comandline
docker build -t your_image_name .

docker run --gpus all -v /path/to/local/data:/opt/ml/input/data/training your_image_name
```

<br>

### 4.4. Etc.

Here, we introduce how to download the pretrained files required during the training and inference processes. We need two pretrained parameter files, as detailed below. To ensure precise voice processing, it's essential to prepare the `ffmpeg.exe` and `ffprobe.exe` libraries as well.

> [HuggingFace-1](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main/pretrained_v2): move files below to RVC-model/pretrained_v2
> - `f0D48k.pth`
> - `f0G48k.pth`

> [HuggingFace-2](https://huggingface.co/lj1995/VoiceConversionWebUI/tree/main): move files below to RVC-model/
> - `ffmepg.exe`
> - `ffprobe.exe`

<br/>

### 4.5. Setting parameters


`@rvc-train.py`
- **trainset_dir**: Specifies the folder where the dataset to be used for training is located.
- **exp_dir**: Sets the name of the experiment for the training.

```commandline
python rvc-train.py
```

<br>

`@rvc-infer.py`
- **sid0**: Selects the .pth file specified by the experiment name within the weights folder.
- **input_audio0**: Chooses the original music (vocal file) to be used for inference.
- **file_index2**:  Selects the `added_*.pth` file existing within the `logs/{exp_dir}/` directory.

```commandline
python rvc-infer.py
```

<br/>

## 5. Reference

- [Retrieval-based-Voice-Conversion-WebUI](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI)

- [Ultimate-Vocal-Remover-GUI](https://github.com/Anjok07/ultimatevocalremovergui)
