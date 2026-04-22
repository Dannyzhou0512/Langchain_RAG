from langchain_core.output_parsers import  JsonOutputParser,StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
str_parser = StrOutputParser()


model = ChatTongyi(model = "qwen3-max")
#第一个提示词
first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname},刚生了{gender},请帮忙起名字,仅仅告诉我名字，不要告诉我其余额外信息。"
)
#第二个提示词
second_prompt = PromptTemplate.from_template(
    "姓名：{name},请帮我解析一下含义"
)
#AImessgae -> dict({"name":"xxxx"})
my_func = RunnableLambda(lambda ai_msg:{"name":ai_msg.content})  #content 的这个属性就是字符串类型的
                                #json输出
chain = first_prompt | model | my_func |second_prompt | model | str_parser
for chunk in chain.stream({"lastname":"上官","gender":"female"}):

    print(chunk,end=" ",flush=True)