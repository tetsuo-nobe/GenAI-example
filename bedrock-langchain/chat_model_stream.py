# https://python.langchain.com/docs/integrations/chat/bedrock/
from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

chat = ChatBedrock(model_id = "anthropic.claude-3-sonnet-20240229-v1:0", model_kwargs={"temperature":0})


messages = [
    HumanMessage(content="自己紹介してください")
]

for chunk in chat.stream(messages):
    print(chunk.content, end="", flush=True)