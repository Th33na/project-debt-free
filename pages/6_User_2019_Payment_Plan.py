import pandas as pd
import streamlit as st
from utils.db_utils import get_relevant_transactions

st.set_page_config(
    page_title="Debt Free Payment Plan",
    page_icon="📊") 

def payment_plan_option(total, time):
    # Reads in the total and the time and applies the APR to calculate the amount 
    # they will need to pay to be debt free by chosen time and returns the payment.

    APR = 0.05 / 12
    payment = total * ((APR*(pow((1.0 + APR), time)))/(pow((1.0 + APR), time) - 1.0))
    return(payment)
    

def sum_of_debt(user_id):
# Gets the total debt for the user for 2019 and returns it.
    
    transaction_2019 = get_relevant_transactions(user_id=user_id, year='2019')
    sumofdebt = transaction_2019["amount"].sum()
    return(sumofdebt)

# Start of Streamlit page.
if 'user_id' in st.session_state:
    user_id = st.session_state["user_id"]

    if user_id != "BANK":
    # Makes sure not a BANK employee

        debt = sum_of_debt(user_id)
        time = 0
        st.write(f"Thank you, {user_id}, for choosing to consolidate your 2019 debt with our payment plan.")
        st.write(f"Your current total debt is ${debt: .2f}.")
        st.write("We currently have an APR on our payment plan of 5%.")
        st.write("This will offer you easy to pay monthly payments.")
        st.write("We have 4 options for our payment plan, please choose one of our plans.")
        
        # Arrange the buttons right next to each other.
        col1, col2, col3, col4 = st.columns([1,1,1,1])
        with col1:
            if st.button("6 Months"):
                time = 6
                
        with col2:
            if st.button("1 Year"):
                time = 12
                
        with col3:
            if st.button("3 Years"):
                time = 36
                
        with col4:
            if st.button("5 Years"):
                time = 60

        if time > 0:
            payment = payment_plan_option(debt, time)
            st.header(f"Your payment amount would be ${payment: .2f} over {time} months.")

        st.session_state["user_id"] = user_id

    else:
        # If BANK tries to use the file.
        st.write("Please use the BANK DEMO")
        st.session_state["user_id"] = user_id
else:
    # If the did not login at all.
    st.write("Please login to use the app")