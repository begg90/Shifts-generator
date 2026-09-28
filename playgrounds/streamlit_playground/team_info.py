import streamlit as st
from playgrounds.streamlit_playground.state import load_value, store_value, check_and_initialize_state

check_and_initialize_state()
## Informazioni sui membri del reparto - INPUT & OUTPUT
if 'nr_senior' not in st.session_state:
    st.session_state.nr_senior = 0
else:
    load_value('nr_senior')
if 'nr_junior' not in st.session_state:
    st.session_state.nr_junior = 0
else:
    load_value('nr_junior')

nr_senior = st.number_input('How many seniors are there?', min_value=0, max_value=10, step=1, key = "_nr_senior", on_change = store_value, args = ['nr_senior'])

load_value('nr_junior')
nr_junior = st.number_input('How many juniors are there?', min_value=0, max_value=10, step=1, key = "_nr_junior", on_change = store_value, args = ['nr_junior'])


if nr_senior == 1:
    st.write('In the team there is only one senior')
if nr_senior > 1:
    st.write(f'The seniors in the team are: {st.session_state._nr_senior}')

if nr_junior == 1:
    st.write('In the team there is only one junior')
if nr_junior > 1:
    st.write(f'The juniors in the team are: {st.session_state._nr_junior}')


