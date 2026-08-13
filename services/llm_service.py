import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing from .env"
    )


client = genai.Client(
    api_key=api_key
)


MODEL_NAME = "gemini-3.6-flash"


def generate_mentor_response(
    question,
    context
):

    prompt = f"""
You are CyberMind AI, an educational
cybersecurity mentor for students.

Your job is to explain cybersecurity
concepts clearly and safely.

Use the provided knowledge context
to answer the student's question.

KNOWLEDGE CONTEXT:
------------------
{context}
------------------

STUDENT QUESTION:
{question}

Instructions:

1. Give an accurate educational answer.
2. Prefer the provided context.
3. Explain difficult concepts simply.
4. Use examples when helpful.
5. If the context does not contain enough
   information, clearly say that.
6. Do not invent sources or facts.
7. Do not provide instructions that enable
   harmful or unauthorized cyber activity.
8. Keep the answer organized and student-friendly.

Answer:
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text



