from langchain_core.output_parsers import  JsonOutputParser,StrOutputParser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate

str_parser = StrOutputParser()
json_parser = JsonOutputParser()

model = ChatTongyi(model = "qwen3-max")
#第一个提示词
first_prompt = PromptTemplate.from_template(
    "我邻居姓：{lastname},刚生了{gender},请帮忙起名字，并封装为JSON的格式返回给我，并且要求key是name,value就是起的名字，请严格遵守格式要求"
)
#第二个提示词
second_prompt = PromptTemplate.from_template(
    "姓名：{name},请帮我解析一下含义"
)
                                #json输出                            string输出
chain = first_prompt | model | json_parser | second_prompt | model |str_parser
for chunk in chain.stream({"lastname":"周","gender":"female"}):

    print(chunk,end=" ",flush=True)