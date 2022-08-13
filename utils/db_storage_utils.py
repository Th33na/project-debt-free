import numpy as np
import pandas as pd
import random
import math
from pathlib import Path
from sqlalchemy import inspect, MetaData, Table, Column, Integer, String, types

from db_utils import get_debt_free_db_engine

def load_all_data():
    load_and_store_mcc()
    load_and_store_ccinfo()

def load_and_store_mcc(mcc_path_filename = "./resources/mcc_codes.csv", engine = get_debt_free_db_engine()):
    """
    Load mcc data and store into db
    input:
        - mcc_path_filename: String by default uses './resources/mcc_codes.csv' otherwise user specified location
        - engine: sqlalchemy connection engine by default uses  'sqlite:///debtfreedb.db'
    output:
        -  json with data, status code, as well as error message when there is a failure   
    """
    # TODO: validation and error handling
    
    mcc_df = load_mcc_source_file(mcc_path_filename=mcc_path_filename)
    store_mcc_to_db(engine, mcc_df)
    
    return {"status": "200", "error_message": None, "data": mcc_df}

def load_mcc_source_file(mcc_path_filename = "./resources/mcc_codes.csv"):
    """
    Load the mcc source file into a pandas dataframe
    input:
        - mcc_path_filename: String by default uses './resources/mcc_codes.csv' otherwise user specified location
    output:
        - dataframe containing the mcc data with columns 'mcc' & 'edited_description' in proper formats
    """
    # TODO: validation to ensure the file exists and the necessary fields/columns exists

    csv_path = Path(mcc_path_filename)
    mcc_df = pd.read_csv(csv_path)
    
    # Change datatype
    mcc_df['mcc'] = mcc_df['mcc'].astype(str)
    # Change Value
    mcc_df['mcc'] = mcc_df['mcc'].str.zfill(4)
    mcc_df.head()
    return mcc_df

def store_mcc_to_db(engine, mcc_dataframe):
    """
        create or replace the mcc_type table in the DB
    input:
        - engine: sqlalchemy connection engine
        - mcc_dataframe: dataframe containing the mcc data with columns 'mcc' & 'edited_description' in proper formats 
    output:
        -  json with status code, as well as error message when there is a failure
    """
    # TODO: validation to ensure necessary fields/columns exists, and DB storage is successful

    # create mcc_type table
    mcc_dataframe[['mcc','edited_description' ]].to_sql(name="mcc_type",
                                                 con=engine,
                                                 if_exists='replace',
                                                 index=False,
                                                 dtype={'mcc': types.VARCHAR(length=4),
                                                        'edited_description':  types.VARCHAR(length=150)})
    return {"status": "200", "error_message": None}


def load_and_store_ccinfo(ccinfo_path_filename = './resources/mcc_codes.csv', engine = get_debt_free_db_engine()):
    """
    Load cc info data and store into db
    input:
        - ccinfo_path_filename: String by default uses './resources/mcc_codes.csv' otherwise user specified location
        - engine: sqlalchemy connection engine by default uses  'sqlite:///debtfreedb.db'
    output:
        -  json with status code, as well as error message when there is a failure   
    """
    # TODO: validation and error handling
    
    cc_info_df = load_ccinfo_source_file(ccinfo_path_filename)
    
    store_ccinfo_to_db(engine, cc_info_df)
    
    return {"status": "200", "error_message": None}

def load_ccinfo_source_file(ccinfo_path_filename = './ccinfo/ccinfo_reduced.csv'):
    """
    Load the mcc source file into a pandas dataframe
    
    input:
        - ccinfo_path_filename: String by default uses './ccinfo/ccinfo_reduced.csv' otherwise user specified location
    output:
        - dataframe containing the mcc data with columns in proper formats
    """
    # TODO: validation to ensure the file exists and the necessary fields/columns exists

    # load the credit card info csv
    csv_path = Path(ccinfo_path_filename)
    cc_info_df = pd.read_csv(csv_path)
    
    
    cc_info_df = transform_ccinfo_data(cc_info_df)
    
    return cc_info_df

def update_ccinfo_datatype(cc_info_df):
    """"
    Update the data types in the cc info dataframe
    input:
        - ccinfo_df: cc info dataframe
    output:
        - updated cc info dataframe
    """
     
    # Change data type
    cc_info_df['MCC'] = cc_info_df['MCC'].astype(str)
    cc_info_df['Zip'] = cc_info_df['Zip'].astype(str)
    cc_info_df['Amount'] = cc_info_df['Amount'].astype(str)
    cc_info_df['Month'] = cc_info_df['Month'].astype(str)
    cc_info_df['Day'] = cc_info_df['Day'].astype(str)
    cc_info_df['Year'] = cc_info_df['Year'].astype(str)
    
    return cc_info_df

def transform_ccinfo_rows(cc_info_df):
    """
    Reformat and or supplement data for the cc 
    input:
        - cc_info_df: ccinfo dataframe
    output:
        - updated cc_info_df
    """
    # TODO: validation and error handling

    # Change/reformat the values
    cc_info_df['MCC'] = cc_info_df['MCC'].str.zfill(4)
    cc_info_df['Month'] = cc_info_df['Month'].str.zfill(2)
    cc_info_df['Day'] = cc_info_df['Day'].str.zfill(2)
    cc_info_df['zip'] = cc_info_df['Zip'].str[:5]
    cc_info_df['Amount'] = cc_info_df["Amount"].str.replace("$", "", regex=False)


    cc_info_df['merchant_id'] = cc_info_df['Merchant Name']

    cc_info_df['transaction_date'] = pd.to_datetime(cc_info_df['Year'].astype(str) + '/' + cc_info_df['Month'] + '/' + cc_info_df['Day'] + ' ' + cc_info_df['Time'])
    
    return cc_info_df

def update_ccinfo_column_names(cc_info_df):
    """"
    Change column names
    input:
        - ccinfo_df: cc info dataframe
    output:
        - updated cc info dataframe
    """
    # Change column names
    cc_info_df.rename(columns={'User':'user_id',
                           'MCC':'mcc',
                           'Card':'card',
                           'Amount': 'amount',
                           'Merchant Name':'merchant_name',
                           'Merchant City':'merchant_city',
                           'Merchant State':'merchant_state',
                          }, inplace=True)

    return cc_info_df

def transform_ccinfo_data(cc_info_df):
    """"
    Massage the data in the dataframe by updating the data types, reformating values and supplementing data
    input:
        - cc_info_df: cc info dataframe
    output:
        - updated cc info dataframe
    """
    cc_info_df = update_ccinfo_datatype(cc_info_df)
    cc_info_df = transform_ccinfo_rows(cc_info_df)
    cc_info_df = update_ccinfo_column_names(cc_info_df)
    
    # Drop unncessary fields
    cc_info_df.drop(columns=['Month','Day','Time','Use Chip','Errors?','Zip','Is Fraud?'], inplace=True)
    
    return cc_info_df
    
def build_account_data(cc_info_df):
    """"
    Create a data with each user-card combo estimated credit limit
    input:
        - ccinfo_df: cc info dataframe
    output:
        - updated cc info dataframe
    """
    
    updated_cc_info = cc_info_df.drop(columns=['merchant_name','merchant_city','merchant_state','zip','merchant_id','transaction_date'])
    updated_cc_info = updated_cc_info.loc[(updated_cc_info['Year'] == "2019")]
    updated_cc_info['amount'] = pd.to_numeric(updated_cc_info['amount'])
    updated_cc_info.drop(columns=['Year'], inplace=True)

    # In normal situation, apr and credit limit data will be provided by the bank or the user,
    # but since we don't have apr and credit limit available we are guess  
    guesstimate_df = updated_cc_info.groupby(['user_id', 'card'],as_index = False)['amount'].sum()
    guesstimate_df['credit_limit'] = guesstimate_df.apply(lambda row: random_ceiling_on_cc_limit(row), axis=1)
    guesstimate_df['card_name'] = 'CARD' + guesstimate_df['card'].astype(str)
    guesstimate_df['annual_percentage_rate'] = guesstimate_df.apply(lambda row: random_apr(row), axis=1)
    guesstimate_df.drop(columns=['amount'], inplace=True)
    guesstimate_df['user_name'] = 'USER' + guesstimate_df['user_id'].astype(str)
    guesstimate_df['card_name'] = 'CARD' + guesstimate_df['card'].astype(str)
    
    return guesstimate_df

def random_ceiling_on_cc_limit(limit_row):
    """"
    Randomizes the available credit and rounding the value to the nearest 100
    input:
        - limit_row: cc info dataframe
    output:
        - computed value
    """
    random_available = random.randint(100, 1000)
    monthly_ave = limit_row['amount'] / 12    
    return math.ceil((monthly_ave + random_available) / 100)  * 100

def random_apr(limit_row):
    """"
    Randomizes the apr
    input:
        - limit_row: row in cc info dataframe
    output:
        - computed value
    """
    card_value = int(limit_row['card'])
    apr = "{:.2f}".format(card_value + random.uniform(1.3, 2.5))
    return apr

def store_ccinfo_to_db(engine, cc_info_df):
    """
        store cc info related data in the DB
    input:
        - engine: sqlalchemy connection engine
        - cc_info_df: dataframe containing thecc info in proper formats 
    output:
        -  json with status code, as well as error message when there is a failure
    """
    
    # TODO: validation and error handling   
    store_transaction_to_db(engine, cc_info_df)
    account_info_df = build_account_data(cc_info_df)
    store_account_holder_to_db(engine, account_info_df)
    store_account_to_db(engine, account_info_df)
    
    return {"status": "200", "error_message": None}

def store_transaction_to_db(engine, cc_info_df):
    """
        Create or Replace transaction data in the DB
    input:
        - engine: sqlalchemy connection engine
        - cc_info_df: dataframe containing the cc info in proper formats 
    output:
        -  json with status code, as well as error message when there is a failure
    """
    
    cc_info_df[['transaction_date','card', 'user_id', 'amount', 'mcc', 'merchant_id']].to_sql(name="transaction_data", con=engine, if_exists='replace', index=False,
                dtype={'transaction_date': types.DateTime(timezone=False), 
                       'card': types.BigInteger(),
                       'user_id': types.BigInteger(),
                       'amount': types.Numeric(8,2),
                       'mcc': types.VARCHAR(length=4),
                       'merchant_id': types.BigInteger()
                      })
    return {"status": "200", "error_message": None}
    
def store_account_holder_to_db(engine, account_info_df):
    """
        Create or Replace account holder data in the DB
    input:
        - engine: sqlalchemy connection engine
        - cc_info_df: dataframe containing the cc info in proper formats 
    output:
        -  json with status code, as well as error message when there is a failure
    """
    account_holder_df = account_info_df.drop(columns=['credit_limit', 'card','card_name', 'annual_percentage_rate'])
    account_holder_df.drop_duplicates(inplace=True)
    account_holder_df.head()
    # create account holder table
    account_holder_df[['user_id','user_name']].to_sql(name="account_holder", con=engine, if_exists='replace', index=False,
                dtype={'user_id': types.BigInteger(), 
                       'user_name': types.VARCHAR(length=50)
                      })
    
    
def store_account_to_db(engine, account_info_df):
    """
        Create or Replace account data in the DB
    input:
        - engine: sqlalchemy connection engine
        - cc_info_df: dataframe containing the cc info in proper formats 
    output:
        -  json with status code, as well as error message when there is a failure
    """    
    # create accounts table
    account_detail_df = account_info_df.drop(columns=['user_name'])
    account_detail_df[['user_id', 'card', 'credit_limit','card_name', 'annual_percentage_rate']].to_sql(name="account", con=engine, if_exists='replace', index=False,
                dtype={'user_id': types.BigInteger(), 
                       'card': types.BigInteger(),
                       'credit_limit': types.Numeric(10,2),
                       'card_name': types.VARCHAR(length=50),
                       'annual_percentage_rate': types.Numeric(5,2)
                      })
    
    return {"status": "200", "error_message": None}
    
def store_merchants_to_db(engine,cc_info_df):
    """
        Create or Replace merchant data in the DB
    input:
        - engine: sqlalchemy connection engine
        - cc_info_df: dataframe containing the cc info in proper formats 
    output:
        -  json with status code, as well as error message when there is a failure
    """    
    merchants_df = cc_info_df.drop(columns=['user_id', 'card', 'Year', 'amount', 'mcc', 'transaction_date'])

    merchants_df.drop_duplicates(inplace=True)
    merchants_df.head()
    # create merchant table
    merchants_df[['merchant_id','merchant_name','merchant_city','merchant_state','zip']].to_sql(name="merchant", con=engine, if_exists='replace', index=False,
                dtype={'merchant_id': types.BigInteger(), 
                       'merchant_name': types.VARCHAR(length=50),
                       'merchant_city': types.VARCHAR(length=50),
                       'merchant_state': types.VARCHAR(length=2),
                       'zip': types.VARCHAR(length=5),
                      })
    
    return {"status": "200", "error_message": None}