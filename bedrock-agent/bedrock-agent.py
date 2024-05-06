import uuid
import boto3

# Bedrock Agent Client
client = boto3.client("bedrock-agent-runtime")

# 
session_id:str = str(uuid.uuid1())
agent_id:str = 'XXXXXXX' # AgentのID
agent_alias_id:str = 'YYYYYYY' # AgentのエイリアスID (Agentの構成変更後は新しいエイリアスの作成が必要)
prompt = "東京の今日の天気は？" 
#prompt = "特許JP2013174393Aについて。この特許はどのような内容で、どのような点に新規性、進歩性があるのか、中学生にもわかる言葉で簡潔に説明してください。"

# invoke_agent
response = client.invoke_agent(
    inputText=prompt,
    agentId=agent_id,
    agentAliasId=agent_alias_id,
    sessionId=session_id,
    enableTrace=False
)

# Result
#print(response)
event_stream = response['completion']
for event in event_stream:        
    if 'chunk' in event:
        text = event['chunk']['bytes'].decode("utf-8")

print(text)
