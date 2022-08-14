import streamlit as st
from streamlit_multipage import MultiPage

from utils.auth_utils import login


st.set_page_config(
    page_title="Welcome",
    page_icon="👋",   
)

st.write("Welcome to Project Debt Free")
st.write("Please login to use the app")

st.text_input("User ID", key="user_id")
user_id = st.session_state.user_id

if user_id:
    output = login(user_id)

    if output:
        if output["status"] == "404":
            st.write(output["error_message"])
        else:
            st.write("Please select a flow")
            if user_id.upper() == 'BANK':
                st.sidebar.success("Select a BANK DEMO above.")
            else:
                st.sidebar.success("Select a USER DEMO above.")


