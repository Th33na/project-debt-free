from functools import lru_cache
from sqlalchemy import create_engine, inspect
import pandas as pd

# default DB
DB_CONNECTION_STRING = "sqlite:///debtfreedb.db"

# Dictionary to retrieve the next month
NEXT_MONTH = {"01": "02",
              "02": "03",
              "03": "04",
              "04": "05",
              "05": "06",
              "06": "07",
              "07": "08",
              "08": "09",
              "09": "10",
              "10": "11",
              "11": "12",
              "12": "01"}
    
def get_debt_free_db_engine(db_connection_string=DB_CONNECTION_STRING):
    """
    Create and return a DB connection
    """
    engine = create_engine(db_connection_string)
    return engine

@lru_cache(maxsize=10)
def get_all_table_names(engine=None):
    """
        Retrieves all table names in the DB
    input: 
        engine: (optional) db connection
    output:
        list of tables names        
    """    

    if engine is None:
        engine = get_debt_free_db_engine()
    inspector = inspect(engine)
    return inspector.get_table_names()

@lru_cache(maxsize=10)
def get_all_data_from_mcc_type(engine=None):
    """
        Retrieves all mcc type data
    input: 
        engine: (optional) db connection
    output:
        dataframe containing all mcc types       
    """    

    if engine is None:
        engine = get_debt_free_db_engine()

    query = """
    SELECT *
    FROM mcc_type
    """
    
    df = pd.read_sql(query, engine)
    
    return df

@lru_cache(maxsize=10)
def get_all_data_from_txn_data(engine=None):
    """
        Retrieves all transaction data
    input: 
        engine: (optional) db connection
    output:
        dataframe containing all transaction data       
    """

    if engine is None:
        engine = get_debt_free_db_engine()
        
    query = """
    SELECT *
    FROM transaction_data
    """
    
    df = pd.read_sql(query, engine)
    
    return df

@lru_cache(maxsize=10)
def get_available_txn_years(engine=None, user_id=None):
    """
        Retrieves the years with available transaction data given user_id (optional)
    input: 
        engine: (optional) db connection
        user_id: (optional) user id
    output:
        dataframe containing all transaction data       
    """

    if engine is None:
        engine = get_debt_free_db_engine()
        
    query = "SELECT distinct strftime('%Y', transaction_date) as year FROM transaction_data"
    
    if user_id:
        query = query + " WHERE user_id = :user_id"
        df = pd.read_sql(query, engine, params={"user_id": user_id})
    else:
        df = pd.read_sql(query, engine)

    return df

@lru_cache(maxsize=10)
def get_all_data_from_account(engine=None):
    """
        Retrieves all accounts data
    input: 
        engine: (optional) db connection
    output:
        dataframe containing all accounts data       
    """
    
    if engine is None:
        engine = get_debt_free_db_engine()
        
    query = """
    SELECT *
    FROM account
    """
    
    df = pd.read_sql(query, engine)
    
    return df

@lru_cache(maxsize=10)
def get_all_data_from_account_holder(engine):
    """
        Retrieves all account holder data
    input: 
        engine: (optional) db connection
    output:
        dataframe containing all accountholder data       
    """

    if engine is None:
        engine = get_debt_free_db_engine()
        
    query = """
    SELECT *
    FROM account_holder
    """
    
    df = pd.read_sql(query, engine)
    
    return df

@lru_cache(maxsize=10)
def get_account_holder(user_id, engine=None):
    """
        Retrieves account holder data
    input: 
        engine: (optional) db connection
    output:
        dataframe with account holder info       
    """

    if engine is None:
        engine = get_debt_free_db_engine()
        
    query = """
    SELECT *
    FROM account_holder
    WHERE user_id = :user_id
    """
    
    df = pd.read_sql(query, engine, params={"user_id": user_id})
    
    return df

@lru_cache(maxsize=10)
def get_all_data_from_merchant(engine):
    """
        Retrieves all merchant data
    input: 
        engine: (optional) db connection
    output:
        dataframe containing all merchant data       
    """

    if engine is None:
        engine = get_debt_free_db_engine()
        
    query = """
    SELECT *
    FROM merchant
    """
    
    df = pd.read_sql(query, engine)
    
    return df

def get_account_for_user(engine=None, user_id=None):
    """
        Retrieves all transaction data
    input: 
        engine: (optional) db connection
        user_id: user id
    output:
        dataframe containing all user data       
    """


    if engine is None:
        engine = get_debt_free_db_engine()
        
    query = """
    SELECT *
    FROM account
    WHERE user_id = :user_id
    """
    
    df = pd.read_sql(query, engine, params={"user_id": user_id})
    
    return df    

@lru_cache(maxsize=10)
def get_transactions_for_user(engine, user_id, year=None, month=None, card=None):
    """
        Retrieves transaction for a user + year + month + card combination when applicable
    input: 
        user_id: integer user id
        year: (optional) String for the year in YYYY format
        month: (optional) String for the month in MM format
        card: (optional) Integer for the card number 
    output:
        dataframe containing all the charges        
    """    

    query = """
        SELECT *
        FROM transaction_data
        WHERE user_id = :user_id
    """
    
    params = {"user_id": user_id}

    if card:
        query = query + " and card = :card"
        params["card"] = card

    if year:
        start_date, end_date = get_year_month_string(year, month=month)
        query = query + " AND transaction_date between :start and :end"                
        params["start"] = start_date
        params["end"] = end_date                             

    df = pd.read_sql(query, engine, params=params)
    
    return df

def get_transactions_for_all_users(engine, year=None, month=None):
    """
        Retrieves transaction for all users + year + month combination when applicable
    input: 
        year: (optional) String for the year in YYYY format
        month: (optional) String for the month in MM format
    output:
        dataframe containing all the charges        
    """

    if engine is None:
        engine = get_debt_free_db_engine()

    query = """
        SELECT *
        FROM transaction_data
    """

    if year:
        params = {}
        start_date, end_date = get_year_month_string(year, month=month)
        query = query + " where transaction_date between :start and :end"                
        params["start"] = start_date
        params["end"] = end_date                             
        df = pd.read_sql(query, engine, params=params)
    else:
        df = pd.read_sql(query, engine)
    
    return df

@lru_cache(maxsize=10)
def get_relevant_transactions(user_id=None, year=None, month=None, card=None):
    """
    Retrieve credit card transactions. 
    input: 
        user_id: (optional) integer user id
        year: (optional) String for the year in YYYY format
        month: (optional) String for the month in MM format, will be used only for year is provided search
        card: (optional) Integer for the card number, will be used only for user specific search
    output:
        dataframe containing all the charges depending on the parameter
    """
    engine = get_debt_free_db_engine()
    
    if user_id:
        all_user_txn = get_transactions_for_user(engine, user_id, year=year, month=month, card=card)
    else:
        all_user_txn = get_transactions_for_all_users(engine, year=year, month=month)

    return all_user_txn

@lru_cache(maxsize=10)
def get_year_month_string(year, month=None):
    """
        Build the start and end date parameters given the year and month parameters
    input:
        year: String year in YYYY format
        month: (Optional) String Month in MM format
    output:
        list with start date and end date strings
    """
    
    END_DAY = "-01 00:00"

    if month:
        start_month = month
        end_month = NEXT_MONTH[month]
        end_year = str(int(year) + 1) if month == "12" else year
    else:
        end_year = str(int(year) + 1)
        start_month = end_month = "01"

    start_date = year + "-" + start_month + END_DAY
    end_date = end_year + "-" + end_month + END_DAY
        
    return (start_date, end_date)