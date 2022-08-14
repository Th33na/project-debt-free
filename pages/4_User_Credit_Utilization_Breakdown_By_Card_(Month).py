import streamlit as st
from user_cc_utilization import get_cc_utilization_plots_for_user_per_card
from utils.db_utils import get_available_txn_years
import holoviews as hv
hv.extension('bokeh', logo=False)

MONTHS = ['01', '02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

def display_plot(user_id):
    if 'year' in st.session_state:
        year = st.session_state["year"]
        month = st.session_state["month"]
        plots = get_cc_utilization_plots_for_user_per_card(user_id, year, month=month)
        for plot in plots: 
            st.bokeh_chart(hv.render(plot, backend="bokeh"))
            st.session_state["user_id"] = user_id


if 'user_id' in st.session_state:
    user_id = st.session_state["user_id"]

    if user_id != "BANK":

        st.write("Hello, User " + str(user_id) + "!!! Please select a year and month you want to see")

        available_years = get_available_txn_years(user_id=user_id)
        year = st.radio("Year Selection", available_years, horizontal=True)
        st.session_state["year"] = year

        month = st.radio("Year Selection", MONTHS, horizontal=True)
        st.session_state["month"] = month
        display_plot(user_id)


    else:
        st.write("Please use the BANK DEMO")
else:
    st.write("Please login to use the app")


