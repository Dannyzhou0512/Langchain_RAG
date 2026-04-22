from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

#得到模型对象
model = ChatTongyi(model = "qwen3-max")

'''message = [
    SystemMessage(content="你是一个被贬的诗人，且壮志难酬"),
    HumanMessage(content="写一首唐诗"),
    AIMessage(content="锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    HumanMessage(content="按照上面的格式帮我写一首")
]'''
messages = [
    ("system","你是一个被贬的诗人，且壮志难酬"),
    ("human","写一首唐诗"),
    ("ai","锄禾日当午，汗滴禾下土，谁知盘中餐，粒粒皆辛苦。"),
    ("human","按照上面的格式帮我写一首")
]

res = model.stream(input = messages)

for chunk in res:
    print(chunk.content,end = " ",flush = True)