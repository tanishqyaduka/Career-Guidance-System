import mysql.connector
import streamlit as st
import bcrypt


def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tanishq",
        database="dbms_project",
        auth_plugin="mysql_native_password",
    )
    return connection


def create_counsellor_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS Counsellor (
        Counsellor_ID INT AUTO_INCREMENT PRIMARY KEY,
        Counsellor_Name VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL,
        Mobile VARCHAR(15) NOT NULL,
        Qualifications VARCHAR(255) NOT NULL,
        Experiences VARCHAR(255) NOT NULL,
        Fees DECIMAL(10, 2),
        Password VARCHAR(255) NOT NULL
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


def if_user_exists(email):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM Counsellor WHERE Email= %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None


def insert_user(name, email, password, mobile, qualifications, experience, fees):
    connection = create_connection()
    cursor = connection.cursor()

    query = "INSERT INTO Counsellor (Counsellor_Name, Email, Password, Mobile, Qualifications,Experiences,Fees) VALUES (%s, %s, %s, %s,%s, %s, %s)"
    cursor.execute(
        query, (name, email, password, mobile, qualifications, experience, fees)
    )

    connection.commit()

    cursor.close()
    connection.close()


def authenticate_user(email, password):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT Counsellor_ID,Password FROM Counsellor WHERE Email = %s"
    cursor.execute(query, (email,))

    user_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if user_data:
        stored_password = user_data[1].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), stored_password):
            return user_data[0], user_data
    return None
