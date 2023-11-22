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


def get_appointments_data():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("DROP PROCEDURE IF EXISTS GetAppointmentData")

    query = """
CREATE PROCEDURE GetAppointmentData()
BEGIN
    SELECT
        A.Date,
        A.Start_Time,
        A.Appointment_ID,
        A.Student_ID,
        U.Student_Name,
        U.Email AS Student_Email,
        U.Mobile AS Student_Mobile,
        A.Counsellor_ID,
        C.Counsellor_Name,
        C.Email AS Counsellor_Email,
        C.Mobile AS Counsellor_Mobile,
        C.Fees,
        COUNT(A.Appointment_ID) AS TotalAppointmentsForStudent,
        (
            SELECT COUNT(Appointment_ID)
            FROM Appointments
            WHERE Counsellor_ID = A.Counsellor_ID
        ) AS TotalAppointmentsForCounselor
    FROM Appointments A
    INNER JOIN Users U ON A.Student_ID = U.Student_ID
    INNER JOIN Counsellor C ON A.Counsellor_ID = C.Counsellor_ID
    GROUP BY A.Appointment_ID, A.Student_ID, U.Student_Name, U.Email, U.Mobile,
             A.Counsellor_ID, C.Counsellor_Name, C.Email, C.Mobile,
             A.Date, A.Start_Time, C.Fees;
END
    """

    cursor.execute(query)
    cursor.callproc("GetAppointmentData")

    for result in cursor.stored_results():
        appointments_data = result.fetchall()

    cursor.close()
    connection.close()

    return appointments_data


def get_datetime(appointment):
    date_str, time_str = appointment[:2]
    return datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M:%S")
