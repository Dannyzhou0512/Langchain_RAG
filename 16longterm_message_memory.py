import os,json
from typing import Sequence
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import message_to_dict, messages_from_dict, BaseMessage
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import  StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
#message_to_dict:单个消息对象（BaseMessage类实例）-> 字典
#message_from_dict:[字典，字典...] ->[消息，消息...]
#AIMessage、humanMessage、SystemMessage都是BaseMessage的子类

class FileChatMessageHistory(BaseChatMessageHistory):
    def __init__(self,session_id,storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        #完整的文件路径
        self.file_path = os.path.join(self.storage_path,self.session_id)
        #确保文件是存在的
        os.makedirs(os.path.dirname(self.file_path),exist_ok=True)

    def add_messages(self, messages: Sequence[BaseMessage]) -> None:
        #Sequence序列类似于list、tuple
        all_messages = list(self.messages)      #已有的消息列表
        all_messages.extend(messages)           #新的和已有的融合成一个新的list

        #将数据同步写入到本地文件当中
        #类对象写入文件-->一堆二进制
        #为了方便，可以将BaseMessage消息转换成字典（借助JSON模块以JSON字符串的形式写入文件）
        #官方message_to_dict：单个消息对象（BaseMessage类实例） ->字典

        new_messages = []
        for message in all_messages:
            d = message_to_dict(message)
            new_messages.append(d)

        #将数据写入到文件当中
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump(new_messages,f)

    @property               #@property装饰器将message方法变成成员属性用  它的主要作用是将类中的方法转换为属性，使得方法可以像访问普通属性一样被调用，而不需要使用括号。
    def messages(self) -> list[BaseMessage]:
        #当前文件内：list[字典]
        try:
            with open(self.file_path,"r",encoding="utf-8") as f:
                messages_data = json.load(f)
                return messages_from_dict(messages_data)    #将message的格式转换成字典的形式
        except FileNotFoundError:
            return []

    def clear(self) -> None:   #  ->表示函数不返回任何有意义的值，非强制性的
        with open(self.file_path,"w",encoding="utf-8") as f:
            json.dump([],f)



model = ChatTongyi(model = "qwen3-max")
prompt = PromptTemplate.from_template(
    "你需要根据会话历史回复用户问题。对话历史：{chat_history},用户提问：{input},请回答"
)
str_parser = StrOutputParser()
base_chain = prompt | model | str_parser


#通过会话ID获取InmemoryChatMessage类对象
def get_history(session_id):
    return FileChatMessageHistory(session_id,"./chat_history")


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
    # res = Conversation_chat.invoke({"input":"小明有两个猫"},session_config)
    #
    # print("第一次执行",res)
    #
    # res = Conversation_chat.invoke({"input": "小红有四只狗"}, session_config)
    #
    # print("第二次执行", res)
    #
    # res = Conversation_chat.invoke({"input": "小华有一个鹦鹉"}, session_config)
    #
    # print("第三次执行", res)

    res = Conversation_chat.invoke({"input": "总共有多少个宠物？"}, session_config)

    print("第四次执行", res)