import streamlit as st
import pandas as pd
import calendar as cal


st.write("This is a first attempt at creating a draft of our app. It will be used to test some features and functions of Streamlit and get an idea of the " \
        "things we will need to implement.")

st.title("User inputs")


## Informazioni sui membri del reparto - INPUT & OUTPUT

nr_senior = st.number_input("How many seniors are there?", min_value=0, max_value=10, step=1, key = "nr_senior")
if nr_senior == 1:
    st.text_input("Write their name", key = "senior_name")
if nr_senior > 1:
    st.text_input("Write their names separated by a comma", key = "senior_names")

nr_junior = st.number_input("How many juniors are there?", min_value=0, max_value=10, step=1, key = "nr_junior")
if nr_junior == 1:
    st.text_input("Write their name", key = "junior_name")
if nr_junior > 1:
    st.text_input("Write their names separated by a comma", key = "junior_names")


if nr_senior == 1:
    st.write(f"In the team there is only one senior")
if nr_senior > 1:
    st.write(f"The seniors in the team are: {st.session_state.nr_senior}")

if nr_junior == 1:
    st.write("In the team there is only one junior")
if nr_junior > 1:
    st.write(f"The juniors in the team are: {st.session_state.nr_junior}")



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