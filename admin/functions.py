import streamlit as st
from students import *
from counsellors import *
from appointments import *


def students():
    st.title("Feedbacks")

    student = all_students()

    if not student:
        st.warning("No students found.")
    else:
        st.table(student)


def counsellors():
    st.title("Feedbacks")

    counsellor = all_counsellors()

    if not counsellor:
        st.warning("No counsellors found.")
    else:
        st.table(counsellor)


def appointments():
    st.title("Appointment Information")

    appointments_data = get_appointments_data()

    if not appointments_data:
        st.warning("No appointments found.")
    else:
        st.table(appointments_data)
