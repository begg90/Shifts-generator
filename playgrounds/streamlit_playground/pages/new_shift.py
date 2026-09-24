import streamlit as st
import pandas as pd
import calendar as cal

## Calendario - INPUT & OUTPUT

mesi = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

with st.form("date_form"):

    st.write("Select the month and year you want to work on")

    chosen_year = st.selectbox("Select the year you are interested in", options = list(range(2026, 2036)), index=0, key = "chosen_year")
    chosen_month = st.selectbox("Select the month you are interested in", options = mesi, index=None, key = "chosen_month")

    submitted = st.form_submit_button("OK")

if submitted:
    index_month = mesi.index(st.session_state.chosen_month) + 1

    st.write(f"The month you want to work on is: {st.session_state.chosen_month} {st.session_state.chosen_year}")
    calendar = cal.monthcalendar(int(st.session_state.chosen_year), index_month)
    st.table(calendar)
