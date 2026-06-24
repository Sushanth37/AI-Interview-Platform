from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def evaluate_answer(answer):

    prompt = f"""
    You are an interview evaluator.

    Evaluate this answer.

    Give:

    Confidence Score (/10)
    Clarity Score (/10)
    Communication Score (/10)

    Improvement Areas

    Answer:
    {answer}
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