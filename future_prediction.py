import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_future_career_options(department):
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 200,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    chat_session = model.start_chat(
        history=[]
    )

    prompt = f"Based on the department '{
        department}', provide exactly three possible career futures in a concise list. Do not give detailed descriptions, just the career names."

    response = chat_session.send_message(prompt)

    careers_list = response.text.strip().split(
        '\n')[:3]

    return careers_list
