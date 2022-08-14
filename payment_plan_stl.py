import pandas as pd
import streamlit as st
from db_utils import get_debt_free_db_engine, get_transaction_for_user_year

def intro():
    
    st.title("Debt Free Payment Plan")
    st.write(f"Thank you, {user}, for choosing to consolidate your debt with our payment plan.")
    st.write(f"Your current total debt is ${sumofdebt}.")
    st.write("We currently have an APR on our payment plan of 5%.")
    st.write("This will offer you easy to pay monthly payments.")
    st.write("We have 4 options for our payment plan, please choose one of our plans listed on the left.")
    st.write("Or Return to return to our main menu.")
    
def inputs():
    
    st.sidebar.header("Payment Plans")
    button1 = st.sidebar.button("6 Months")
    button2 = st.sidebar.button("1 Year")
    button3 = st.sidebar.button("3 Years")
    button4 = st.sidebar.button("5 Years")
    button5 = st.siderbar.button("Return")
    
    if button1:
        time_choice = 6
    elif button2:
        time_choice = 12
    elif button3:
        time_choice = 36
    elif button4:
        time_choice = 60
    elif button5:
        time_choice = 0
              
    return time_choice

def main(user):
    
    engine = get_debt_free_db_engine()
    transaction_2019 = get_transaction_for_user_year(engine, user, '2019')
    sumofdebt = transaction_2019["amount"].sum()
    
    intro()

    time = inputs()
    
    if time == 0:
        st.empty
        st.write("You will be returned to the main menu.")
        
                
    else:
        payment_amount = payment_plan_option(sumofdebt, time)
        st.header(f"Your payment amount would be ${payment_amount} over {time} months.")