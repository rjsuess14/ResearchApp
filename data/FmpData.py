import os
from dotenv import load_dotenv
import pandas as pd
import requests

#import helper funtions
from data.transformation import clean_fmp_df, clean_fmp_metrics

# Actual API key is stored in a .env file.  Not good to store API key directly in script.
load_dotenv()
apikey = os.environ['FMP_KEY']


#Fetch financial statement data
def fmp_fs_data(ticker, period, limit=None):

    is_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period={period}&limit={limit}&apikey={apikey}"
    is_response = requests.get(is_url)
    bs_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={apikey}"
    bs_response = requests.get(bs_url)
    cfs_url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?period={period}&limit={limit}&apikey={apikey}"
    cfs_response = requests.get(cfs_url)

    if is_response.status_code == 200 and bs_response.status_code == 200 and cfs_response.status_code == 200:
        is_data = is_response.json()
        is_df = pd.DataFrame(is_data)
        bs_data = bs_response.json()
        bs_df = pd.DataFrame(bs_data)
        cfs_data = cfs_response.json()
        cfs_df = pd.DataFrame(cfs_data)

        fmp_is_df = clean_fmp_df(is_df)
        fmp_bs_df = clean_fmp_df(bs_df)
        fmp_cfs_df = clean_fmp_df(cfs_df)

    else:
        print("Failed to retrieve data from the API")
    return fmp_is_df, fmp_bs_df, fmp_cfs_df


#Fetch company info


def fmp_company_info(ticker):

    url = f"https://financialmodelingprep.com/api/v3/profile/{ticker}?apikey={apikey}"
    response = requests.get(url)

    if response.status_code == 200:
        profile_data = response.json()
        # Convert the dictionary to a DataFrame
        df = pd.DataFrame([profile_data[0]])
        df = df[[
            'price', 'changes', 'range', 'mktCap', 'companyName', 'industry',
            'description', 'sector', 'image', 'website'
        ]].dropna()
    else:
        print(
            f"Failed to retrieve data from the API. Status code: {response.status_code}"
        )
    return df


#Fetch company metrics
def fmp_company_metrics(ticker):

    annual_url = f"https://financialmodelingprep.com/api/v3/key-metrics/{ticker}?apikey={apikey}"
    annual_response = requests.get(annual_url)
    ttm_url = f"https://financialmodelingprep.com/api/v3/key-metrics-ttm/{ticker}?apikey={apikey}"
    ttm_response = requests.get(ttm_url)

    if annual_response.status_code == 200 and ttm_response.status_code == 200:
        annual_data = annual_response.json()
        annual_df = pd.DataFrame(annual_data)
        ttm_data = ttm_response.json()
        ttm_df = pd.DataFrame(ttm_data)

        combined_metrics_df = clean_fmp_metrics(annual_df, ttm_df)

    else:
        print("Failed to retrieve data from the API.")
    return combined_metrics_df

#Fetch growth metrics
def fmp_growth_metrics(ticker):

    url = f"https://financialmodelingprep.com/api/v3/financial-growth/{ticker}?apikey={apikey}"
    response = requests.get(url)

    if response.status_code == 200:
        growth_metrics_data = response.json()
        growth_metrics_df = pd.DataFrame(growth_metrics_data)
        growth_metrics_df = growth_metrics_df.set_index(['date'])

        growth_metrics_df = growth_metrics_df[[
            'calendarYear', 'revenueGrowth', 'grossProfitGrowth', 'rdexpenseGrowth', 'sgaexpensesGrowth',
            'operatingIncomeGrowth', 'netIncomeGrowth', 'weightedAverageSharesDilutedGrowth', 'dividendsperShareGrowth',
            'operatingCashFlowGrowth', 'freeCashFlowGrowth'
        ]].dropna()

    else:
        print("Failed to retrieve data from the API.")
    return growth_metrics_df


