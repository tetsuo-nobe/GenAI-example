import boto3
import json

runtime_client = boto3.client(
    service_name = 'bedrock-runtime',
    region_name = 'us-east-1')

modelId = "amazon.titan-embed-text-v1" # Embedding のモデル
accept = "application/json"
contentType = "application/json"

prompt = "Hi, there"

body = json.dumps({
    "inputText": prompt
})

response = runtime_client.invoke_model(
    body = body,
    modelId = modelId
    )

response_body = json.loads(response.get("body").read())
print(response_body)
