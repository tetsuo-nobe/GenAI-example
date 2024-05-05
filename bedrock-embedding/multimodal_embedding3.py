import boto3
import io
import os
import json
import base64
import numpy as np
from IPython.display import display, HTML


def cosineSimilarity(vector1, vector2):
    dot = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    similarity = dot / (norm1 * norm2)
    return similarity


def getMultiVec(b64):
    modelId = "amazon.titan-embed-image-v1" # Embedding のモデル    
    body = json.dumps({
        "inputImage": b64
    })
    
    runtime_client = boto3.client(
        service_name = 'bedrock-runtime',
        region_name = 'us-east-1')
    
    response = runtime_client.invoke_model(
        body = body,
        modelId = modelId
    )

    response_body = json.loads(response.get("body").read())
    return response_body["embedding"]
    

def getMultiVec2(p):
    modelId = "amazon.titan-embed-image-v1" # Embedding のモデル    
    body = json.dumps({
        "inputText": p
    })
    
    runtime_client = boto3.client(
        service_name = 'bedrock-runtime',
        region_name = 'us-east-1')
    
    response = runtime_client.invoke_model(
        body = body,
        modelId = modelId
    )

    response_body = json.loads(response.get("body").read())
    return response_body["embedding"]


def listFiles(folder):
    files = []
    for file in os.listdir(folder):
        files.append(os.path.join(folder, file))
    return files
    
def getBase64(path):
    with open(path, "rb") as f:
        data = f.read()
        return base64.b64encode(data).decode("utf-8")
        
folder = "./data"

multi_embedding_data = []
files = listFiles(folder)

for f in files:
    base64_data = getBase64(f)
    emb = getMultiVec(base64_data)
    multi_embedding_data.append({"file":f , "vector": emb})

print("Embedding is over!")

###

prompt = "person"
embedded = getMultiVec2(prompt)

cos_data = []

for item in multi_embedding_data:
    calc = cosineSimilarity(embedded, item["vector"])
    cos_data.append({"value": calc, "file": item["file"]})

sorted_data = sorted(cos_data, key=lambda x: x['value'], reverse=True)

path = sorted_data[0]["file"]
b64 = getBase64(path)

print("prompt:" + prompt)
print("file:" + path)



# def checkCos(p1,p2):
#     v1 = getVec(p1)
#     v2 = getVec(p2)
#     return cosineSimilarity(v1,v2)


