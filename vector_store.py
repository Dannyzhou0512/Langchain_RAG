"""
在向量数据库当中检索数据
"""
from langchain_chroma import Chroma
import config_data as config
from langchain_community.embeddings import DashScopeEmbeddings

class VectorStoreService:
    """
    嵌入模型的传入
    """
    def __init__(self,embedding):
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name = config.collection_name,
            embedding_function = self.embedding,
            persist_directory = config.persist_directory,
        )
    def get_retriever(self):
        """
        :return:返回向量检索器，方便加入chain
        """
        return self.vector_store.as_retriever(search_kwargs = {"k":config.similarity_threshold})   #相似度的阈值

if __name__ == "__main__":
    retriever = VectorStoreService(embedding = DashScopeEmbeddings(model = "text-embedding-v4")).get_retriever()
    res = retriever.invoke("我体重160斤，尺码推荐什么？")
    print(res)