from database.mysql_connection import get_connection


def get_topic_performance(user_id):

    connection = get_connection()

    if connection is None:
        return []

    try:

        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                topic,
                AVG(score_percentage) AS average_score,
                COUNT(*) AS attempts
            FROM quizzes
            WHERE user_id = %s
            GROUP BY topic
            ORDER BY average_score ASC
        """

        cursor.execute(
            query,
            (user_id,)
        )

        results = cursor.fetchall()

        return results

    except Exception as e:

        print(
            f"Topic performance error: {e}"
        )

        return []

    finally:

        cursor.close()
        connection.close()


def get_weakest_topic(user_id):

    results = get_topic_performance(
        user_id
    )

    if not results:
        return None

    return results[0]


def get_recommendation_message(
    user_id
):

    weakest = get_weakest_topic(
        user_id
    )

    if not weakest:

        return (
            "Complete a quiz first so "
            "CyberMind AI can analyze your "
            "performance."
        )

    topic = weakest["topic"]

    score = float(
        weakest["average_score"]
    )

    if score < 40:

        level = "Needs significant improvement"

    elif score < 60:

        level = "Needs improvement"

    elif score < 80:

        level = "Developing"

    else:

        level = "Strong"


    recommendation = f"""
### 🎯 Recommended Focus: {topic}

**Average Score:** {score:.1f}%

**Performance:** {level}

### 📚 What you should do

1. Review your {topic} study notes.
2. Ask the AI Mentor about concepts you don't understand.
3. Complete an AI-generated quiz on {topic}.
4. Reattempt the quiz after revision.
"""

    return recommendation
