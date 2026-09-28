import streamlit as st
from playgrounds.streamlit_playground.state import check_and_initialize_state, reset_state

# The entrypoint runs on every rerun, before the selected page: initializing here guarantees that every page finds the keys of DEFAULT_STATE.
check_and_initialize_state()


def login():
    st.title(':red[WELCOME TO OUR SHIFTS GENERATOR APP!]')
    st.write('This is a first attempt at creating a draft of our app. It will be used to test some features and functions of Streamlit and get an idea of the ' \
        'things we will need to implement.')

    if st.button('Log in'):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    
    st.write('You are now logged in. You can log out by clicking the button below. If you do so, the values you have entered in the previous pages will be reset to the default values'
    'if you didn\'t save them')
    if st.button('Log out'):
        reset_state() # this will reset all session states to DEFAULT, include the loggd_in one
        st.rerun()


# Defining the pages of the app. Until  the users log in, he won't be able to access the other pages, even if he tries to navigate to them directly. 

login_page = st.Page(login, title='Log in', icon=':material/login:')
logout_page = st.Page(logout, title='Log out', icon=':material/logout:')

new_shift_page = st.Page("new_shift.py", title='Create new shift', icon=':material/calendar_month:')
team_info = st.Page("team_info.py", title='Team information', icon=':material/group:')


if st.session_state.logged_in:
    pg = st.navigation(
        {
            'Account': [logout_page],
            'Shifts': [new_shift_page],
            'Team': [team_info]
        }
    )
else:
    pg = st.navigation([login_page])


pg.run()
