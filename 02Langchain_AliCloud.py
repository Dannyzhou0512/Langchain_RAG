from kubernetes.stream import stream
from langchain_community.llms.tongyi import Tongyi

model = Tongyi(model = "qwen-plus",
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"


               )    #qwen-max 是LLM

res = model.invoke(input="你是谁，能做什么？")

print(res)

