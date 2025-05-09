import openai
from google import genai
import os
from dotenv import load_dotenv
from services.similarity_service import calculate_similarity
from services.cv_service import create_cv_embedding
from services.jd_service import create_jd_embedding

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def openai_chat_completion(prompt: str, model_name: str = "gpt-4", max_tokens: int = 500) -> str:
    """
    Generates a chat completion using OpenAI's model.
    :param prompt: The prompt to send to the model.
    :param model_name: The name of the model to use (default is "gpt-4").
    :param max_tokens: The maximum number of tokens to generate (default is 500).
    :return: The response from the model.
    """
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

def gemini_chat_completion(prompt: str, model_name: str = "gemini-2.0-flash") -> str:
    """
    Generates a chat completion using Google's Gemini model.
    :param prompt: The prompt to send to the model.
    :param model_name: The name of the model to use (default is "gemini-2.0-flash").
    :return: The response from the model.
    """
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
    )
    return response.text

def answer_question(question, cv_text, jd_text, chat_model: str = "gemini-2.0-flash") -> str:
    """
    Answers a question based on the CV and JD text using OpenAI's model.
    :param question: The question to answer.
    :param cv_text: The CV text to use for context.
    :param jd_text: The JD text to use for context.
    :param chat_model: The name of the model to use (default is "gemini-2.0-flash")
    :return: The answer to the question.
    """
    cv_embedding = create_cv_embedding(cv_text)
    jd_embedding = create_jd_embedding(jd_text)
    match_score = calculate_similarity(cv_embedding, jd_embedding)
    prompt = (
        f"Question: {question}\n"
        f"CV: {cv_text}\n"
        f"JD: {jd_text}\n"
        f"Match Score: {match_score:.2f}%\n"
        "Answer in Vietnamese with suggestions."
    )
    if chat_model == "gpt-4":
        response = openai_chat_completion(prompt, model_name="gpt-4", max_tokens=500)
    elif "gemini" in chat_model:
        response = gemini_chat_completion(prompt, model_name=chat_model)
    else:
        raise ValueError("Invalid chat model specified. Use 'gpt-4' or 'gemini'.")
    return response