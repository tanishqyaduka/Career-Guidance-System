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


def create_career_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS career_options (
        Career_ID INT AUTO_INCREMENT PRIMARY KEY,
        Job_Title VARCHAR(255),
        Education VARCHAR(255),
        Description TEXT,
        Industries VARCHAR(255),
        Salary DECIMAL(10, 2)
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


def get_career_options(sort_order=None):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM career_options WHERE 1"

    if sort_order:
        query += f" ORDER BY Salary {sort_order}"

    cursor.execute(query)
    career_options = cursor.fetchall()

    cursor.close()
    connection.close()

    return career_options


def get_unique_industries():
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT DISTINCT Industries FROM career_options"
    cursor.execute(query)
    industries = [row[0] for row in cursor.fetchall()]

    cursor.close()
    connection.close()

    return industries
