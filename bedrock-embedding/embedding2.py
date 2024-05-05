import boto3
import json
import numpy as np

#####

def cosineSimilarity(vector1, vector2):
    dot = np.dot(vector1, vector2)
    norm1 = np.linalg.norm(vector1)
    norm2 = np.linalg.norm(vector2)
    similarity = dot / (norm1 * norm2)
    return similarity

def getVec(p):
    modelId = "amazon.titan-embed-text-v1" # Embedding のモデル    
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
    return response_body['embedding']

def checkCos(p1,p2):
    v1 = getVec(p1)
    v2 = getVec(p2)
    return cosineSimilarity(v1,v2)
    
prompt1 = "I feel great today."
prompt2 = "It is a good weather today."
prompt3 = "It's overtime again tonight."

p1_p2 = checkCos(prompt1,prompt2)
p1_p3 = checkCos(prompt1,prompt3)
p2_p3 = checkCos(prompt2,prompt3)

print(f'p1-p2: {p1_p2}')
print(f'p1-p3: {p1_p3}')
print(f'p2-p3: {p2_p3}')

###########################

