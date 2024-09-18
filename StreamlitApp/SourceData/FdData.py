import os
from dotenv import load_dotenv
import pandas as pd
import requests

#import helper funtions
from SourceData.transformation import clean_fd_df

# Actual API key is stored in a .env file.  Not good to store API key directly in script.
load_dotenv()
apikey = os.environ['FDAI_KEY']

headers = {"X-API-KEY": apikey}


#Fetch financial statement data
def fd_fs_data(ticker, period, limit=None):
    fs_url = f'https://api.financialdatasets.ai/financials/'
    querystring = {"ticker": ticker, "period": period, "limit": limit}
    fs_response = requests.get(fs_url, headers=headers, params=querystring)

    if fs_response.status_code == 200:
        fs_data = fs_response.json().get('financials')
        is_data = fs_data.get('income_statements')
        bs_data = fs_data.get('balance_sheets')
        cfs_data = fs_data.get('cash_flow_statements')

        is_df = pd.DataFrame(is_data)
        bs_df = pd.DataFrame(bs_data)
        cfs_df = pd.DataFrame(cfs_data)

        fd_is_df = clean_fd_df(is_df)
        fd_bs_df = clean_fd_df(bs_df)
        fd_cfs_df = clean_fd_df(cfs_df)

    else:
        print("Failed to retrieve data from the API")
    return fd_is_df, fd_bs_df, fd_cfs_df


#Fetch financial statement data
def price_data(ticker, interval, multiplier, start_date, end_date):
    price_url = f'https://api.financialdatasets.ai/prices'
    querystring = {
        "ticker": ticker,
        "interval": interval,
        "interval_multiplier": multiplier,
        "start_date": start_date,
        "end_date": end_date
    }
    price_response = requests.get(price_url,
                                  headers=headers,
                                  params=querystring)

    if price_response.status_code == 200:
        price_data = price_response.json().get('prices')

        price_df = pd.DataFrame(price_data)

    else:
        print("Failed to retrieve data from the API")
    return price_df
