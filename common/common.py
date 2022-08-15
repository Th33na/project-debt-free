import numpy as np
import pandas as pd

from utils.db_utils import get_all_data_from_mcc_type

def merge_transactions_with_mcc_group(txn):
    """
    Merges the transaction dataframe with the MCC dataframe
    """
    mcc_group = get_all_data_from_mcc_type()
    merged_txn = pd.merge(txn, mcc_group, on="mcc")
    if len(merged_txn) > 0:
        merged_txn.rename(columns={"edited_description": "description"}, inplace=True)
        sorted_txn = merged_txn.sort_values(by=['amount'], ascending=False)

        return sorted_txn
    else:
        return merged_txn

def get_total_amount_by_group(txn, grouping):
    grouped_txn = txn.groupby(by=grouping, as_index = False)['amount'].sum()
    
    return grouped_txn
