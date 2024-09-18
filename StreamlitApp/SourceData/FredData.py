import os
from dotenv import load_dotenv
import requests
import pandas as pd

# Import API key stored in a .env file.
load_dotenv()
FRED_API_KEY = os.environ['FRED_KEY']

# FRED API functions
def fred_data(series_id, start_date=None, end_date=None):
    """
    Fetch data from the FRED API for a given series ID and return it as a pandas DataFrame.

    Parameters:
    series_id (str): The ID of the FRED data series.
    start_date (str): Optional start date for the data in YYYY-MM-DD format.
    end_date (str): Optional end date for the data in YYYY-MM-DD format.

    Returns:
    DataFrame: pandas DataFrame containing the data.
    """
    base_url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        'series_id': series_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json'
    }
    if start_date:
        params['observation_start'] = start_date
    if end_date:
        params['observation_end'] = end_date

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        observations = data['observations']
        df = pd.DataFrame(observations)
        df['date'] = pd.to_datetime(df['date']).dt.date
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df = df.dropna(subset=['value'])
        df.set_index('date', inplace=True, drop=False)
        return df
    else:
        response.raise_for_status()

def series_info(series_id):
    """
    Fetch metadata for a given series ID from the FRED API.

    Parameters:
    series_id (str): The ID of the FRED data series.

    Returns:
    dict: Parsed JSON response from the FRED API containing the series metadata.
    """
    base_url = "https://api.stlouisfed.org/fred/series"
    params = {
        'series_id': series_id,
        'api_key': FRED_API_KEY,
        'file_type': 'json'
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()['seriess'][0]
    else:
        response.raise_for_status()

def fred_options():
    return {
        "10YR Minus 2YR Treasury": "T10Y2Y",
        "10YR Minus 3M Treasury": "T10Y3M",
        "10YR Treasury Yield": "DGS10",
        "Federal Funds Rate": "FEDFUNDS",
        "30YR Mortgage Rate": "MORTGAGE30US",
        "Unemployment Rate": "UNRATE",
        "Initial Jobless Claims": "ICSA",
        "Total GDP": "GDP",
        "Median CPI": "MEDCPIM158SFRBCLE",
        "M2 Money Supply": "M2SL",
        "FED Total Assets": "WALCL",
        "Total Federal Debt": "GFDEBTN",
        "Federal Debt to GDP": "GFDEGDQ188S",
        "Government Surplus or Deficit": "FYFSD",
        "Household Debt to GDP": "HDTGPDUSQ163N",
        "Household Debt Service as Percent of Disposable Income": "TDSP",
        "Credit Card Delinquency Rate": "DRCCLACBS"
    }

