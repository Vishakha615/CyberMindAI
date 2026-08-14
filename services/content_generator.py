from services.llm_service import client, MODEL_NAME


def generate_notes(topic, difficulty, context):

    prompt = f"""
You are CyberMind AI, an educational
cybersecurity mentor.

Create clear study notes for a student.

Topic:
{topic}

Student Level:
{difficulty}

Relevant Knowledge:
{context}

Create the notes using this structure:

# Topic

## 1. Introduction

## 2. Important Concepts

## 3. How It Works

## 4. Real-World Example

## 5. Common Mistakes

## 6. Key Points to Remember

Rules:

- Keep the explanation educational.
- Use simple language.
- Do not invent information unsupported
  by the provided knowledge.
- Do not provide harmful or unauthorized
  cyber instructions.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


def generate_quiz(
    topic,
    difficulty,
    number_of_questions,
    context
):

    prompt = f"""
You are CyberMind AI.

Generate a cybersecurity quiz.

Topic:
{topic}

Difficulty:
{difficulty}

Number of questions:
{number_of_questions}

Knowledge Context:
{context}

Return ONLY valid JSON in this format:

[
  {{
    "question": "Question text",
    "option_a": "Option A",
    "option_b": "Option B",
    "option_c": "Option C",
    "option_d": "Option D",
    "correct_option": "A"
  }}
]

Rules:

- Each question must have exactly
  four options.
- correct_option must be A, B, C, or D.
- Questions must be based on the provided
  cybersecurity knowledge.
- Avoid duplicate questions.
- Keep questions appropriate for students.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text








import json
import os
from google import genai
import streamlit as st


if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = os.getenv("GEMINI_API_KEY")


client = genai.Client(api_key=api_key)

MODEL_NAME = "gemini-3.6-flash"


def generate_quiz(
    topic,
    difficulty,
    number_of_questions,
    context
):

    prompt = f"""
You are CyberMind AI, an educational cybersecurity quiz generator.

Generate a multiple-choice cybersecurity quiz.

Topic:
{topic}

Difficulty:
{difficulty}

Number of questions:
{number_of_questions}

Use ONLY the following knowledge context:

------------------
{context}
------------------

For every question provide:

- question
- option_a
- option_b
- option_c
- option_d
- correct_answer
- explanation

The correct_answer MUST be exactly one of:

A
B
C
D

The explanation must clearly explain why that answer is correct.

Return ONLY valid JSON.

Do not use markdown.
Do not use ```json.
Do not add any text before or after the JSON.

Format:

[
    {{
        "question": "Question here",
        "option_a": "Option A",
        "option_b": "Option B",
        "option_c": "Option C",
        "option_d": "Option D",
        "correct_answer": "A",
        "explanation": "Explanation here."
    }}
]
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text
