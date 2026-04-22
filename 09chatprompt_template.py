from h5py.h5f import flush
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

model = ChatTongyi(
    model = "qwen3-max"
)
prompt_text = chat_prompt_template.invoke({"history":history_data}).to_string()
res = model.invoke(prompt_text,end = " ",flush = False)

print(res.content,type(res))

