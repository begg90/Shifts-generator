import streamlit as st
import pandas as pd


## Informazioni sui membri del reparto - INPUT & OUTPUT

def store_team_member():
    
    """Store the team member's name and role in the doctors list."""
    name = st.session_state['doctor_name']
    role = st.session_state['doctor_role'] 
    if role == '-' or name == '':                           # Check that both fields are filled correctly before adding to the list
        st.warning('Please complete correctly both fields for the team member.')
        return
    else:                                                   # Store the updated list in session state
        st.session_state['doctors'].append([name, role])    
        st.success(f'{role} {name} added successfully!')

def add_team_member():
    """Add a new team member."""
    with st.form('team_info_form', width='content', clear_on_submit=True):          # Make sure that the form is cleared after submission, so that the user can add multiple team members 
        st.write('Please enter the name and the role of the team members:')
        st.text_input('Name', key='doctor_name')
        st.selectbox('Role', options=['-', 'Senior', 'Junior'], key='doctor_role')  # Just this three roles for now 
        st.form_submit_button('Add to the team', on_click=store_team_member)        # Clicking the button will trigger the store_team_member function, which will store the values in the session state

add_team_member()   # initalize the form to add team members 

st.write('Current team members:')
doctors_df = pd.DataFrame(st.session_state['doctors'], columns=['Name', 'Role'])    # Create a DataFrame from the list of doctors stored in the session state, easy to save in the future 
st.dataframe(doctors_df)  # Display the DataFrame as a table

