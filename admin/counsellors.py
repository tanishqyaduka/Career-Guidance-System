import mysql.connector


def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tanishq",
        database="dbms_project",
        auth_plugin="mysql_native_password",
    )
    return connection


def all_counsellors():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = """SELECT * FROM Counsellor"""
    cursor.execute(query)
    payments = cursor.fetchall()

    cursor.close()
    connection.close()

    return payments
