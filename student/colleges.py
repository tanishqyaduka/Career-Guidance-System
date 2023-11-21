import streamlit as st
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


def create_college_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS college (
        College_ID INT AUTO_INCREMENT PRIMARY KEY,
        College_Name VARCHAR(255) NOT NULL,
        Website VARCHAR(255),
        Ranking INT,
        Courses VARCHAR(255),
        Entrance_Exams VARCHAR(255),
        Type SET('undergraduate', 'postgraduate') NOT NULL
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


def get_unique_courses():
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT Courses FROM college"
    cursor.execute(query)
    courses = [course[0] for course in cursor.fetchall()]

    cursor.close()
    connection.close()

    return courses


def get_colleges(sort_order=None):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM college WHERE 1"

    if sort_order:
        query += f" ORDER BY Ranking {sort_order}"

    cursor.execute(query)
    colleges = cursor.fetchall()

    cursor.close()
    connection.close()

    return colleges
