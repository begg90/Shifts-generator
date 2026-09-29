import streamlit as st
from playgrounds.streamlit_playground.state import persistent_widget


## Informazioni sui membri del reparto - INPUT & OUTPUT

nr_senior = persistent_widget(
    st.number_input, 'How many seniors are there?', 'nr_senior',
    min_value=0, max_value=10, step=1)

nr_junior = persistent_widget(
    st.number_input, 'How many juniors are there?', 'nr_junior',
    min_value=0, max_value=10, step=1)



if nr_senior == 1:
    st.write('In the team there is only one senior')
if nr_senior > 1:
    st.write(f'The seniors in the team are: {st.session_state._nr_senior}')

if nr_junior == 1:
    st.write('In the team there is only one junior')
if nr_junior > 1:
    st.write(f'The juniors in the team are: {st.session_state._nr_junior}')
