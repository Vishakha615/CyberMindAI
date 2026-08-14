'''from database.mysql_connection import get_connection


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

    return recommendation'''





from database.mysql_connection import get_connection


# =========================================================
# GET TOPIC PERFORMANCE
# =========================================================

def get_topic_performance(user_id):

    connection = get_connection()

    if connection is None:
        return []

    cursor = None

    try:

        cursor = connection.cursor(
            dictionary=True
        )

        query = """
            SELECT
                topic,
                AVG(score) AS average_score,
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
            f"Recommendation error: {e}"
        )

        return []

    finally:

        if cursor:
            cursor.close()

        connection.close()


# =========================================================
# GET RECOMMENDATION MESSAGE
# =========================================================

def get_recommendation_message(user_id):

    performance = get_topic_performance(
        user_id
    )

    if not performance:

        return (
            "📚 Complete some quizzes first. "
            "Your personalized recommendation "
            "will appear here."
        )


    # Find weakest topic

    weakest = performance[0]

    weakest_topic = weakest["topic"]

    weakest_score = float(
        weakest["average_score"]
    )


    # Find strongest topic

    strongest = max(
        performance,
        key=lambda x:
        float(x["average_score"])
    )

    strongest_topic = strongest["topic"]

    strongest_score = float(
        strongest["average_score"]
    )


    # -----------------------------------------------------
    # Recommendation based on score
    # -----------------------------------------------------

    if weakest_score < 50:

        return (
            f"🔴 **Focus on {weakest_topic} first.**\n\n"
            f"Your average score in this topic is "
            f"**{weakest_score:.1f}%**. "
            f"Review the fundamentals and take more "
            f"practice quizzes before moving to advanced "
            f"concepts."
        )


    elif weakest_score < 75:

        return (
            f"🟡 **Practice {weakest_topic} more.**\n\n"
            f"Your current average is "
            f"**{weakest_score:.1f}%**. "
            f"You understand the basics, but more "
            f"practice will improve your confidence."
        )


    else:

        return (
            f"🟢 **Great progress!**\n\n"
            f"Your weakest topic is **{weakest_topic}** "
            f"with an average of **{weakest_score:.1f}%**.\n\n"
            f"You are also performing strongly in "
            f"**{strongest_topic}** "
            f"({strongest_score:.1f}%). "
            f"Consider moving toward more advanced "
            f"cybersecurity concepts."
        )
