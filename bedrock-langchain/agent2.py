from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_aws import ChatBedrock

chat = ChatBedrock(model_id = "anthropic.claude-3-sonnet-20240229-v1:0", model_kwargs={"temperature":0})

tools = load_tools(["ddg-search"])
agent_chain = initialize_agent(
    tools,chat, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION
)
result = agent_chain.invoke({"input": "東京と大阪の天気を教えて"})
print(result)