import streamlit as st


st.set_page_config(
    page_title="Welcome!",
    page_icon="👋",
)

# Welcome message on the home page

st.title(":red[WELCOME TO OUR SHIFTS GENERATOR APP!]")

st.write("This is a first attempt at creating a draft of our app. It will be used to test some features and functions of Streamlit and get an idea of the " \
        "things we will need to implement.")


# Working on the sidebar & navigation menu

st.sidebar.info('What would you like to do?')


new_shift_page = st.Page("pages/page_1.py", title="New Shift")
pg = st.navigation([new_shift_page])