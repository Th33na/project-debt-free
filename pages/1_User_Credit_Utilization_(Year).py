import streamlit as st
from user_cc_utilization import get_cc_utilization_plot_for_user_for_cards
from utils.db_utils import get_available_txn_years
import holoviews as hv
hv.extension('bokeh', logo=False)

st.set_page_config(
    page_title="User Credit Utilization",
    page_icon="📊",   
)

def display_plot(user_id):
    if 'year' in st.session_state:
        year = st.session_state["year"]
        plot = get_cc_utilization_plot_for_user_for_cards(user_id, year)
        st.bokeh_chart(hv.render(plot, backend="bokeh"))
        st.session_state["user_id"] = user_id

if 'user_id' in st.session_state:
    user_id = st.session_state["user_id"]

    if user_id != "BANK":

        st.write("Hello, User " + str(user_id) + "!!! Please select a year you want to see.")

        available_years = get_available_txn_years(user_id=user_id)
        year = st.radio("Year Selection", available_years, horizontal=True)
        st.session_state["year"] = year
        display_plot(user_id)


    else:
        st.write("Please use the BANK DEMO")
else:
    st.write("Please login to use the app")


