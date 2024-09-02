import os
from dotenv import load_dotenv
import pandas as pd
import requests
import streamlit as st
import altair as alt

# Import functions from the existing file
from finDatasets import fs_data, price_data
from fredData import fetch_fred_data, fetch_series_info

# Set page config at the top
st.set_page_config(page_title="Financial Data Explorer", layout="wide")

def home_page():
    st.title("Financial Data Explorer")
    st.write("Analyze company financial data and macroeconomic indicators. Use the sidebar to navigate between different data views.")

def main():
    st.sidebar.title("Navigation")

    # Create the selectbox with the current page as the default
    page = st.sidebar.selectbox("Go to", ("Home 🏠", "Financial Statements 📊", "Price Data 📈", "Macro Data 💸"))

    # Display the selected page
    if page == "Home 🏠":
        home_page()
    elif page == "Financial Statements 📊":
        financial_statements_page()
    elif page == "Price Data 📈":
        price_data_page()
    elif page == "Macro Data 💸":
        macro_data_page()

@st.cache_data
def cached_fs_data(ticker, period, limit):
    return fs_data(ticker, period, limit)

@st.cache_data
def cached_price_data(ticker, interval, multiplier, start_date, end_date):
    return price_data(ticker, interval, multiplier, start_date, end_date)

def financial_statements_page():
    st.title("Financial Statements")
    ticker = st.text_input("Enter ticker symbol:")
    period = st.selectbox("Select period:", ["annual", "quarterly", "ttm"])
    limit = st.number_input("Enter limit:", min_value=1, max_value=25, value=4)

    if st.button("Fetch Financial Statements"):
        income_df, balance_df, cash_flow_df = cached_fs_data(ticker, period, limit)
        
        st.subheader("Income Statement")
        st.dataframe(income_df)
        
        st.subheader("Balance Sheet")
        st.dataframe(balance_df)
        
        st.subheader("Cash Flow Statement")
        st.dataframe(cash_flow_df)
            
def price_data_page():
    st.title("Price Data")
    ticker = st.text_input("Enter ticker symbol:")
    interval = st.selectbox("Select interval:", ["second", "minute", "day", "week", "month", "quarter", "year"])
    multiplier = st.number_input("Enter interval multiplier:", min_value=1, value=1)
    start_date = st.date_input("Start date")
    end_date = st.date_input("End date")

    if st.button("Fetch Price Data"):
        price_df = cached_price_data(ticker, interval, multiplier, start_date, end_date)
        price_df = price_df.drop(columns=['time_milliseconds'])
        price_df['time'] = pd.to_datetime(price_df['time']).dt.date

    #Candlestick chart of price data
        source = price_df

        open_close_color = alt.condition("datum.open <= datum.close",
                                        alt.value("#06982d"),
                                        alt.value("#ae1325"))

        base = alt.Chart(source).encode(
            alt.X('time:T',
                axis=alt.Axis(
                    format='%Y-%m-%d',
                    labelAngle=-45,
                    title='Date'
                )
            ),
            color=open_close_color
        )

        rule = base.mark_rule().encode(
            alt.Y(
                'low:Q',
                title='Price',
                scale=alt.Scale(zero=False),
            ),
            alt.Y2('high:Q')
        )

        bar = base.mark_bar().encode(
            alt.Y('open:Q'),
            alt.Y2('close:Q')
        )

        chart = rule + bar
        st.altair_chart(chart, theme="streamlit", use_container_width=True)

    #Data table of price data
        st.data_editor(
            price_df,
            column_config={
                "open": st.column_config.NumberColumn(
                    "Open (in USD)",
                    help="The price of the stock at the start of the day in USD",
                    min_value=0,
                    max_value=1000,
                    step=1,
                    format="$%.2f",
                ),
                "close": st.column_config.NumberColumn(
                    "Close (in USD)",
                    help="The price of the stock at the end of the day in USD",
                    min_value=0,
                    max_value=1000,
                    step=1,
                    format="$%.2f",
                ),
                "high": st.column_config.NumberColumn(
                    "High (in USD)",
                    help="The highest price of the stock during the day in USD",
                    min_value=0,
                    max_value=1000,
                    step=1,
                    format="$%.2f",
                ),
                "low": st.column_config.NumberColumn(
                    "Low (in USD)",
                    help="The lowest price of the stock during the day in USD",
                    min_value=0,
                    max_value=1000,
                    step=1,
                    format="$%.2f",
                ),
            },
            hide_index=True,
        )

def macro_data_page():
    st.title("Macro Data")

    #define series options available. Add more as needed.
    series_options = {
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
    # Create input fields for FRED series ID and date range
    selected_series_name = st.selectbox('Select a Data Series:', list(series_options.keys()), index=0)
    series_id = series_options[selected_series_name]
    start_date = st.date_input("Start Date:")
    end_date = st.date_input("End Date:")

    if st.button("Fetch Data"):
        try:
            # Fetch data from FRED API
            fred_data = fetch_fred_data(series_id, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            
            # Fetch series info
            series_info = fetch_series_info(series_id)
            series_title = series_info['title']
            
            if fred_data and series_info:
                # Extract observations from the API response
                observations = fred_data['observations']
                
                # Create a DataFrame from the observations
                df = pd.DataFrame(observations)
                df['date'] = pd.to_datetime(df['date'])
                df['value'] = pd.to_numeric(df['value'], errors='coerce')
                
                # Create a line chart using Altair
                chart = alt.Chart(df).mark_line().encode(
                    x='date:T',
                    y='value:Q',
                    tooltip=['date', 'value']
                ).properties(
                    width=600,
                    height=400,
                    title=series_title
                )
                
                # Display the chart
                st.altair_chart(chart, use_container_width=True)
                
                # Display the data table
                st.dataframe(df)
            else:
                st.error("Failed to fetch data from FRED API.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()