import numpy as np
import pandas as pd

import hvplot.pandas

from bokeh.models import HoverTool

from utils.db_utils import get_relevant_transactions, get_all_data_from_mcc_type
from common.common import merge_transactions_with_mcc_group, get_total_amount_by_group

    
def get_cc_utilization_plot_for_user_for_cards(user_id, year, month=None, card=None):
    """
    Generates the Credit Card Utilization Plot for a year + month + card of user's transactions
    input: 
        user_id: BigInt user id
        year: String year in YYYY format
        month: (Optional) String in MM format
        card: (Optional) Card Number
    ouput:
        bar chart of users utilization for year + month + card combination when applicable
    """

    txn = get_relevant_transactions(user_id=user_id, year=year, month=month, card=card)
    grouped_txn = get_total_amount_by_group(txn, ["mcc"])
        
    merged_txn = merge_transactions_with_mcc_group(grouped_txn)

    year_month = year + "-" + month if month else year

    title = f'Overall Card spendings for {year_month}'

    hover = HoverTool(tooltips=[("amount", "@amount{8.2f}"),
                                ("description", "@description"),
                                ("mcc", "@mcc")
                           ])
    plot = merged_txn.hvplot.bar(
        y='amount',
        x='mcc',
        title= title,
        rot=90,
        xlabel="Merchant Category Code",
        hover_cols=['mcc', 'amount', 'description'])
    return plot

def get_cc_utilization_plots_for_user_per_card(user_id, year, month=None):
    """
    Generates the Credit Card Utilization Plots for a year + month of user's transactions by Card
    input: 
        user_id: BigInt user id
        year: String year in YYYY format
        month: (Optional) String in MM format
        card: (Optional) Card Number
    ouput:
        bar charts of users utilization for year + month combination when applicable
    """
    
    txn = get_relevant_transactions(user_id=user_id, year=year, month=month)
    grouped_txn = get_total_amount_by_group(txn, ["mcc", "card"])
        
    merged_txn = merge_transactions_with_mcc_group(grouped_txn)
    
    year_month = year + "-" + month if month else year

    plot_list = []

    for card_num in sorted(merged_txn['card'].unique()):
        card_txn = merged_txn[merged_txn["card"] == card_num]

        title = f'Card {card_num} spendings for {year_month}'


        hover = HoverTool(tooltips=[("amount", "@amount{8.2f}"),
                                    ("description", "@description")
                               ])
        plot = card_txn.hvplot.barh(
            y='amount',
            x='description',
            title= title,
            xlabel="Merchant Category",
            hover_cols=['amount', 'description'])
        
        
        plot_list.append(plot)

    
    return plot_list
