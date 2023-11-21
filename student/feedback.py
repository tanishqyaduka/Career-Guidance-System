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


def create_feedback_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS Feedback (
        Feedback_ID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
        Student_ID INT,
        Counsellor_ID INT,
        Comments VARCHAR(255) NOT NULL,
        Ratings INT,
        FOREIGN KEY (Student_ID) REFERENCES Users (Student_ID),
        FOREIGN KEY (Counsellor_ID) REFERENCES Counsellor (Counsellor_ID)
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


def insert_feedback(counsellor_id, ratings, comments):
    connection = create_connection()
    cursor = connection.cursor()

    query = (
        "INSERT INTO Feedback (Counsellor_ID, Ratings, Comments) VALUES (%s, %s, %s)"
    )
    cursor.execute(query, (counsellor_id, ratings, comments))

    connection.commit()

    cursor.close()
    connection.close()
