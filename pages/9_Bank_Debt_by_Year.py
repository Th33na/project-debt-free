import streamlit as st
import pandas as pd
from utils.db_utils import get_relevant_transactions
import holoviews as hv
hv.extension('bokeh', logo=False)

st.set_page_config(
    page_title="Bank Information",
    page_icon="📊")

def display_plot(year):
    if 'year' in st.session_state:
        year = st.session_state["year"]

        plot = get_relevant_transactions(year=year)
        st.bokeh_chart(hv.render(plot, backend="bokeh"))
        st.session_state["user_id"] = user_id

if 'user_id' in st.session_state:
    user_id = st.session_state["user_id"]

    if user_id == "BANK":

        st.write(f"Hello, {user_id} employee, please select the year to view the User Debt for that year.")

        available_years = ["2016", "2017", "2018", "2019", "2020"]
        year = st.radio("Year Selection", available_years, horizontal=True)
        st.session_state["year"] = year
        display_plot(year)


    else:
        st.write("This is for Bank Employees only.")
        st.session_state["user_id"] = user_id
else:
    st.write("Please login to use the app")