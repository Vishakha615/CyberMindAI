import os
import tempfile

import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    try:

        # ---------------------------------
        # Streamlit Cloud / Streamlit Secrets
        # ---------------------------------
        if "TIDB_HOST" in st.secrets:

            host = st.secrets["TIDB_HOST"]
            port = int(st.secrets["TIDB_PORT"])
            user = st.secrets["TIDB_USER"]
            password = st.secrets["TIDB_PASSWORD"]
            database = st.secrets["TIDB_DATABASE"]

            # Get CA certificate content
            ca_cert = st.secrets["TIDB_CA_CERT"]

            # Create temporary .pem file
            ca_file = tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".pem",
                delete=False
            )

            ca_file.write(ca_cert)
            ca_file.close()

            ssl_ca = ca_file.name

        # ---------------------------------
        # Local .env
        # ---------------------------------
        else:

            host = os.getenv("TIDB_HOST")
            port = int(os.getenv("TIDB_PORT", "4000"))
            user = os.getenv("TIDB_USER")
            password = os.getenv("TIDB_PASSWORD")
            database = os.getenv("TIDB_DATABASE")
            ssl_ca = os.getenv("TIDB_SSL_CA")

        # ---------------------------------
        # Connect to TiDB
        # ---------------------------------

        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            ssl_ca=ssl_ca,
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )

        if connection.is_connected():
            print("✅ TiDB Cloud connected successfully!")
            return connection

    except Error as e:
        print(f"❌ TiDB connection error: {e}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return None
