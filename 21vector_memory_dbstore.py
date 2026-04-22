from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader

#InMemory是内存存储
vector_store = Chroma(
    collection_name="test",
    embedding_function = DashScopeEmbeddings(),
    persist_directory="./chroma_db"
)
loader = CSVLoader(
    file_path="./data/info.csv",
    source_column="source",   #指定本条数据的来源是哪里
    encoding="utf-8"
)

documents = loader.load()
#向量的存储、新增、删除、检索

#id1,id2,id3...
vector_store.add_documents(
    documents = documents,
    ids = ["id"+str(i) for i in range(1,len(documents) + 1)]
)

#删除  传入["id1","id2"]
vector_store.delete(["id1","id2"])

#检索  返回类型   相似性检索
result = vector_store.similarity_search(
    "AI怎么样？",
    3   #检索的结果需要几个
)

print(result)
