import streamlit as st

# Setting a dummy logged_in state for testing purposes. The login funcion is also the welcome page of the app. 
# The user will be able to log in and log out, and the navigation will change accordingly.

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():
    st.title(":red[WELCOME TO OUR SHIFTS GENERATOR APP!]")
    st.write("This is a first attempt at creating a draft of our app. It will be used to test some features and functions of Streamlit and get an idea of the " \
        "things we will need to implement.")

    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()


# Defining the pages of the app. Until  the users log in, he won't be able to access the other pages, even if he tries to navigate to them directly. 


login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

new_shift_page = st.Page("pages/new_shift.py", title="Create new shift", icon=":material/calendar_month:")
team_info = st.Page("pages/team_info.py", title="Team information", icon=":material/group:")


if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Account": [logout_page],
            "Shifts": [new_shift_page],
            "Team": [team_info]
        }
    )
else:
    pg = st.navigation([login_page])

pg.run()
