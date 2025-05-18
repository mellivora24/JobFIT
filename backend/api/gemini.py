import os
from google import genai
from dotenv import load_dotenv

def call_gemini_api(message):
    """
    Gọi API Gemini
    :param message: string
    :return: string
    """
    load_dotenv()

    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=message,
    )
    return response.text

# Đã kiểm thử