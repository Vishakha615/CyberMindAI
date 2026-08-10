from mysql_connection import get_connection


connection = get_connection()


if connection:
    print("✅ TiDB Cloud connection successful!")
    connection.close()
else:
    print("❌ TiDB Cloud connection failed!")