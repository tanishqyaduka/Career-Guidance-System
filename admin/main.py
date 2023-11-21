import streamlit as st
from functions import *

menu = ["Home", "Students", "Counsellors", "Appointments"]

tab = st.tabs(menu)

with tab[0]:
    st.title("Admin Page")

with tab[1]:
    students()

with tab[2]:
    counsellors()

with tab[3]:
    appointments()
