from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_questions(resume_text):

    prompt = f"""
    Generate exactly 10 interview questions.

    Rules:
    - Return only questions.
    - No headings.
    - No category names.
    - No introductions.
    - One question per line.

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content