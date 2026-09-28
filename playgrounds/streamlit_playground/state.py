import streamlit as st

# Working on saving the state of the app, so that the user can navigate between pages without losing the data he has already entered.

def store_value(key):
    """Store the value of a widget in the session state -> on_change callback: copy the temporary widget's value (_key) into the persistent one (key)."""
    st.session_state[key] = st.session_state[f'_{key}']

def load_value(key):
    """Calling this function will load the saved value of a widget -> on_change callback: so the user can navigate between pages without losing the data."""
    st.session_state[f'_{key}'] = st.session_state[key]

def persistent_widget(widget, label, key, **kwargs):
    """Create a widget whose value survives page changes."""
    load_value(key)
    return widget(label, key=f'_{key}', on_change=store_value, args=[key], **kwargs)


DEFAULT_STATE = {
    'logged_in': False,
    'nr_senior': 0,
    'nr_junior': 0,
    'chosen_year': 2026,
    'chosen_month': 'January'
}

def check_and_initialize_state():
    """Check if the session state has been initialized, and if not, initialize it with the default values."""
    for key, value in DEFAULT_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_state():
    """Reset the session state to the default values."""
    for key, value in DEFAULT_STATE.items():
        st.session_state[key] = value