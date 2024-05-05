"""

invoke_model の基本 (各種モデルを使用)

"""
import logging
import boto3
import json
from botocore.exceptions import ClientError

### For Image
from PIL import Image
import base64
import io

import datetime


logger = logging.getLogger(__name__)


#
# Amazon Titan Large
# https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/model-parameters-titan-text.html
#
#
print("---" * 42)
print("Amazon Titan Large")
print("---" * 42)

#bedrock = boto3.client('bedrock')
bedrock_runtime = boto3.client('bedrock-runtime')

prompt_data = """Command: Write me a blog about making strong business decisions as a leader.

Blog:
"""

prompt_data_jp = """Command: リーダーとしてビジネス上の強力な意思決定を下すことについてブログを書いてください。

Blog:
"""

try:
    
    maxTokenCount = {"maxTokenCount": 500}

    body = json.dumps(
            {
                "inputText": prompt_data_jp, "textGenerationConfig": maxTokenCount
            }
        )
    modelId = "amazon.titan-tg1-large"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())

    print(response_body.get("results")[0].get("outputText"))

except ClientError as error:
    if error.response['Error']['Code'] == 'AccessDeniedException':
           print(f"\x1b[41m{error.response['Error']['Message']}\
                \nTo troubeshoot this issue please refer to the following resources.\
                 \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                 \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")

    else:
        raise error
        
#
# Anthropic Claude
# https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/model-parameters-claude.html
#
#
print("---" * 42)
print("Anthropic Claude")
print("---" * 42)

#bedrock = boto3.client('bedrock')
bedrock_runtime = boto3.client('bedrock-runtime')

prompt_data = """Human: Write me a blog about making strong business decisions as a leader.

Assistant:
"""

prompt_data_jp = """Human: リーダーとしてビジネス上の強力な意思決定を下すことについてブログを書いてください。

Assistant:
"""

try:

    body = json.dumps(
            {
                "prompt": prompt_data_jp, "max_tokens_to_sample": 500
            }
        )
    modelId = "anthropic.claude-instant-v1"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())

    print(response_body.get("completion"))

except ClientError as error:
    if error.response['Error']['Code'] == 'AccessDeniedException':
           print(f"\x1b[41m{error.response['Error']['Message']}\
                \nTo troubeshoot this issue please refer to the following resources.\
                 \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                 \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")

    else:
        raise error

#
# AI21 Jurassic Grande
# https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/model-parameters-jurassic2.html
# (日本語だと意味のある回答を得られない)
#
print("---" * 42)
print("AI21 Jurassic Grande")
print("---" * 42)

prompt_data = """Human: Write me a blog about making strong business decisions as a leader.

Assistant:
"""

prompt_data_jp = """Human: リーダーとしてビジネス上の強力な意思決定を下すことについてブログを書いてください。

Assistant:
"""

try:

    body = json.dumps(
            {
                "prompt": prompt_data, "maxTokens": 500
            }
        )
    modelId = "ai21.j2-mid-v1"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())

    print(response_body.get("completions")[0].get("data").get("text"))

except ClientError as error:
    if error.response['Error']['Code'] == 'AccessDeniedException':
           print(f"\x1b[41m{error.response['Error']['Message']}\
                \nTo troubeshoot this issue please refer to the following resources.\
                 \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                 \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")

    else:
        raise error


#
# Cohere MetaLlama 2 
# https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/model-parameters-meta.html
# # (日本語のプロンプトは解釈できるがレスポンスは英語)
#
print("---" * 42)
print("Cohere MetaLlama 2")
print("---" * 42)

prompt_data = """Human: Write me a blog about making strong business decisions as a leader.

Assistant:
"""

prompt_data_jp = """Human: リーダーとしてビジネス上の強力な意思決定を下すことについてブログを書いてください。

Assistant:
"""

try:

    body = json.dumps(
            {
                "prompt": prompt_data_jp, "max_gen_len": 500
            }
        )
    modelId = "meta.llama2-13b-chat-v1"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())

    print(response_body.get("generation"))

except ClientError as error:
    if error.response['Error']['Code'] == 'AccessDeniedException':
           print(f"\x1b[41m{error.response['Error']['Message']}\
                \nTo troubeshoot this issue please refer to the following resources.\
                 \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                 \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")

    else:
        raise error



#
# Stability Stable Diffusion XL
# https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/model-parameters-diffusion-1-0-text-image.html
#

print("---" * 42)
print("Stability Stable Diffusion XL")
print("---" * 42)

prompt_data = "a landscape with trees"

prompt_data_jp = "木々のある風景"


try:

    body = json.dumps(
            {
                "text_prompts": [{"text": prompt_data}],
                "cfg_scale": 10,
                "seed": 20,
                "steps": 50
            }
        )
    modelId = "stability.stable-diffusion-xl"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    response_body = json.loads(response.get("body").read())
    
    base64_image = response_body.get("artifacts")[0].get("base64")
    base64_bytes = base64_image.encode('ascii')
    image_bytes = base64.b64decode(base64_bytes)
    
    dt_now = datetime.datetime.now()
    image = Image.open(io.BytesIO(image_bytes))
    image.save(str(dt_now) + ".png")
    

   

except ClientError as error:
    if error.response['Error']['Code'] == 'AccessDeniedException':
           print(f"\x1b[41m{error.response['Error']['Message']}\
                \nTo troubeshoot this issue please refer to the following resources.\
                 \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                 \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")

    else:
        raise error
