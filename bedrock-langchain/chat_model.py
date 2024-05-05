# https://python.langchain.com/docs/integrations/chat/bedrock/
from langchain_aws import ChatBedrock
from langchain.schema import AIMessage, HumanMessage, SystemMessage

chat = ChatBedrock(model_id = "anthropic.claude-3-sonnet-20240229-v1:0", model_kwargs={"temperature":0})

messages = [
    SystemMessage(content="You are a helphul assistant."),
    HumanMessage(content="こんにちは！私はジョンといいます。"),
    AIMessage(content="こんにちは、ジョンさん！どのようにお手伝いできますか？"),
    HumanMessage(content="私の名前がわかりますか？")

]
result = chat.invoke(messages)
print(result)