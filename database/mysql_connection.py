import os
import tempfile

import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    try:

        # =========================
        # STREAMLIT CLOUD
        # =========================
        if "TIDB_HOST" in st.secrets:

            host = st.secrets["TIDB_HOST"]
            port = int(st.secrets["TIDB_PORT"])
            user = st.secrets["TIDB_USER"]
            password = st.secrets["TIDB_PASSWORD"]
            database = st.secrets["TIDB_DATABASE"]

            # Get certificate CONTENT from Streamlit Secrets
            ca_content = st.secrets["TIDB_SSL_CA"]

            # Create temporary PEM file
            with tempfile.NamedTemporaryFile(
                mode="w",
                suffix=".pem",
                delete=False
            ) as ca_file:

                ca_file.write(ca_content)
                ssl_ca = ca_file.name

        # =========================
        # LOCAL
        # =========================
        else:

            host = os.getenv("TIDB_HOST")
            port = int(os.getenv("TIDB_PORT", "4000"))
            user = os.getenv("TIDB_USER")
            password = os.getenv("TIDB_PASSWORD")
            database = os.getenv("TIDB_DATABASE")

            ssl_ca = os.getenv("TIDB_SSL_CA")

        # =========================
        # CONNECT
        # =========================

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
            print("✅ TiDB connection successful!")
            return connection

    except Error as e:
        print(f"❌ TiDB connection error: {e}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")

    return None
