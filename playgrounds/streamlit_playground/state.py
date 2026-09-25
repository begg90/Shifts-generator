import streamlit as st

# Working on saving the state of the app, so that the user can navigate between pages without losing the data he has already entered.

DEFAULTS = {
    "nr_senior": 0,
    "nr_junior": 0,
}

def init_state():
    for key, default in DEFAULTS.items():
        st.session_state.setdefault(key, default)

def sync_widget(persistent_key):
    """Da chiamare come on_change per copiare _key -> key"""
    st.session_state[persistent_key] = st.session_state[f"_{persistent_key}"]