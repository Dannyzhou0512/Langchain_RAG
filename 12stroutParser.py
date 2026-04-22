from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

parser = StrOutputParser()

model = ChatTongyi(model = "qwen-max")
prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname},刚生了{gender}，请起名，仅告诉我名字无需其他内存"
)
chain = prompt | model | parser | model

res = chain.invoke({"lastname":"张","gender":"female"})
print(res.content)