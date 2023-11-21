import streamlit as st
from functions import *

create_user_table()
create_appointments_table()
create_feedback_table()
create_college_table()
create_career_table()

menu = [
    "Home",
    "Sign Up",
    "Sign In",
    "Appointments",
    "Book an Appointment",
    "Colleges",
    "Career Options",
    "Feedback",
]

tab = st.tabs(menu)

with tab[0]:
    st.title("Career Guidance System")

with tab[1]:
    sign_up()

with tab[2]:
    sign_in()

with tab[3]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"] == False:
        st.write("Signed Out")
    else:
        history()

with tab[4]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"] == False:
        st.write("Signed Out")
    else:
        appointments()

with tab[5]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"] == False:
        st.write("Signed Out")
    else:
        colleges()

with tab[6]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"] == False:
        st.write("Signed Out")
    else:
        career_options()

with tab[7]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"] == False:
        st.write("Signed Out")
    else:
        feedback()
