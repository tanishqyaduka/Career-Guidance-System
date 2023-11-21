import mysql.connector
from datetime import datetime


def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tanishq",
        database="dbms_project",
        auth_plugin="mysql_native_password",
    )
    return connection


def past_appointments(Student_ID):
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        query = """SELECT Appointment_ID,Counsellor_ID,Date,Start_Time FROM Appointments where Student_ID=%s"""
        cursor.execute(query, (Student_ID,))
        appointments = cursor.fetchall()

        return appointments

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

    finally:
        if "connection" in locals() and connection.is_connected():
            cursor.close()
            connection.close()


def get_datetime(appointment):
    date_str = appointment["Date"]
    time_str = appointment["Start_Time"]
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
