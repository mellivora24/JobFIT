import openai
import os
from dotenv import load_dotenv
from backend.utils.file_utils import extract_text_from_file

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def create_cv_embedding(cv_file):
    """
    Tạo embedding cho CV bằng OpenAI API
    :param cv_file: CV file (PDF)
    :return: embedding vector
    """
    try:
        # Trích xuất văn bản từ file (PDF)
        text = extract_text_from_file(cv_file)
        if not text:
            raise ValueError("Không thể trích xuất văn bản từ CV")

        # Gọi OpenAI API để tạo embedding
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response['data'][0]['embedding']
    except Exception as e:
        raise Exception(f"Lỗi khi tạo embedding cho CV: {str(e)}")