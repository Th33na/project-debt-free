import streamlit as st
import numpy as np
import pandas as pd
from utils.db_utils import get_account_for_user, get_relevant_transactions, get_available_txn_years
from common.common import get_total_amount_by_group


MONTHS = ['01', '02','03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

st.set_page_config(
    page_title="User Credit Card Balance",
    page_icon="📊",   
)

def get_apr_for_card(user_id, card):
    """"
    Gets the Annual Percent Rate for a given user's credit card from database
    input: 
        user_id: BigInt user id
        card: Card Number
    ouput:
        annual_percent_rate APR from database
    """
    account_data = get_account_for_user(user_id=user_id)
    card= account_data.loc[account_data['card'] == card]
    annual_percent_rate= float(card['annual_percentage_rate'])
    return annual_percent_rate

def calc_new_balance(row, annual_percent_rate):
    """ 
    Calculates the new balance of summarized credit card transaction
    input:
        row: dataframe row containing 'user_id','card','amount' columns
        annual_percent_rate: APR for the credit card
    output:
        row updated with three new columns 'minimum_payment', 'interest_charged', 'new_balance'
    """
   
    # calculate monthly percent rate
    monthly_percent_rate = float((annual_percent_rate/100) / 12)
        
    # assign remaining balance
    monthly_remaining_balance = row['amount']
    
    # calculate minimum payment
    minimum_payment = (monthly_remaining_balance) * 0.02
    row['minimum_payment'] = round(minimum_payment,2)
    
    # deduct payment made i.e. min payment
    adjusted_balance = monthly_remaining_balance - minimum_payment
    
    # calculate interest
    interest_charged = adjusted_balance * monthly_percent_rate
    row['interest_charged'] = round(interest_charged,2)
    
    # calculate new balance
    new_balance = adjusted_balance + interest_charged
    row['new_balance'] = round(new_balance,2)

    return row

def get_cc_balance_user_for_cards(user_id, year, month, card):
    """
    Generates the Credit Card Balance for a year + month + card of user's transactions
    input: 
        user_id: BigInt user id
        year: String year in YYYY format
        month: String in MM format
        card: Card Number
    ouput:
        dataframe of minimum payment, interest charged and new balance for given user, card, month and year combination
    """
    txn = get_relevant_transactions(user_id=user_id, year=year, month=month, card=card)
    grouped_txn = get_total_amount_by_group(txn, ['user_id','card'])
    annual_percent_rate = get_apr_for_card(user_id=user_id,card=card)
    summary_transactions = grouped_txn.apply(lambda row: calc_new_balance(row,annual_percent_rate), axis =1)
    st.session_state["user_id"] = user_id
    return summary_transactions

def get_available_cards(user_id, year):
    """
    Gets the cards available to the current user.
    input:
        user_id: BigInt user id
    output:
        list of cards for the given user
    """
    account_data = get_relevant_transactions(user_id=user_id, year=year)
    cards = account_data['card'].unique()
    st.session_state["user_id"] = user_id
    return cards


if 'user_id' in st.session_state:
    user_id = st.session_state["user_id"]

    if user_id != "BANK":

        st.write("Hello, User " + str(user_id) + "!!! Please select a year, month, and card you want to see.")
        available_years = get_available_txn_years(user_id=user_id)
        year = st.radio("Year Selection", available_years, horizontal=True)
        month = st.radio("Month Selection", MONTHS, horizontal=True)
        available_cards = get_available_cards(user_id, year)
        card = st.radio("Card Selection", available_cards, horizontal=True)
        balance = get_cc_balance_user_for_cards(user_id, year, month, card)   
        st.write(balance)

    else:
        st.write("Please use the BANK DEMO")
        st.session_state["user_id"] = user_id
else:
    st.write("Please login to use the app")