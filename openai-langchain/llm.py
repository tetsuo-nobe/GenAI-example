# from langchain.llms import OpenAI # Deprecated
from langchain_community.llms import OpenAI
import os

# OpenAI API Key のインポート
#os.environ["OPENAI_API_KEY"] = ""

llm = OpenAI(model_name = "gpt-3.5-turbo", temperature=0)

result = llm.invoke("自己紹介してください")
print(result)