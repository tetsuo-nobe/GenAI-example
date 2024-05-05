# from langchain.chat_models import ChatOpenAI # Deprecated
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

chat = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature=0)

messages = [
    SystemMessage(content="You are a helphul assistant."),
    HumanMessage(content="こんにちは！私はジョンといいます。"),
    AIMessage(content="こんにちは、ジョンさん！どのようにお手伝いできますか？"),
    HumanMessage(content="私の名前がわかりますか？")

]
result = chat.invoke(messages)
print(result)