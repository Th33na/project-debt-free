import pandas as pd
import streamlit as st
from db_utils import get_debt_free_db_engine, get_transaction_for_user_year

st.set_page_config(
    page_title="Debt Free 5.5% Interest Payment Plan",
    page_icon="📊") 
    
def payment_projection(debt, payment):
    # Reads in the debt and payment choice and returns the time and the last payment.
    APR = 0.055 / 12
    counter = 1

    while debt > payment:
        counter += 1
        debt = ((debt - payment) * APR) + (debt - payment)
        st.write(debt)

    final_payment = debt
    return counter, final_payment


def sum_of_debt(user_id):
    
    engine = get_debt_free_db_engine()
    transaction_2019 = get_transaction_for_user_year(engine, user_id, '2019')
    sumofdebt = transaction_2019["amount"].sum()
    return(sumofdebt)

if 'user_id' in st.session_state:
    user_id = st.session_state["user_id"]

    if user_id != "BANK":
        
        payment_amount = 0
        debt = sum_of_debt(user_id)
        time = 0
        st.write(f"Hello, {user_id}, you have chosen to pay off your debt with your own payment amount.")
        st.write(f"Your current total debt is ${debt: .2f}.")
        st.write("We currently have an APR on our payment plan of 5.5% with this option.")
        user_amount = st.text_input("Amount you wish to pay monthly:", "0.00")
        payment_amount = float(user_amount)
        
        if payment_amount > 0:
            time_pay = payment_projection(debt, payment_amount)
            time = time_pay[0] / 12
            st.write(f"It will take you {time: .2f} years to pay off this debt with a final payment of ${time_pay[1]: .2f} on the final month.")

        st.session_state["user_id"] = user_id

    else:
        st.write("Please use the BANK DEMO")
        st.session_state["user_id"] = user_id
else:
    st.write("Please login to use the app")