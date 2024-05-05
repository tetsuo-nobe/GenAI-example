# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

chat = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature=0, streaming=True)

messages = [
    HumanMessage(content="自己紹介してください")
]
result = chat.invoke(messages) # Google Colabo だとここで Stream 出力される
