import os


PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", 3306)
PG_USER = os.getenv("PG_USER", "root")
PG_PASSWORD = os.getenv("PG_PASSWORD", "12345678")
PG_DATABASE = os.getenv("PG_DATABASE", "faiss_qa")

ANSWER_INFO_TABLE = os.getenv("DEFAULT_TABLE", "answer_info")

BERT_SERVING_IP = os.getenv("BERT_SERVING_IP", "127.0.0.1")
