from langchain.prompts import PromptTemplate

template = """
以下の料理のレシピを考えて下さい。

料理名： {dish}
"""

prompt = PromptTemplate(
    input_variables=["dish"],
    template=template
)
result = prompt.format(dish = "カレー")
print(result)
