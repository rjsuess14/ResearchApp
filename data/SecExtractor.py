##load API key
import streamlit as st
import json
from firecrawl import FirecrawlApp
import google.generativeai as genai
import markdown
import os
from dotenv import load_dotenv
import requests
import pandas as pd

#Retreive api keys and initialize tools
load_dotenv()
apikey = os.environ['FDAI_KEY']
headers = {"X-API-KEY": apikey}

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

model = genai.GenerativeModel('gemini-1.5-flash')

firecrawl = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

#fetch list of filings
def fd_filing_data(ticker, selected_filings):
    filing_url = f'https://api.financialdatasets.ai/filings'
    querystring = {"ticker": ticker}
    filing_response = requests.get(filing_url, headers=headers, params=querystring)

    if filing_response.status_code == 200:
        filing_data = filing_response.json().get('filings')
        filing_df = pd.DataFrame(filing_data)

        # Filter the DataFrame based on selected filing types
        if selected_filings:
            filing_df = filing_df[filing_df['filing_type'].isin(selected_filings)]

        if not filing_df.empty:
            return filing_df
    else:
        print("Failed to retrieve data from the API")
    return None

#summarize filing contents with Gemini
def get_filing_summary(ticker, selected_filing, user_prompt):
    filing_url = selected_filing['url']
    if filing_url:
        try:
            page_content = firecrawl.scrape_url(url=filing_url)
            prompt = f"{user_prompt}\n\nBased on the following filing for {ticker}:\n\n{page_content}"
            summary = model.generate_content(prompt).text
            return summary
        except Exception as e:
            return f"Error retrieving the filing content: {str(e)}"
    else:
        return f"No {selected_filing} filing found for {ticker}"

