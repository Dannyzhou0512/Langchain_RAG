from tempfile import template

from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_core.prompts import ChatPromptTemplate
'''
PromptTemplate --> StringPromptTemplate --> BasePromptTemplate --> RunnableSerializable --> Runnable
FewShotPromptTemplate --> StringPromptTemplate --> BasePromptTemplate --> RunnableSerializable --> Runnable
ChatPromptTemplate --> BaseChatPromptTemplate --> BasePromptTemplate --> RunnableSerializable --> Runnable
'''

template = PromptTemplate.from_template("我的邻居是,{lastname},最喜欢：{hobby}")
res = template.format(lastname = "张晓梅",hobby = "fishing")
print(res,type(res))

result = template.invoke({"lastname": "周杰伦", "hobby": "singing"})   #传字典的形式
print(result,type(result))