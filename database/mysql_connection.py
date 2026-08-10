import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_connection():
    """
    Creates and returns a TiDB Cloud database connection.
    """

    try:
        connection = mysql.connector.connect(
            host=os.getenv("TIDB_HOST"),
            port=int(os.getenv("TIDB_PORT", "4000")),
            user=os.getenv("TIDB_USER"),
            password=os.getenv("TIDB_PASSWORD"),
            database=os.getenv("TIDB_DATABASE"),

            ssl_ca=os.getenv("TIDB_SSL_CA"),
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )

        if connection.is_connected():
            print("✅ TiDB Cloud connected successfully!")
            return connection

    except Error as e:
        print(f"❌ TiDB connection error: {e}")

    return None