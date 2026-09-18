import streamlit as st
import pandas as pd
import calendar as cal


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


