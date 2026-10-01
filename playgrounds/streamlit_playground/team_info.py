import streamlit as st
import pandas as pd


## Informazioni sui membri del reparto - INPUT & OUTPUT

def store_team_member(name, role):
    """Store the team member's name and role in the doctors list."""
    st.session_state['doctors'].append([name, role])   # Store the updated list in session state
    st.success(f'{role} {name} added successfully!')

def add_team_member():
    """Add a new team member."""
    with st.form('team_info_form', width='content', clear_on_submit=True):
        st.write('Please enter the name and the role of the team members:')
        name = st.text_input('Name', key='doctor_name')
        role = st.selectbox('Role', options=['-', 'Senior', 'Junior'], key='doctor_role')
        st.form_submit_button('Add to the team', on_click=store_team_member, args=(name, role))

add_team_member()   # initalize the form to add team members 

st.write('Current team members:')
doctors_df = pd.DataFrame(st.session_state['doctors'], columns=['Name', 'Role'])
st.dataframe(doctors_df)  # Display the DataFrame as a table

