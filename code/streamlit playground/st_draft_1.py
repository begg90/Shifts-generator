import streamlit as st
import pandas as pd


st.write("This is a first attempt at creating a draft of our app. It will be used to test some features and functions of Streamlit and get an idea of the things we will need to implement.")

### Sidebar for user inputs

st.sidebar.title("User inputs")

nr_senior = st.sidebar.number_input("Quanti senior ci sono in reparto?", min_value=0, max_value=10, step=1, key = "nr_senior")
if nr_senior == 1:
    st.sidebar.text_input("Scrivi il suo nome", key = "senior_name")
if nr_senior > 1:
    st.sidebar.text_input("Scrivi i loro nomi separati da una virgola", key = "senior_names")

nr_junior = st.sidebar.number_input("Quanti junior ci sono in reparto?", min_value=0, max_value=10, step=1, key = "nr_junior")
if nr_junior == 1:
    st.sidebar.text_input("Scrivi il suo nome", key = "junior_name")
if nr_junior > 1:
    st.sidebar.text_input("Scrivi i loro nomi separati da una virgola", key = "junior_names")


d_month = st.sidebar.selectbox("Seleziona il mese che ti interessa", options = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"], index=None,key = "d_month")
d_year = st.sidebar.selectbox("Seleziona l'anno che ti interessa", options = [2026,2027,2028,2029,2030,2031,2032,2033,2034,2035,2036], index=0, key = "d_year")



### Main page for outputs

if nr_senior == 1:
    st.write(f"Nel reparto c'è un solo senior")
if nr_senior > 1:
    st.write(f"I senior in reparto sono: {st.session_state.nr_senior}")

if nr_junior == 1:
    st.write("Nel reparto c'è un solo junior")
if nr_junior > 1:
    st.write(f"I junior in reparto sono: {st.session_state.nr_junior}")


   