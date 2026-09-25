import streamlit as st
from playgrounds.streamlit_playground.state import init_state, sync_widget


init_state()

## Informazioni sui membri del reparto - INPUT & OUTPUT

nr_senior = st.number_input("How many seniors are there?", min_value=0, max_value=10, step=1, key = "_nr_senior", on_change = lambda: sync_widget("nr_senior"))


nr_junior = st.number_input("How many juniors are there?", min_value=0, max_value=10, step=1, key = "_nr_junior", on_change= lambda: sync_widget("nr_junior"))



if nr_senior == 1:
    st.write(f"In the team there is only one senior")
if nr_senior > 1:
    st.write(f"The seniors in the team are: {st.session_state._nr_senior}")

if nr_junior == 1:
    st.write("In the team there is only one junior")
if nr_junior > 1:
    st.write(f"The juniors in the team are: {st.session_state._nr_junior}")


