"""
 Chain
"""
from langchain_aws import ChatBedrock
from langchain.prompts import PromptTemplate
#from langchain import LLMChain
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain

# LLM
chat = ChatBedrock(model_id = "anthropic.claude-3-sonnet-20240229-v1:0", model_kwargs={"temperature":0})

# Tempale #1
cot_template = """
以下の質問に回答して下さい。

質問： {question}

ステップバイステップで考えましょう。
"""
# Prompt #1
cot_prompt = PromptTemplate(
    input_variables=["question"],
    template=cot_template
)

# Chain #1
cot_chain = LLMChain(llm=chat, prompt=cot_prompt)

# Template #2
summarize_template = """以下の文章を結論だけ一言に要約して下さい。

{input}
"""
# Prompt #2
summarize_prompt = PromptTemplate(
    input_variables = ["input"],
    template = summarize_template
)

# Chain #2
summarize_chain = LLMChain(llm=chat, prompt=summarize_prompt)

# SimpleSequentialChain
cot_summarize_chain = SimpleSequentialChain(
    chains=[cot_chain,summarize_chain]
)

result = cot_summarize_chain.invoke("私は市場に行って10個のリンゴを買いました。隣人に2つ、修理工に2つ渡しました。それから5つのリンゴを買って1つ食べました。残りは何個ですか？")

print(result["output"])
