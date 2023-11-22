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


def past_appointments(Counsellor_ID):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = """SELECT Appointment_ID,Student_ID,Date,Start_Time FROM Appointments where Counsellor_ID=%s"""
    cursor.execute(query, (Counsellor_ID,))
    appointments = cursor.fetchall()

    cursor.close()
    connection.close()

    return appointments


def get_datetime(appointment):
    date_str = appointment["Date"]
    time_str = appointment["Start_Time"]
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
