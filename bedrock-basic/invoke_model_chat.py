"""

Chat のように継続的に会話していく
invoke_model使用(Titan)

"""
import logging
import boto3
import json
from botocore.exceptions import ClientError

bedrock_runtime = boto3.client('bedrock-runtime')

app_prompt = ""
flag = True

while flag:
    prompt = input("prompt:")
    
    # 入力なしの場合 while から抜ける
    if prompt == "":
        flag = False
    else:
        # プロンプトを追加
        app_prompt += f'\n\nHuman: {prompt}\n\nAssistant: '
        
        # body用のコンテンツを作成
        body = json.dumps(
            {
                "inputText": app_prompt, 
                "textGenerationConfig":{
                    "temperature": 0.5,
                    "maxTokenCount": 1000,
                    "topP": 0.2,
                    "stopSequences":[]
                } 
            }
        )
        modelId = "amazon.titan-tg1-large"
        accept = "application/json"
        contentType = "application/json"
        
        # AI モデルに invoke_model 実行
        response = bedrock_runtime.invoke_model(
            body=body, modelId=modelId, accept=accept, contentType=contentType
        )
        
        # 結果を受け取り応答を表示
        response_body = json.loads(response.get("body").read())
        result = response_body.get("results")[0].get("outputText")
        print(f'Result: {result}')
        app_prompt += result # 応援を追加

print("Good bye!")