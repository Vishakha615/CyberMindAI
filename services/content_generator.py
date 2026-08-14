
import os
import time
import streamlit as st

from google import genai


# =========================================================
# GEMINI CONFIGURATION
# =========================================================

if "GEMINI_API_KEY" in st.secrets:

    api_key = st.secrets["GEMINI_API_KEY"]

else:

    api_key = os.getenv("GEMINI_API_KEY")


if not api_key:

    raise ValueError(
        "GEMINI_API_KEY is missing."
    )


client = genai.Client(
    api_key=api_key
)


MODEL_NAME = "gemini-3.6-flash"


# =========================================================
# GENERATE QUIZ
# =========================================================

def generate_quiz(
    topic,
    difficulty,
    number_of_questions,
    context
):

    prompt = f"""
You are CyberMind AI, an educational
cybersecurity quiz generator for students.

Generate a multiple-choice quiz using
the provided cybersecurity knowledge.

TOPIC:
{topic}

DIFFICULTY:
{difficulty}

NUMBER OF QUESTIONS:
{number_of_questions}


KNOWLEDGE CONTEXT:
--------------------------------
{context}
--------------------------------


IMPORTANT RULES:

1. Generate exactly {number_of_questions}
   questions.

2. Questions must be related to the
   selected topic.

3. Use the provided knowledge context
   as the primary source.

4. Each question must have exactly
   four options.

5. The options must be labelled
   option_a, option_b, option_c
   and option_d.

6. Every question MUST contain:

   question
   option_a
   option_b
   option_c
   option_d
   correct_answer
   explanation

7. correct_answer MUST contain ONLY
   one of these four values:

   A
   B
   C
   D

8. Do NOT put the complete answer
   inside correct_answer.

9. explanation MUST NOT be empty.

10. explanation must explain clearly
    why the correct answer is correct.

11. Base the explanation on the
    provided knowledge context.

12. Do not invent sources.

13. Do not include markdown.

14. Do not include ```json.

15. Do not include any text before
    or after the JSON.

16. Return ONLY a valid JSON array.


EXPECTED FORMAT:

[
    {{
        "question": "What is cybersecurity?",
        "option_a": "Protecting systems and data",
        "option_b": "Creating websites",
        "option_c": "Designing games",
        "option_d": "Managing databases",
        "correct_answer": "A",
        "explanation": "Cybersecurity is the practice of protecting computer systems, networks, applications and data from unauthorized access, misuse and attacks."
    }}
]


Now generate the quiz.
"""


    # =====================================================
    # GEMINI REQUEST WITH RETRY
    # =====================================================

    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt
            )


            if not response.text:

                raise ValueError(
                    "Gemini returned an empty response."
                )


            return response.text.strip()


        except Exception as e:

            error_message = str(e)


            # Retry temporary Gemini 503 errors

            if (
                "503" in error_message
                and attempt < 2
            ):

                time.sleep(
                    2 ** attempt
                )

                continue


            raise


# =========================================================
# OPTIONAL: GENERATE EXPLANATION
# =========================================================

def generate_explanation(
    question,
    correct_answer,
    context
):

    prompt = f"""
You are CyberMind AI, an educational
cybersecurity mentor.

Explain why the following answer
is correct.

QUESTION:
{question}

CORRECT ANSWER:
{correct_answer}

KNOWLEDGE CONTEXT:
{context}

Give a short, simple explanation
for a cybersecurity student.

Do not provide harmful or unauthorized
cybersecurity instructions.
"""


    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )


    return response.text.strip()




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


