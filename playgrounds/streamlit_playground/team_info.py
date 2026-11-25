"""This page allows the user to enter the information of the team members,
and displays the current list of team members in a table."""

import pandas as pd
import streamlit as st


def store_team_member():
    """Store the team member's name and role in the doctors list, with a
    check to make sure that both fields are completed correctly."""
    name = st.session_state["doctor_name"]
    role = st.session_state["doctor_role"]
    if role == "-" or name == "":
        st.warning("Please complete correctly both fields for the team member.")
        return
    st.session_state["doctors"].append([name, role])
    st.success(f"{role} {name} added successfully!")


def add_team_member():
    """Add a new team member, making sure that the form is cleared after
    submission, so that the user can add multiple team members."""
    with st.form("team_info_form", width="content", clear_on_submit=True):
        st.write("Please enter the name and the role of the team members:")
        st.text_input("Name", key="doctor_name")
        st.selectbox("Role", options=["-", "Senior", "Junior"], key="doctor_role")
        st.form_submit_button("Add to the team", on_click=store_team_member)


add_team_member()

st.write("Current team members:")
doctors_df = pd.DataFrame(st.session_state["doctors"], columns=["Name", "Role"])
st.dataframe(doctors_df)
