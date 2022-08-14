
import numpy as np
from utils.db_utils import get_relevant_transactions


#method for calculating how long to pay off debt given desired monthly amount
def payment_projection(user_id, monthly_amount):
    transaction_2020 = get_relevant_transactions(user_id=user_id, year="2019")

    #get the amount on user's balance
    total_amount = transaction_2020[('amount')].sum()
    #get number of months
    number_of_months = total_amount/monthly_amount
    # print("Num Months: " + str(number_of_months))
    #get number of years
    number_of_years=number_of_months/12
    # print("Num Years: " + str(number_of_years))
    #return the number of years for output to use in flask
    return number_of_years