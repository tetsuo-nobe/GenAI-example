from langchain.agents import AgentType, initialize_agent, load_tools
# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

chat = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature=0)
tools = load_tools(["ddg-search"])
agent_chain = initialize_agent(
    tools,chat, agent=AgentType.OPENAI_MULTI_FUNCTIONS
)
result = agent_chain.invoke("東京と大阪の天気を教えて")
print(result)