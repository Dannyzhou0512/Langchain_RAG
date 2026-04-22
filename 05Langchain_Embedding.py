from langchain_community.embeddings import  DashScopeEmbeddings


#不传model，默认为text-embedding
model = DashScopeEmbeddings()
#不用invoke和stream用embed_query、embed_documents
print(model.embed_query("我喜欢你"))
print(model.embed_documents(["我喜欢你","黑凤梨"]))