import streamlit as st


if 'user_id' in st.session_state:
    del(st.session_state["user_id"])
    st.write("Logout successfull.")
    st.sidebar.success("Please login to use the system.")