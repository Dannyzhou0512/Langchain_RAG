from langchain_community.document_loaders import CSVLoader


loader = CSVLoader(
    file_path="./data/stu.csv",
    csv_args={"delimiter": "，","fieldnames": ["name", "age", "gender"]},    #指定分隔符
    encoding="utf-8",
)

#批量加载  一次性加载
# documents = loader.load()
# for document in documents:
#     print(document,type(document))

#lazy迭代器加载

for document in loader.lazy_load():
    print(document)