import pandas as pd
import streamlit as st
from utils.db_utils import get_relevant_transactions

# Generates payment plan to show how long it takes to pay off their debt
st.set_page_config(
    page_title="Debt Free 5.5% Interest Payment Plan",
    page_icon="📊") 

# Calculation function with 5.5 percent interest per month    
def payment_projection(debt, payment):
    # Reads in the debt and payment choice and returns the time and the last payment.
    APR = 0.055 / 12
    counter = 1

    while debt > payment:
        counter += 1
        debt = ((debt - payment) * APR) + (debt - payment)
        
    final_payment = debt
    return counter, final_payment

# Calculation of the total debt amount from 2019
def sum_of_debt(user_id):
    
    transaction_2019 = get_relevant_transactions(user_id=user_id, year='2019')
    sumofdebt = transaction_2019["amount"].sum()
    return(sumofdebt)

# Streamlit User interface with output of the result based on user's input
if 'user_id' in st.session_state:
    user_id = st.session_state["user_id"]

    if user_id != "BANK":
        
        payment_amount = 0
        debt = sum_of_debt(user_id)
        time = 0
        st.write(f"Hello, {user_id}, you have chosen to pay off your 2019 debt with your own payment amount.")
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