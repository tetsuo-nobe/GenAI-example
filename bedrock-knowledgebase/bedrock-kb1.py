"""

特許情報

https://aws.amazon.com/jp/blogs/news/knowledge-bases-for-amazon-bedrock-rag-patent/

"""
import boto3

# Bedrock Agent Client
agent = boto3.client(service_name='bedrock-agent-runtime')

# 
model_id = "anthropic.claude-v2:1"
model_arn = f'arn:aws:bedrock:us-east-1::foundation-model/{model_id}'
kb_id = "xxxxxxx" # Knowkedge BaseのID
# prompt = "特許JP2013174393Aについて。この特許はどのような内容で、どのような点に新規性、進歩性があるのか、中学生にもわかる言葉で簡潔に説明してください。"
prompt = "モーターの回転運動を往復運動に変換するネジ螺合駆動形式の極低温冷凍機を発案しました。これによって従来の形式よりも機構部分の部品点数が少なくコストが低くできます。これと内容が重複する既存特許はデータソースの中にありますか？"

# retrieve_and_generate
response = agent.retrieve_and_generate(
    input={
        'text': prompt
    },
    retrieveAndGenerateConfiguration={
        'type': 'KNOWLEDGE_BASE',
        'knowledgeBaseConfiguration': {
            'knowledgeBaseId': kb_id,
            'modelArn': model_arn
        }
    },
)

# result

generated_text = response['output']['text']
print(generated_text)
