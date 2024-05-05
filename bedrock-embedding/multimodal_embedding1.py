import boto3
import io
import json
import base64
import numpy as np

modelId = "amazon.titan-embed-image-v1" # Embedding のモデル   

prompt = "a cat."
filename = "cat.jpg"

with open(filename,"rb") as f:
    data = f.read()
    base64_data = base64.b64encode(data).decode("utf-8")

body = json.dumps({
        "inputText": prompt,
        "inputImage": base64_data
})

runtime_client = boto3.client(
    service_name = 'bedrock-runtime',
    region_name = 'us-east-1')
    
response = runtime_client.invoke_model(
    body = body,
    modelId = modelId
)

response_body = json.loads(response.get("body").read())
print(response_body)

