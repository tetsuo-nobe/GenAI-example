from langchain.agents import AgentType, initialize_agent, load_tools
#from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature=0)
tools = load_tools(["terminal"], allow_dangerous_tools=True)
agent_chain = initialize_agent(
    tools,chat, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
result = agent_chain.invoke("現在のディレクトリにあるファイルの一覧を教えて")
print(result)