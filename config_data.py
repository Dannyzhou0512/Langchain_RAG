


md5_path = "./md5.txt"

persist_directory = "./chroma_db"
collection_name = "rag"
chunk_size = 1000
chunk_overlap = 100
separator = ["\n\n","\n",".","!","?","。","？"," ",""]
similarity_threshold = 1
max_split_char_number = 1000
embedding_model_name = "text-embedding-v4"

chat_model_name = "qwen3-max"

config = {
    "configurable": {
        "session_id": "user_001",
    }
}