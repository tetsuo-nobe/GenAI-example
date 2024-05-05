# from langchain_community.llms import Bedrock # Deprecated
from langchain_aws import BedrockLLM
import boto3

## bedrock-runtimeのインスタンス化
bedrock_runtime = boto3.client(
        service_name="bedrock-runtime",
        region_name="us-east-1"
)

# モデルにClaude3 Sonnetを選択 
llm = BedrockLLM(
      # model_id = "anthropic.claude-3-sonnet-20240229-v1:0", # Claude 3 では BedrockLLM は使えない
      model_id = "anthropic.claude-v2",
      region_name = "us-east-1",
      client = bedrock_runtime,
      model_kwargs={
            "max_tokens_to_sample": 4096,
            "temperature": 0,
            "stop_sequences": []
      }
)


result = llm.invoke("自己紹介してください")
print(result)