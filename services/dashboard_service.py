from database.mysql_connection import get_connection


def get_learning_progress(user_id):
    connection = get_connection()

    if connection is None:
        return []

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                topic,
                progress_percentage,
                status
            FROM learning_progress
            WHERE user_id = %s
            ORDER BY topic
        """

        cursor.execute(query, (user_id,))

        return cursor.fetchall()

    except Exception as e:
        print(f"Error fetching learning progress: {e}")
        return []

    finally:
        cursor.close()
        connection.close()


def get_dashboard_statistics(user_id):
    connection = get_connection()

    if connection is None:
        return {
            "average_progress": 0,
            "topics_completed": 0
        }

    try:
        cursor = connection.cursor(dictionary=True)

        # Average learning progress
        cursor.execute(
            """
            SELECT
                COALESCE(AVG(progress_percentage), 0)
                AS average_progress
            FROM learning_progress
            WHERE user_id = %s
            """,
            (user_id,)
        )

        progress_result = cursor.fetchone()

        # Completed topics
        cursor.execute(
            """
            SELECT COUNT(*) AS completed_topics
            FROM learning_progress
            WHERE user_id = %s
            AND status = 'Completed'
            """,
            (user_id,)
        )

        completed_result = cursor.fetchone()

        return {
            "average_progress": round(
                float(progress_result["average_progress"]), 1
            ),
            "topics_completed": completed_result["completed_topics"]
        }

    except Exception as e:
        print(f"Dashboard error: {e}")

        return {
            "average_progress": 0,
            "topics_completed": 0
        }

    finally:
        cursor.close()
        connection.close()