from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models.tongyi import ChatTongyi
chat_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system","你是一个被贬的诗人，可以作诗"),
        MessagesPlaceholder("history"),
        ("human","请再来一首唐诗")
    ]
)

history_data = [
    ("human","你来写一个唐诗"),
    ("ai", "床前明月光，疑似地上霜。举头望明月，低头思故乡。"),
    ("human", "好诗，好诗，再来一个"),
]

model = ChatTongyi(model = "qwen3-max")

#组成链必须是runnable的子类
chain = chat_prompt_template | model

#通过链调用invoke

# res = chain.invoke({"history":history_data})
# print(res.content)
#通过链调用stream
for chunk in chain.stream({"history":history_data}):
    print(chunk.content,end="",flush=True)




