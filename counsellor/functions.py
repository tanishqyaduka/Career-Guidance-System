import streamlit as st
from user_authentication import *
from feedback import *
from appointments import *

Counsellor_ID = None


def sign_up():
    st.title("Sign Up")
    st.write("Have an account! Head to the sign in page!! 🙋‍♂️")
    with st.form("signup_form"):
        name = st.text_input("Full Name:")
        email = st.text_input("Email:")
        password = st.text_input("Password:", type="password")
        mobile = st.text_input("Mobile Number:")
        qualifications = st.text_input("Qualifications:")
        experience = st.text_input("Experience:")
        fees = st.text_input("Fees:")

        submit_button = st.form_submit_button("Sign Up")

    if submit_button:
        if not all([name, email, password, mobile, qualifications, experience, fees]):
            st.warning("Please fill all the required details.")
        elif if_user_exists(email):
            st.error("Email already exists. Please choose a different email.")
        else:
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
            insert_user(
                name, email, hashed_password, mobile, qualifications, experience, fees
            )
            st.success(f"Account created for {email}. You can now sign in")


def set_sign_out():
    st.session_state["shared"] = False


def sign_out():
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")


def sign_in():
    global Counsellor_ID
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
                Counsellor_ID = user_data[0]
                st.session_state["shared"] = True
            else:
                st.error("Invalid credentials! Try Again")

    signout_button = st.button("Sign Out", key="Sign Out")
    if signout_button:
        set_sign_out()
        st.write("Please sign In again to continue using the app!!")


def feedback():
    st.title("Feedbacks")

    feedbacks = feedback_recieved(Counsellor_ID)

    if not feedbacks:
        st.warning("No appointments found.")
    else:
        st.table(feedbacks)


def appointments():
    st.title("Previous Appointments")

    appointments = past_appointments(Counsellor_ID)

    if not appointments:
        st.warning("No appointments found.")
    else:
        st.table(appointments)
