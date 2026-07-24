import streamlit as st
import pandas as pd
import calendar as cal


st.write("This is a first attempt at creating a draft of our app. It will be used to test some features and functions of Streamlit and get an idea of the " \
        "things we will need to implement.")

st.title("User inputs")


## Informazioni sui membri del reparto - INPUT & OUTPUT

nr_senior = st.number_input("Quanti senior ci sono in reparto?", min_value=0, max_value=10, step=1, key = "nr_senior")
if nr_senior == 1:
    st.text_input("Scrivi il suo nome", key = "senior_name")
if nr_senior > 1:
    st.text_input("Scrivi i loro nomi separati da una virgola", key = "senior_names")

nr_junior = st.number_input("Quanti junior ci sono in reparto?", min_value=0, max_value=10, step=1, key = "nr_junior")
if nr_junior == 1:
    st.text_input("Scrivi il suo nome", key = "junior_name")
if nr_junior > 1:
    st.text_input("Scrivi i loro nomi separati da una virgola", key = "junior_names")


if nr_senior == 1:
    st.write(f"Nel reparto c'è un solo senior")
if nr_senior > 1:
    st.write(f"I senior in reparto sono: {st.session_state.nr_senior}")

if nr_junior == 1:
    st.write("Nel reparto c'è un solo junior")
if nr_junior > 1:
    st.write(f"I junior in reparto sono: {st.session_state.nr_junior}")



## Calendario - INPUT & OUTPUT

mesi = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"]

with st.form("date_form"):

    st.write("Seleziona il mese e l'anno su cui lavorare")

    d_year = st.selectbox("Seleziona l'anno che ti interessa", options = list(range(2026, 2036)), index=0, key = "d_year")
    d_month = st.selectbox("Seleziona il mese che ti interessa", options = mesi, index=None, key = "d_month")

    submitted = st.form_submit_button("OK")

if submitted:
    index_month = mesi.index(st.session_state.d_month) + 1

    st.write(f"Il mese su cui lavorare è: {st.session_state.d_month} {st.session_state.d_year}")
    calendar = cal.monthcalendar(int(st.session_state.d_year), index_month)
    st.table(calendar)
 