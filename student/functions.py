import streamlit as st
from user_authentication import *
from history import *
from feedback import *
from appointments import *
from datetime import datetime
from colleges import *
from career_options import *

Student_ID = None


def sign_up():
    st.title("Sign Up")
    st.write("Have an account! Head to the sign in page!! 🙋‍♂️")
    with st.form("signup_form"):
        name = st.text_input("Full Name:")
        email = st.text_input("Email:")
        password = st.text_input("Password:", type="password")
        mobile = st.text_input("Mobile Number:")

        submit_button = st.form_submit_button("Sign Up")

    if submit_button:
        if not all([name, email, password, mobile]):
            st.warning("Please fill all the required details.")
        elif if_user_exists(email):
            st.error("Email already exists. Please choose a different email.")
        else:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            insert_user(name, email, hashed_password, mobile)
            st.success(f"Account created for {email}. You can now sign in")


def set_sign_out():
    st.session_state["shared"] = False


def sign_out():
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")


def sign_in():
    global Student_ID
    st.title("Sign In")

    with st.form("signin_form"):
        email = st.text_input("Email:")
        password = st.text_input("Password", type="password")
        submit_button = st.form_submit_button("Sign In")
    st.write("Don't have an account? Head to the sign up page!! 🙋‍♂️")
    if submit_button:
        if not email or not password:
            st.warning("Please enter both email and password")
        else:
            user_data = authenticate_user(email, password)
            if user_data:
                st.success(f"Welcome, {email}")
                Student_ID = user_data[0]
                st.session_state["shared"] = True
            else:
                st.error("Invalid credentials! Try Again")

    signout_button = st.button("Sign Out", key="Sign Out")
    if signout_button:
        set_sign_out()
        st.write("Please sign In again to continue using the app!!")


def history():
    st.title("Appointment History")

    appointments = past_appointments(Student_ID)
    current_datetime = datetime.now()

    if not appointments:
        st.warning("No appointments found.")
    else:
        previous_appointments = [
            appointment
            for appointment in appointments
            if get_datetime(appointment) < current_datetime
        ]
        upcoming_appointments = [
            appointment
            for appointment in appointments
            if get_datetime(appointment) >= current_datetime
        ]
        if upcoming_appointments:
            st.header("Upcoming Appointments")
            st.table(upcoming_appointments)
        else:
            st.info("No upcoming appointments found.")

        if previous_appointments:
            st.header("Previous Appointments")
            st.table(previous_appointments)
        else:
            st.info("No previous appointments found.")


def feedback():
    st.title("Feedback Form")
    st.write("Give feedback and help us improve your experience")
    with st.form("feedback_form"):
        counsellor_id = st.text_input("Counsellor ID:")
        ratings = st.number_input(
            "Ratings out of 10:", min_value=0, max_value=10, step=1
        )
        comments = st.text_area("Comments:")

        submit_button = st.form_submit_button("Submit")

    if submit_button:
        if counsellor_id and ratings is not None:
            insert_feedback(counsellor_id, ratings, comments)
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please fill in all required fields.")


def appointments():
    st.title("Counselor Appointments")

    st.header("Counselors")
    counselors = get_counselors()
    st.table(counselors)

    st.header("Set Appointment")
    selected_counselor = st.selectbox(
        "Select Counselor", counselors, format_func=lambda x: x["Counsellor_Name"]
    )

    current_date = datetime.now().date()
    date = st.date_input("Select Date", min_value=current_date)
    time_slots = generate_time_slots()
    current_time = datetime.now().time()
    start_time = st.selectbox(
        "Select Start Time",
        [time for time in time_slots if datetime.combine(date, time) >= datetime.now()],
    )

    if st.button("Set Appointment"):
        selected_datetime = datetime.combine(date, start_time)
        if selected_datetime < datetime.now():
            st.error(
                "Selected date and time cannot be earlier than the current date and time."
            )
        else:
            counselor_id = selected_counselor["Counsellor_ID"]
            try:
                set_appointment(Student_ID, counselor_id, date, start_time)
                st.success("Appointment set successfully!")
            except mysql.connector.Error as err:
                if err.errno == 1644:
                    st.error(
                        "Appointment slot already booked for the selected date and time."
                    )
                else:
                    st.error(f"Error: {err}")


def colleges():
    colleges = get_colleges()
    st.title("List of Colleges")
    if st.button("Toggle Filters", key="1"):
        show_filters = not st.session_state.get("show_filters", False)
        st.session_state.show_filters = show_filters

    if st.session_state.get("show_filters", False):
        st.write("### Filters")

        ranking_filter = st.number_input("Filter by Ranking:")
        sort_order = st.radio(
            "Sort Order:", ["None", "Lowest to Highest", "Highest to Lowest"], key="3"
        )

        sort_mapping = {
            "None": "",
            "Lowest to Highest": "ASC",
            "Highest to Lowest": "DESC",
        }
        sort_order_sql = sort_mapping.get(sort_order, "")

        colleges = get_colleges(sort_order_sql)
        if st.button("Clear Filters"):
            st.session_state.show_filters = False
            st.experimental_rerun()

    else:
        colleges = get_colleges()

    if not colleges:
        st.warning("No colleges found.")
    else:
        st.table(colleges)


def career_options():
    st.title("Career Options")

    if st.button("Toggle Filters", key="2"):
        show_filters = not st.session_state.get("show_filters", False)
        st.session_state.show_filters = show_filters

    if st.session_state.get("show_filters", False):
        st.write("### Filters")

        sort_order = st.radio(
            "Filter by Salary:",
            ["None", "Lowest to Highest", "Highest to Lowest"],
            key="4",
        )

        sort_mapping = {
            "None": "",
            "Lowest to Highest": "ASC",
            "Highest to Lowest": "DESC",
        }
        sort_order_sql = sort_mapping.get(sort_order, "")

        career_options = get_career_options(sort_order_sql)
        if st.button("Clear Filters"):
            st.session_state.show_filters = False
            st.experimental_rerun()

    else:
        career_options = get_career_options()

    if not career_options:
        st.warning("No career options found.")
    else:
        st.table(career_options)
