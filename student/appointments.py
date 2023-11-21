import mysql.connector
from datetime import datetime, timedelta


def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tanishq",
        database="dbms_project",
        auth_plugin="mysql_native_password",
    )
    return connection


def create_appointments_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS Appointments (
        Appointment_ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        Student_ID INT,
        Counsellor_ID INT,
        Date DATE NOT NULL,
        Start_Time VARCHAR(255) NOT NULL,
        CONSTRAINT uc_appointment UNIQUE (Counsellor_ID, Date, Start_Time),
        FOREIGN KEY (Student_ID) REFERENCES Users (Student_ID),
        FOREIGN KEY (Counsellor_ID) REFERENCES Counsellor (Counsellor_ID)
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


def get_counselors():
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT Counsellor_ID,Counsellor_Name,Email,Mobile,Qualifications,Experiences,Fees FROM Counsellor"
    cursor.execute(query)
    counselors = cursor.fetchall()

    cursor.close()
    connection.close()

    return counselors


def set_appointment(student_id, counselor_id, date, start_time):
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    INSERT INTO Appointments (Student_ID, Counsellor_ID, Date, Start_Time)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (student_id, counselor_id, date, start_time))

    connection.commit()

    cursor.close()
    connection.close()


def generate_time_slots():
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("17:00", "%H:%M")
    time_slots = []

    current_time = start_time
    while current_time <= end_time:
        time_slots.append(current_time.time())
        current_time += timedelta(hours=1)

    return time_slots


def same_booking_trigger():
    connection = create_connection()
    cursor = connection.cursor()

    trigger = """
    DELIMITER //

CREATE TRIGGER before_insert_appointment
BEFORE INSERT ON Appointments
FOR EACH ROW
BEGIN
    DECLARE existing_appointment INT;

    SELECT COUNT(*)
    INTO existing_appointment
    FROM Appointments
    WHERE Counsellor_ID = NEW.Counsellor_ID
      AND Date = NEW.Date
      AND Start_Time = NEW.Start_Time;

    IF existing_appointment > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Appointment slot already booked for the selected date and time.';
    END IF;
END //

DELIMITER ;
    """

    cursor.execute(trigger)
    connection.commit()

    cursor.close()
    connection.close()
