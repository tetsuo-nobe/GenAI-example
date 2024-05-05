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
    

data = [
  "Macintosh. Apple computer. Beautiful design. Easy to use interface. very expensive. Not compatible with other computers. Suitable for creative work.",
  "Windows machine. A computer running Microsoft's OS. A wide range of lineups from low to high prices. Huge amount of software. Full range of peripheral equipment. It has an overwhelming market share in business use.",
  "Linux machine. Equipped with open source OS. Very few products are sold. There is little information and you have to solve every problem on your own. Used in the field of development and research.",
  "Chromebook. Low cost computers by Google. Minimum hardware required. It is designed with the premise that much of the work will be done in the cloud. Widely used in the educational field.",
  "Android. It is equipped with an OS developed by Google. It is used in smartphones and tablets, and there are also small PCs. Touch panel operation. It is often used as a second machine."
]


embedding_data = []

for item in data:
    vector = getVec(item)
    embedding_data.append({"content":item, "embedded": vector})

print("Embedding finished.")

with open('data.json','w') as f:
    json.dump(data,f)
    
with open('embedding_data.json','w') as f:
    json.dump(embedding_data,f)
    
print("Embedding data saved.")

prompt = "I want a computer to use in university classes."

# プロンプトのベクトリデータを取得
embedded = getVec(prompt)

cos_data = []

# 保存しておいたベクトルデータとの類似性をチェックする
for item in embedding_data:
 calc = cosineSimilarity(embedded, item['embedded'])
 cos_data.append({"value": calc, "content": item['content']})
 
sorted_data = sorted(cos_data, key=lambda x: x['value'], reverse=True)

print('prompt:' + prompt)
print('result:' + sorted_data[0]['content'])

for item in sorted_data:
    print(item)


