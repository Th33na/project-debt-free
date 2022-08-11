from sqlalchemy import create_engine, inspect
import pandas as pd

DB_CONNECTION_STRING = "sqlite:///debtfreedb.db"

def get_debt_free_db_engine():
    engine = create_engine(DB_CONNECTION_STRING)
    return engine

def get_all_table_names(engine):
    inspector = inspect(engine)
    return inspector.get_table_names()

def get_all_data_from_mcc_type(engine):
    query = """
    SELECT *
    FROM mcc_type
    """
    
    df = pd.read_sql(query, engine)
    
    return df

def get_all_data_from_txn_data(engine):
    query = """
    SELECT *
    FROM transaction_data
    """
    
    df = pd.read_sql(query, engine)
    
    return df


def get_all_data_from_account(engine):
    query = """
    SELECT *
    FROM account
    """
    
    df = pd.read_sql(query, engine)
    
    return df


def get_all_data_from_account_holder(engine):
    query = """
    SELECT *
    FROM account_holder
    """
    
    df = pd.read_sql(query, engine)
    
    return df

def get_all_data_from_merchant(engine):
    query = """
    SELECT *
    FROM merchant
    """
    
    df = pd.read_sql(query, engine)
    
    return df

def get_transaction_for_user(engine, user_id):
    """
    Retrieves transaction for a user
    """
    query = """
    SELECT *
    FROM transaction_data
    WHERE user_id = :user_id
    """
    
    df = pd.read_sql(query, engine, params={"user_id": user_id})
    
    return df


def get_transaction_for_user_card(engine, user_id, card):
    """
    Retrieves transaction for a user + card
    """
    query = """
    SELECT *
    FROM transaction_data
    WHERE user_id = :user_id
    and card = :card
    """
    
    df = pd.read_sql(query, engine, params={"user_id": user_id, "card": card})
    
    return df

def get_transaction_for_user_year(engine, user_id, year):
    """
    Retrieves transaction for a user
    """
    query = """
    SELECT *
    FROM transaction_data
    WHERE user_id = :user_id
    AND transaction_date between :start and :end
    """
    
    start_date = year + '-01-01 00:00'
    end_date = year + '-12-31 23:59'
    df = pd.read_sql(query, engine, params={"user_id": user_id, "start": start_date, "end": end_date})
    
    return df
        
def get_account_for_user(engine, user_id):
    query = """
    SELECT *
    FROM account
    WHERE user_id = :user_id
    """
    
    df = pd.read_sql(query, engine, params={"user_id": user_id})
    
    return df    