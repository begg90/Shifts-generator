"""The home page for the app, or our entrypoint. It is responsible for initializing the session state,
since doing so guarantees that every page finds the keys of DEFAULT_STATE.
It also contains the login and logout functions, which are displayed depending on the value
of the logged_in key in the session state, and the other pages of the app, which are displayed
when the user is logged in."""

import streamlit as st

from ..streamlit_playground.state import (
    check_and_initialize_state,
    reset_state,
)

check_and_initialize_state()


def login():
    """Describes the login page, which is displayed when the user is not logged in."""
    st.title(":red[WELCOME TO OUR SHIFTS GENERATOR APP!]")
    st.write(
        "This is a first attempt at creating a draft of our app. It will be used to test some features "
        "and functions of Streamlit and get an idea of the things we will need to implement."
    )

    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()


def logout():
    """Describes the logout page, which is displayed when the user is logged in."""

    st.write(
        "You are now logged in. You can log out by clicking the button below. If you do so, the values you "
        "have entered in the previous pages will be reset to the default values if you didn't save them."
    )
    if st.button("Log out"):
        reset_state()
        st.rerun()


login_page = st.Page(login, title="Log in", icon=":material/login:")
logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

new_shift_page = st.Page("new_shift.py", title="Create new shift", icon=":material/calendar_month:")
team_info = st.Page("team_info.py", title="Team information", icon=":material/group:")


if st.session_state.logged_in:
    pg = st.navigation({"Account": [logout_page], "Shifts": [new_shift_page], "Team": [team_info]})
else:
    pg = st.navigation([login_page])


pg.run()
