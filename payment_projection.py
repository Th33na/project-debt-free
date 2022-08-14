
import numpy as np
from utils.db_utils import get_relevant_transactions

"""
Generates the Payment Plan Calculation
based on user's monthly payment with resulting how many years balance will be paid off
"""

# method for calculating how long to pay off debt given desired monthly amount
def payment_projection(user_id, monthly_amount):
    transaction_2020 = get_relevant_transactions(user_id=user_id, year="2019")

    #get the amount on user's balance
    total_amount = transaction_2020[('amount')].sum()
    #get number of months
    number_of_months = total_amount/monthly_amount
    #get number of years
    number_of_years=number_of_months/12
    # print("Num Years: " + str(number_of_years))
    return number_of_years