from database.mysql_connection import get_connection


def get_student_profile(user_id):

    connection = get_connection()

    if connection is None:
        return None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT
                u.user_id,
                u.full_name,
                u.email,
                sp.profile_id,
                sp.education_level,
                sp.experience_level,
                sp.career_goal
            FROM users u
            LEFT JOIN student_profiles sp
                ON u.user_id = sp.user_id
            WHERE u.user_id = %s
        """

        cursor.execute(query, (user_id,))

        profile = cursor.fetchone()

        return profile

    except Exception as e:

        print(f"Error fetching profile: {e}")
        return None

    finally:

        cursor.close()
        connection.close()


def update_student_profile(
    user_id,
    education_level,
    experience_level,
    career_goal
):

    connection = get_connection()

    if connection is None:
        return False, "Database connection failed."

    try:

        cursor = connection.cursor()

        query = """
            UPDATE student_profiles
            SET
                education_level = %s,
                experience_level = %s,
                career_goal = %s
            WHERE user_id = %s
        """

        cursor.execute(
            query,
            (
                education_level,
                experience_level,
                career_goal,
                user_id
            )
        )

        connection.commit()

        return True, "Profile updated successfully."

    except Exception as e:

        connection.rollback()

        return False, f"Profile update failed: {e}"

    finally:

        cursor.close()
        connection.close()