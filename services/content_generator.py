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