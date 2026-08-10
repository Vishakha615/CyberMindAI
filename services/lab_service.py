from database.mysql_connection import get_connection


def get_labs():

    connection = get_connection()

    if connection is None:
        return []

    try:

        cursor = connection.cursor(
            dictionary=True
        )

        cursor.execute(
            """
            SELECT *
            FROM cyber_labs
            ORDER BY lab_id
            """
        )

        return cursor.fetchall()

    except Exception as e:

        print(
            f"Lab loading error: {e}"
        )

        return []

    finally:

        cursor.close()
        connection.close()


def save_lab_result(
    user_id,
    lab_id,
    score
):

    connection = get_connection()

    if connection is None:
        return False

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO lab_results
            (
                user_id,
                lab_id,
                score_percentage
            )
            VALUES (%s, %s, %s)
            """,
            (
                user_id,
                lab_id,
                score
            )
        )

        connection.commit()

        return True

    except Exception as e:

        connection.rollback()

        print(
            f"Lab result error: {e}"
        )

        return False

    finally:

        cursor.close()
        connection.close()


def get_completed_labs(user_id):

    connection = get_connection()

    if connection is None:
        return 0

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM lab_results
            WHERE user_id = %s
            """,
            (user_id,)
        )

        result = cursor.fetchone()

        return result[0]

    except Exception as e:

        print(
            f"Lab statistics error: {e}"
        )

        return 0

    finally:

        cursor.close()
        connection.close()