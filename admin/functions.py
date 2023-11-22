import streamlit as st
from students import *
from counsellors import *
from appointments import *


def students():
    st.title("Students")

    student = all_students()

    if not student:
        st.warning("No students found.")
    else:
        st.table(student)


def counsellors():
    st.title("Counsellors")

    counsellor = all_counsellors()

    if not counsellor:
        st.warning("No counsellors found.")
    else:
        st.table(counsellor)


def appointments():
    st.title("Appointment Information")

    appointments = get_appointments_data()
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
