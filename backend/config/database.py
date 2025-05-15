import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("DATABASE_URL"))
db = client["jobfit_db"]

def init_db():
    pass  # Thêm index nếu cần

def save_qa(question, cv_text, jd_text, response):
    db["cv_jd_pairs"].insert_one({
        "question": question,
        "cv_text": cv_text,
        "jd_text": jd_text,
        "response": response
    })