import streamlit as st

# Working on saving the state of the app, so that the user can navigate between pages without losing the data he has already entered.

def store_value(key):
    """Store the value of a widget in the session state- The temporary key is prefixed with an underscore to avoid conflicts with the persistent key, which is copied to 
    preserve its value between pages."""
    st.session_state[key] = st.session_state[f'_{key}']

def load_value(key):
    """Da chiamare come on_change per copiare _key -> key"""
    st.session_state[f'_{key}'] = st.session_state[key]


DEFAULT_STATE = {
    "nr_senior": 0,
    "nr_junior": 0,
    "chosen_year": 2026,
    "chosen_month": "January"
}

def check_and_initialize_state():
    """Check if the session state has been initialized, and if not, initialize it with the default values."""
    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value