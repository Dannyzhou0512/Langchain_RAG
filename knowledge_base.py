import os

from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
import config_data as config
import hashlib
from datetime import datetime

"""
check_md5()、save_md5()、get_string_md5()都是工具函数
"""

def check_md5(md5_str:str):
    """
    检查传入的md5字符串是否已经被处理过了
    return False(md5未处理过)
    :param md5_str:
    :return:
    """
    if not os.path.exists(config.md5_path):     #if进入表示文件不存在，那肯定没有处理过md5
        open(config.md5_path, 'w',encoding='utf-8').close()
        return False
    else:
        for line in open(config.md5_path, 'r', encoding='utf-8'):
            line = line.strip() #处理字符串前后的空格和回车
            if line == md5_str:
                return True  #已经处理过

        return False

def save_md5(md5_str:str):#将传入的字符串转换为md5字符串
    """
    将传入的md5字符串，记录到文件内保存
    :param md5_str:
    :param encoding:
    :return:
    """
    with open(config.md5_path, 'a', encoding = 'utf-8') as f:   #'a' = append（追加模式）
        f.write(md5_str + '\n')
    pass

def get_string_md5(input_str:str,encoding = 'utf-8'):
    #将字符串转换为byte字节数组
    str_byte = input_str.encode(encoding= encoding)
    #创建md5对象
    md5_obj = hashlib.md5()  #得到md5对象
    md5_obj.update(str_byte)   #传入即将要转换的字节数组
    md5_hex = md5_obj.hexdigest()    #得到md5的十六进制字符串

    return md5_hex

#---------------------------------------------------------------------------------------------------------------------------
class KnowledgeBaseService(object):
    def __init__(self):                           #初始化对象部分进行向量数据库的声明，分割器的声明
        # 如果文件不存在则创建，如果存在则跳过
        os.makedirs(config.persist_directory,exist_ok=True)
        self.chroma = Chroma(
            collection_name = config.collection_name,  #数据库的表名
            embedding_function = DashScopeEmbeddings(model = "text-embedding-v4"),
            persist_directory = config.persist_directory     #数据库本地存储文件夹
        )    #向量存储的额实例Chroma向量库对象

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size = config.chunk_size,   #分割后的文本段的最大长度
            chunk_overlap = config.chunk_overlap, #连续文本段之间的字符重叠数量
            separators = config.separator,  #自然段落划分的符号
            length_function = len,   #使用Python自带的len函数作为长度统计的依据
        )  #文本分割器的对象

    def upload_by_str(self,data:str,filename):
        #将传入的字符串进行向量化，存入到向量数据库当中
        #先得到传入字符串的md5的值
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):   #如果说检查过了则进行跳过
            return "[跳过]内容已经存在知识库当中"

        if len(data) > config.max_split_char_number:
            knowledge_chunks:list[str] = self.spliter.split_text(data)   #类型注解
        else:
            knowledge_chunks = [data]

        metadata = {
            "source" : filename,
            #2026-04-22 10:00:00
            "create_time" : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "Danny"
        }

        self.chroma.add_texts(   #内容加载到向量库当中
            knowledge_chunks,
            metadata =[metadata for _ in knowledge_chunks],    #这里的 _ 表示对metadata里面的数据进行一个逐渐的追加的一个过程    这个变量的值我不关心只用来迭代
        )

        save_md5(md5_hex)

        return "[成功]内容已经成功载入向量库"





def main():

   service = KnowledgeBaseService()
   r = service.upload_by_str("林丹","testfile")
   print(r)

if __name__ == '__main__':
    main()


