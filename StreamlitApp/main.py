import os
from dotenv import load_dotenv
import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go

# Import functions from the existing file
from SourceData.FdData import fd_fs_data, price_data
from SourceData.FmpData import fmp_fs_data, fmp_company_info
from SourceData.FredData import fred_data, series_info, fred_options
from SourceData.MarketauxNews import get_news

# Set page config at the top
st.set_page_config(page_title="Equity Research AI", layout="wide")

def home_page():
    st.title("Equity Research Assistant")
    st.write("Analyze company data, news and macroeconomic indicators. Use the sidebar to navigate between different views.")

def main():
    st.sidebar.title("Navigation")

    # Create the selectbox with the current page as the default
    page = st.sidebar.selectbox("Go to", ("Home 🏠", "Overview 🔍", "Financial Statements 📊", "Price Data 📈", "News 🗒️", "Macro Data 💸"))

    # Display the selected page
    if page == "Home 🏠":
        home_page()
    elif page == "Overview 🔍":
        profile_page()
    elif page == "Financial Statements 📊":
        financial_statements_page()
    elif page == "Price Data 📈":
        price_data_page()
    elif page == "News 🗒️":
        news_page()
    elif page == "Macro Data 💸":
        macro_data_page()

#@st.cache_data
#def cached_fs_data(ticker, period, limit):
#    return fs_data(ticker, period, limit)

@st.cache_data
def cached_price_data(ticker, interval, multiplier, start_date, end_date):
    return price_data(ticker, interval, multiplier, start_date, end_date)

def profile_page():
    st.title("Company Overview")
    ticker = st.text_input("Enter ticker symbol:")

    if st.button("Get Info"):
        info_df = fmp_company_info(ticker)
        

def financial_statements_page():
    st.title("Financial Statements")
    ticker = st.text_input("Enter ticker symbol:")
    period = st.selectbox("Select period:", ["annual", "quarterly", "ttm"])
    limit = st.number_input("Enter limit:", min_value=1, max_value=25, value=4)

    if period == "annual":
        if st.button("Fetch Financial Statements"):
            income_df, balance_df, cash_flow_df = fmp_fs_data(ticker, period, limit)
            
            st.subheader("Income Statement")
            st.dataframe(income_df)
            
            st.subheader("Balance Sheet")
            st.dataframe(balance_df)
            
            st.subheader("Cash Flow Statement")
            st.dataframe(cash_flow_df)
    else:
        if st.button("Fetch Financial Statements"):
            income_df, balance_df, cash_flow_df = fd_fs_data(ticker, period, limit)
            
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
        price_df['time_milliseconds'] = pd.to_datetime(price_df['time_milliseconds'], unit='ms')
        price_df['time_milliseconds'] = price_df['time_milliseconds'].dt.strftime('%Y-%m-%d %H:%M:%S %Z')
        #price_df = price_df.drop(columns=['time_milliseconds'])
        #price_df['time'] = pd.to_datetime(price_df['time'], format='%Y-%m-%d %H:%M:%S %Z', errors='coerce')

        # Candlestick chart of price data using Plotly
        fig = go.Figure(data=[go.Candlestick(x=price_df['time_milliseconds'],
                                              open=price_df['open'],
                                              high=price_df['high'],
                                              low=price_df['low'],
                                              close=price_df['close'])])
        fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price (USD)')
        st.plotly_chart(fig, use_container_width=True)

        # Data table of price data
        st.data_editor(
            price_df,
            column_config={
                "open": st.column_config.NumberColumn(
                    "Open (in USD)",
                    help="The price of the stock at the start of the day in USD",
                    step=0.01,
                    format="$%.2f",
                ),
                "close": st.column_config.NumberColumn(
                    "Close (in USD)",
                    help="The price of the stock at the end of the day in USD",
                    step=0.01,
                    format="$%.2f",
                ),
                "high": st.column_config.NumberColumn(
                    "High (in USD)",
                    help="The highest price of the stock during the day in USD",
                    step=0.01,
                    format="$%.2f",
                ),
                "low": st.column_config.NumberColumn(
                    "Low (in USD)",
                    help="The lowest price of the stock during the day in USD",
                    step=0.01,
                    format="$%.2f",
                ),    
                "time_milliseconds": None
            },
            hide_index=True,
        )

def macro_data_page():
    st.title("Macro Data")

    # Define series options available. Add more as needed.
    series_options = fred_options()
    
    # Create input fields for FRED series ID and date range
    selected_series_name = st.selectbox('Select a Data Series:', list(series_options.keys()), index=0)
    series_id = series_options[selected_series_name]
    start_date = st.date_input("Start Date:")
    end_date = st.date_input("End Date:")

    if st.button("Fetch Data"):
        try:
            # Fetch data from FRED API
            macro_data = fred_data(series_id, start_date, end_date)
            
            # Fetch series info
            fred_series = series_info(series_id)
            
            # Check if macro_data and fred_series are valid
            if not macro_data.empty:
                
                # Create a line chart using Plotly
                fig = go.Figure(data=go.Scatter(x=macro_data['date'], y=macro_data['value'], mode='lines+markers'))
                fig.update_layout(title=fred_series['title'], xaxis_title='Date', yaxis_title='Value')
                
                # Display the chart
                st.plotly_chart(fig, use_container_width=True)
                
                # Display the data table
                st.data_editor(
                    macro_data,
                    column_config={
                        "realtime_start": None,
                        "realtime_end": None
                    }
                )
            else:
                st.error("Failed to fetch data from FRED API.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

def news_page():
    st.title("Company News")
    ticker = st.text_input("Enter ticker symbol:")
    if st.button("Fetch News"):
        news_data = get_news(ticker)
        
        # Custom CSS to style the layout
        st.markdown("""
        <style>
        .news-item {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
            width: 300px;  /* Set width for news items */
            height: auto;  /* Set height for news items */
        }
        .news-title {
            font-weight: bold;
            margin-top: 5px;
        }
        .news-description {
            margin: 5px 0;
        }
        .news-published {
            color: #666;
            font-size: 0.8em;
        }
        img {
            width: 100%;  /* Set width for images */
            height: auto; /* Maintain aspect ratio */
            border-radius: 5px;
            margin-bottom: 10px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Create a container for the news articles
        news_container = st.container()

        with news_container:
            # Create a horizontal layout using st.columns
            cols = st.columns(len(news_data))  # Create a column for each article

            for col, article in zip(cols, news_data):
                with col:
                    st.markdown(f"""
                    <div class="news-item">
                        <img src="{article[4]}" alt="News Image"> <!-- Added image here -->
                        <div class="news-title">{article[0]}</div>
                        <div class="news-description">{article[1]}</div>
                        <div class="news-published">Published At: {pd.to_datetime(article[2]).strftime('%B %d, %Y %I:%M %p')}</div>
                        <a href="{article[3]}" target="_blank">Read more</a>
                    </div>
                    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

