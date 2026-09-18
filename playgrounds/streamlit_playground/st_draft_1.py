import streamlit as st


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Welcome message on the home page

st.title(":red[WELCOME TO OUR SHIFTS GENERATOR APP!]")

st.write("This is a first attempt at creating a draft of our app. It will be used to test some features and functions of Streamlit and get an idea of the " \
        "things we will need to implement.")


def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()

def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()


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



