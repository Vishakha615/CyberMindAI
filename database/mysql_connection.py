import os
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import certifi

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

            # Streamlit Cloud runs on Linux
            # Use the system CA certificate bundle
            ssl_ca = "/etc/ssl/certs/ca-certificates.crt"

            # Fallback to certifi if system path is unavailable
            if not os.path.exists(ssl_ca):
                ssl_ca = certifi.where()

        # =========================
        # LOCAL COMPUTER
        # =========================
        else:

            host = os.getenv("TIDB_HOST")
            port = int(os.getenv("TIDB_PORT", "4000"))
            user = os.getenv("TIDB_USER")
            password = os.getenv("TIDB_PASSWORD")
            database = os.getenv("TIDB_DATABASE")
            ssl_ca = os.getenv("TIDB_SSL_CA")

        # =========================
        # CONNECT TO TiDB
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
            print("✅ TiDB Cloud connection successful!")
            return connection

    except Error as e:
        st.error(f"❌ TiDB ERROR: {e}")
        return None

    except Exception as e:
        st.error(f"❌ UNEXPECTED ERROR: {e}")
        return None

    return None
