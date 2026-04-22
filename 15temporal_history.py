from click import prompt, parser
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import  StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory


model = ChatTongyi(model = "qwen3-max")
prompt = PromptTemplate.from_template(
    "你需要根据会话历史回复用户问题。对话历史：{chat_history},用户提问：{input},请回答"
)
str_parser = StrOutputParser()
base_chain = prompt | model | str_parser

store = {}
#通过会话ID获取InmemoryChatMessage类对象
def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]


#创建一个新的链，对原有的链进行增强
Conversation_chat= RunnableWithMessageHistory(
    base_chain, #被增强原始的链
    get_history, #通过会话ID获取InmemoryChatMessage类对象
    input_messages_key="input",   #表示用户输入在模板当中的占位符
    history_messages_key="chat_history",
)

if __name__ == "__main__":
    #固定格式，添加langchain的配置，为当前程序配置所属的session_id
    session_config = {
    "configurable":{"session_id":"user_001"},
    }
    res = Conversation_chat.invoke({"input":"小明有两个猫"},session_config)

    print("第一次执行",res)

    res = Conversation_chat.invoke({"input": "小红有四只狗"}, session_config)

    print("第二次执行", res)

    res = Conversation_chat.invoke({"input": "小华有一个鹦鹉"}, session_config)

    print("第三次执行", res)

    res = Conversation_chat.invoke({"input": "总共有多少个宠物？"}, session_config)

    print("第四次执行", res)