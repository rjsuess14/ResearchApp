import os
import pandas as pd
import numpy as np

# Import functions from the existing files
from FdData import fd_fs_data, price_data
from FmpData import fmp_fs_data, fetch_company_info
from FredData import fred_data, series_info
from MarketauxNews import fetch_news

def clean_financial_df(df):
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])

    # Set date as index and sort
    df.set_index('date', inplace=True)
    df.sort_index(inplace=True)

    # Remove duplicate entries
    df = df[~df.index.duplicated(keep='first')]

    # Convert numeric columns to float
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].astype(float)

    # Handle missing values (you might want to adjust this based on your specific needs)
    df.fillna(0, inplace=True)

    return df

def get_cleaned_financial_data(ticker, period, limit=None):
    fd_is_df, fd_bs_df, fd_cfs_df = fd_fs_data(ticker, period, limit)
    
    cleaned_is_df = clean_financial_df(fd_is_df)
    cleaned_bs_df = clean_financial_df(fd_bs_df)
    cleaned_cfs_df = clean_financial_df(fd_cfs_df)
    
    return cleaned_is_df, cleaned_bs_df, cleaned_cfs_df

# You can now use this function to get cleaned financial data
# Example usage:
cleaned_is, cleaned_bs, cleaned_cfs = get_cleaned_financial_data('AAPL', 'annual', 3)
print(cleaned_is)
print(cleaned_bs)
print(cleaned_cfs)
