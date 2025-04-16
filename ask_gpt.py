# ask_gpt.py
import os
import openai
from dotenv import load_dotenv


load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]
