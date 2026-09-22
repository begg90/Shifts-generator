import streamlit as st
import pandas as pd
import calendar as cal


## Calendario - INPUT & OUTPUT

mesi = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

with st.form("date_form"):

    st.write("Select the month and year you want to work on")

    d_year = st.selectbox("Select the year you are interested in", options = list(range(2026, 2036)), index=0, key = "d_year")
    d_month = st.selectbox("Select the month you are interested in", options = mesi, index=None, key = "d_month")

    submitted = st.form_submit_button("OK")

if submitted:
    index_month = mesi.index(st.session_state.d_month) + 1

    st.write(f"The month you want to work on is: {st.session_state.d_month} {st.session_state.d_year}")
    calendar = cal.monthcalendar(int(st.session_state.d_year), index_month)
    st.table(calendar)