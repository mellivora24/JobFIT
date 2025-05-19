import os
from openai import OpenAI
from dotenv import load_dotenv

def call_chatgpt_api(message):
    """
    Gọi API ChatGPT
    :param message: string
    :return: string
    """

    load_dotenv()
    client = OpenAI(api_key=os.getenv("CHATGPT_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": message}
        ]
    )

    return response.choices[0].message.content

# Đã kiểm tra