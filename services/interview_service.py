from services.llm_service import (
    client,
    MODEL_NAME
)


def generate_interview_question(
    topic,
    difficulty
):

    prompt = f"""
You are CyberMind AI, an educational
cybersecurity interview mentor.

Generate ONE interview question.

Topic:
{topic}

Difficulty:
{difficulty}

The question should test understanding,
not require performing any real cyber attack.

Return only the question.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text.strip()


def evaluate_answer(
    topic,
    question,
    answer
):

    prompt = f"""
You are CyberMind AI, a cybersecurity
interview evaluator.

Topic:
{topic}

Question:
{question}

Student Answer:
{answer}

Evaluate the answer.

Return exactly this format:

SCORE: <number from 0 to 100>

STRENGTHS:
<what the student explained correctly>

IMPROVEMENTS:
<what the student should improve>

MODEL ANSWER:
<a concise ideal answer>

Keep the evaluation educational.
Do not provide instructions for harmful
cyber activities.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text



from database.mysql_connection import (
    get_connection
)


def save_interview_result(
    user_id,
    topic,
    question,
    student_answer,
    score,
    feedback
):

    connection = get_connection()

    if connection is None:
        return False

    try:

        cursor = connection.cursor()

        query = """
            INSERT INTO interview_results
            (
                user_id,
                topic,
                question,
                student_answer,
                score,
                feedback
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                user_id,
                topic,
                question,
                student_answer,
                score,
                feedback
            )
        )

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(
            f"Interview save error: {e}"
        )

        return False

    finally:

        cursor.close()
        connection.close()