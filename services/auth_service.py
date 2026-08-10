import hashlib
from database.mysql_connection import get_connection


def hash_password(password):
    """
    Converts a password into a SHA-256 hash.
    """
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


def register_user(full_name, email, password):

    connection = get_connection()

    if connection is None:
        return False, "Database connection failed."

    try:

        cursor = connection.cursor()

        # Check whether email already exists
        cursor.execute(
            "SELECT user_id FROM users WHERE email = %s",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            return False, "Email already registered."

        password_hash = hash_password(password)

        # Insert user
        cursor.execute(
            """
            INSERT INTO users
            (full_name, email, password_hash)
            VALUES (%s, %s, %s)
            """,
            (full_name, email, password_hash)
        )

        user_id = cursor.lastrowid

        # Create empty student profile
        cursor.execute(
            """
            INSERT INTO student_profiles
            (user_id)
            VALUES (%s)
            """,
            (user_id,)
        )

        connection.commit()

        return True, "Registration successful."

    except Exception as e:

        connection.rollback()

        return False, f"Registration failed: {e}"

    finally:

        cursor.close()
        connection.close()


def login_user(email, password):

    connection = get_connection()

    if connection is None:
        return False, None, "Database connection failed."

    try:

        cursor = connection.cursor(dictionary=True)

        password_hash = hash_password(password)

        cursor.execute(
            """
            SELECT user_id, full_name, email
            FROM users
            WHERE email = %s
            AND password_hash = %s
            """,
            (email, password_hash)
        )

        user = cursor.fetchone()

        if user:

            return True, user, "Login successful."

        return False, None, "Invalid email or password."

    except Exception as e:

        return False, None, f"Login failed: {e}"

    finally:

        cursor.close()
        connection.close()