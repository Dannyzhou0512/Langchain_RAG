from langchain_community.llms.tongyi import Tongyi

model = Tongyi(model = "qwen-max")

res = model.stream(input = "介绍一下江苏省宝应县")

for chunk in res:
    print(chunk,end=" ",flush=True)