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


def create_user_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS users (
        Student_ID INT AUTO_INCREMENT PRIMARY KEY,
        Student_Name VARCHAR(255) NOT NULL,
        Email VARCHAR(255) NOT NULL,
        Password VARCHAR(255) NOT NULL,
        Mobile VARCHAR(15),
        Registration_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


def if_user_exists(email):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM USERS WHERE Email= %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None


def insert_user(name, email, password, mobile):
    connection = create_connection()
    cursor = connection.cursor()

    query = "INSERT INTO users (Student_Name, Email, Password, Mobile) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, email, password, mobile))

    connection.commit()

    cursor.close()
    connection.close()


def authenticate_user(email, password):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT Student_ID,Password FROM users WHERE Email = %s"
    cursor.execute(query, (email,))

    user_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if user_data:
        stored_password = user_data[1].encode("utf-8")
        if bcrypt.checkpw(password.encode("utf-8"), stored_password):
            return user_data[0], user_data
    return None
