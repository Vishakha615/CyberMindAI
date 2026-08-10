   
import os
import streamlit as st
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    try:

        if "TIDB_HOST" in st.secrets:

            host = st.secrets["TIDB_HOST"]
            port = int(st.secrets["TIDB_PORT"])
            user = st.secrets["TIDB_USER"]
            password = st.secrets["TIDB_PASSWORD"]
            database = st.secrets["TIDB_DATABASE"]
            ssl_ca = st.secrets["TIDB_SSL_CA"]

        else:

            host = os.getenv("TIDB_HOST")
            port = int(os.getenv("TIDB_PORT", "4000"))
            user = os.getenv("TIDB_USER")
            password = os.getenv("TIDB_PASSWORD")
            database = os.getenv("TIDB_DATABASE")
            ssl_ca = os.getenv("TIDB_SSL_CA")

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
            return connection

    except Error as e:
        print(f"TiDB connection error: {e}")

    return None    
    
    
  
