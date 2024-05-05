"""
Memory
"""
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# LLM
#chat = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature=0)
# gpt-3.5 だと名前を覚えてくれない。gpt-4なら問題ない
chat = ChatOpenAI(model_name = "gpt-4", temperature=0)

conversation = ConversationChain(llm=chat, memory=ConversationBufferMemory())

# first: 私の名前はジョンです
# second: 私の名前はわかりまか

while True:
  user_message = input("You: ")
  ai_message = conversation.invoke(input=user_message)
  print(f"AI: {ai_message['response']}")