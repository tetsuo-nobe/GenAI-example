"""

invoke_model_with_response_stream の基本 ( Claude と Titan )

"""
import logging
import boto3
import json
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

#bedrock = boto3.client('bedrock')
bedrock_runtime = boto3.client('bedrock-runtime')

#
# Anthropic Claude
# https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/model-parameters-claude.html
#
#
print("---" * 42)
print("Anthropic Claude")
print("---" * 42)

prompt_data = """Human: Please briefly explain what AWS is.
Assistant:
"""

prompt_data_jp = """
Human:AWS とは何かを簡単に説明してください。
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

    response = bedrock_runtime.invoke_model_with_response_stream(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )

    stream = response.get('body')
    # if stream:
    #     for event in stream:
    #         chunk = event.get('chunk')
    #         if chunk:
    #             print(json.loads(chunk.get('bytes').decode()))
    
    count = 0
    if stream:
       for event in stream:
             chunk = event.get('chunk')
             if chunk:
                 chunk_bytes = chunk.get('bytes').decode()
                 result = json.loads(chunk_bytes)
                 count +=1
                 print(f'[{count}] {result["completion"]}')
    
    
    # output = []
    # i = 1
    # if stream:
    #   for event in stream:
    #          chunk = event.get('chunk')
    #          if chunk:
    #              chunk_obj = json.loads(chunk.get('bytes').decode())
    #              text = chunk_obj['completion']
    #              output.append(text)
    #              print(f'\t\t\x1b[31m**Chunk {i}**\x1b[0m\n{text}\n')
    #              i+=1
    
    

except ClientError as error:
    if error.response['Error']['Code'] == 'AccessDeniedException':
           print(f"\x1b[41m{error.response['Error']['Message']}\
                \nTo troubeshoot this issue please refer to the following resources.\
                 \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                 \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")

    else:
        raise error


#
# Amazon Titan Large
# https://docs.aws.amazon.com/ja_jp/bedrock/latest/userguide/model-parameters-titan-text.html
#
#
print("---" * 42)
print("Amazon Titan Large")
print("---" * 42)

prompt_data = """Please briefly explain what AWS is.
"""

prompt_data_jp = """
AWS とは何かを簡単に説明してください。
"""


try:
    
    maxTokenCount = {"maxTokenCount": 500}

    body = json.dumps(
            {
                "inputText": prompt_data, "textGenerationConfig": maxTokenCount
            }
        )
    modelId = "amazon.titan-tg1-large"
    accept = "application/json"
    contentType = "application/json"

    response = bedrock_runtime.invoke_model_with_response_stream(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    
    stream = response.get('body')
    # if stream:
    #   for event in stream:
    #       chunk = event.get('chunk')
    #       if chunk:
    #           print(json.loads(chunk.get('bytes').decode()))

    count = 0
    if stream:
       for event in stream:
             chunk = event.get('chunk')
             if chunk:
                 chunk_bytes = chunk.get('bytes').decode()
                 result = json.loads(chunk_bytes)
                 count +=1
                 print(f'[{count}] {result["outputText"]}')
                 

except ClientError as error:
    if error.response['Error']['Code'] == 'AccessDeniedException':
           print(f"\x1b[41m{error.response['Error']['Message']}\
                \nTo troubeshoot this issue please refer to the following resources.\
                 \nhttps://docs.aws.amazon.com/IAM/latest/UserGuide/troubleshoot_access-denied.html\
                 \nhttps://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html\x1b[0m\n")

    else:
        raise error