from database.mysql_connection import get_connection


def get_quiz_questions(topic, difficulty, limit=5):

    connection = get_connection()

    if connection is None:
        return []

    try:

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                question_id,
                topic,
                question_text,
                option_a,
                option_b,
                option_c,
                option_d,
                correct_option,
                difficulty
            FROM quiz_questions
            WHERE topic = %s
            AND difficulty = %s
            ORDER BY RAND()
            LIMIT %s
        """

        cursor.execute(
            query,
            (topic, difficulty, limit)
        )

        return cursor.fetchall()

    except Exception as e:

        print(f"Quiz loading error: {e}")
        return []

    finally:

        cursor.close()
        connection.close()


def save_quiz_result(
    user_id,
    topic,
    total_questions,
    correct_answers
):

    connection = get_connection()

    if connection is None:
        return False

    try:

        cursor = connection.cursor()

        score = (
            correct_answers / total_questions
        ) * 100

        query = """
            INSERT INTO quiz_results
            (
                user_id,
                topic,
                total_questions,
                correct_answers,
                score_percentage
            )
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                user_id,
                topic,
                total_questions,
                correct_answers,
                score
            )
        )

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(f"Quiz result error: {e}")

        return False

    finally:

        cursor.close()
        connection.close()


def get_quiz_statistics(user_id):

    connection = get_connection()

    if connection is None:
        return {
            "quizzes_completed": 0,
            "average_score": 0
        }

    try:

        cursor = connection.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                COUNT(*) AS quizzes_completed,
                COALESCE(
                    AVG(score_percentage),
                    0
                ) AS average_score
            FROM quiz_results
            WHERE user_id = %s
            """,
            (user_id,)
        )

        result = cursor.fetchone()

        return {
            "quizzes_completed": result["quizzes_completed"],
            "average_score": round(
                float(result["average_score"]),
                1
            )
        }

    except Exception as e:

        print(f"Quiz statistics error: {e}")

        return {
            "quizzes_completed": 0,
            "average_score": 0
        }

    finally:

        cursor.close()
        connection.close()