"""
Memory
"""
from langchain_aws import ChatBedrock
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# LLM
chat = ChatBedrock(model_id = "anthropic.claude-3-sonnet-20240229-v1:0", model_kwargs={"temperature":0})


conversation = ConversationChain(llm=chat, memory=ConversationBufferMemory())

# first: 私の名前はジョンです
# second: 私の名前はわかりまか

while True:
  user_message = input("You: ")
  ai_message = conversation.invoke(input=user_message)
  print(f"AI: {ai_message['response']}")