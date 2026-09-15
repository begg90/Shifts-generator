import streamlit as st

st.write("This is a first attempt at creating a draft of our app. It will be used to test some features and functions of Streamlit and get an idea of the " \
        "things we will need to implement.")

st.title(":red[WELCOME TO OUR SHIFTS GENERATOR APP!]")

st.write('Do you want to create a new shift?')
if st.button('Yes'):
    st.write('You clicked Yes!')

pg = st.navigation([st.Page("pages/page_1.py"), st.Page("pages/page_2.py")], position="hidden")
pg.run()