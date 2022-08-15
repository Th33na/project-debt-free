import streamlit as st

from utils.db_utils import get_available_txn_years, get_available_cards
from user_cc_balance import get_cc_balance_user_for_cards



MONTHS = ['01', '02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

st.set_page_config(
    page_title="User Credit Card Balance",
    page_icon="📊",   
)

if 'user_id' in st.session_state:
    user_id = st.session_state["user_id"]

    if user_id != "BANK":

        st.write("Hello, User " + str(user_id) + "!!! Please select a year, month, and card you want to see.")
        available_years = get_available_txn_years(user_id=user_id)
        year = st.radio("Year Selection", available_years, horizontal=True)
        month = st.radio("Month Selection", MONTHS, horizontal=True)
        available_cards = get_available_cards(user_id, year)
        card = st.radio("Card Selection", available_cards, horizontal=True)
        balance = get_cc_balance_user_for_cards(user_id, year, month, int(card))   
        st.write(balance)

    else:
        st.write("Please use the BANK DEMO")
        st.session_state["user_id"] = user_id
else:
    st.write("Please login to use the app")