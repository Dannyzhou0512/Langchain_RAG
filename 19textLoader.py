from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter    #Text字段分隔
loader = TextLoader(
    "./data/data.txt",
    encoding="utf-8",
)

docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=100,     #分段的最大字符数
    chunk_overlap=20,   #分段之间允许重复的字符数
    separators=["\n\n","\n",".","。","!","！","?","？"," "],
    length_function=len,        #统计字符的依据函数
)

splitter_doc = splitter.split_documents(docs)


for doc in splitter_doc:
    print("="*20)
    print(doc)
    print("="*20)
   # print(len(splitter_doc))

