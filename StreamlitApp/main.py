import os
from dotenv import load_dotenv
import pandas as pd
import requests
import streamlit as st
import plotly.graph_objects as go
import pygwalker as pyg
#from pygwalker.api.streamlit import StreamlitRenderer

# Import functions from the existing file
from SourceData.FdData import fd_fs_data, price_data
from SourceData.FmpData import fmp_fs_data, fmp_company_info, fmp_company_metrics, fmp_growth_metrics
from SourceData.FredData import fred_data, series_info, fred_options
from SourceData.MarketauxNews import get_news

# Set page config at the top
st.set_page_config(page_title="Equity Research App", layout="wide")


def home_page():
    st.header("Equity Research Assistant", divider=True)
    st.write(
        "Analyze company data, news and macroeconomic indicators. Use the sidebar to enter a ticker and navigate between different pages."
    )
    ticker = st.session_state.get('ticker', '')
    if ticker:
        st.write(f"Current Ticker: {ticker}")
    else:
        st.write("Please enter a ticker symbol in the sidebar to begin your analysis.")


def main():
    st.sidebar.title("Navigation")

    # Ticker input on the sidebar
    ticker = st.sidebar.text_input("Enter ticker symbol:", value="").upper()
    # Store the ticker in session state if it's not empty
    if ticker:
        st.session_state['ticker'] = ticker

    # Create the selectbox with the current page as the default
    page = st.sidebar.selectbox(
        "Go to", ("Home 🏠", "Overview 🔍", "Financial Statements 📊",
                  "Price Data 📈", "News 🗒️", "Macro Data 💸"))

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
    ticker = st.session_state.get('ticker', '')
    if not ticker:
        st.warning("Please enter a ticker symbol in the sidebar.")
        return
        
    st.title(f"Company Overview for {ticker}")

    if st.button("Get Info"):
        
        info_df = fmp_company_info(ticker)
        metric_df = fmp_company_metrics(ticker)
        growth_df = fmp_growth_metrics(ticker)

        # Custom CSS to style the layout
        st.markdown("""
        <style>
        .company-profile {
            display: flex;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .company-logo {
            flex: 0 0 150px;
            margin-right: 20px;
        }
        .company-info {
            flex: 1;
        }
        .company-name {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .company-detail {
            margin: 5px 0;
        }
        .company-description {
            margin-top: 15px;
        }
        img {
            width: 100%;
            max-width: 150px;
            height: auto;
            border-radius: 5px;
        }
        </style>
        """, unsafe_allow_html=True)

        # Create a container for the company profile
        profile_container = st.container()

        with profile_container:
            st.markdown(f"""
            <div class="company-profile">
                <div class="company-logo">
                    <img src="{info_df.iloc[0]['image']}" alt="Company Logo">
                </div>
                <div class="company-info">
                    <div class="company-name">{info_df.iloc[0]['companyName']}</div>
                    <div class="company-detail"><strong>Sector:</strong> {info_df.iloc[0]['sector']}</div>
                    <div class="company-detail"><strong>Industry:</strong> {info_df.iloc[0]['industry']}</div>
                    <div class="company-detail"><strong>Website:</strong> <a href="{info_df.iloc[0]['website']}" target="_blank">{info_df.iloc[0]['website']}</a></div>
                    <div class="company-description">{info_df.iloc[0]['description']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Parse price range and current price
        low_price, high_price = map(float, info_df.iloc[0]['range'].split('-'))
        current_price = float(info_df.iloc[0]['price'])

        # Create gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = current_price,
            domain = {'x': [0, 1], 'y': [0, 1]},
            gauge = {
                'axis': {'range': [low_price, high_price], 'tickwidth': 1, 'tickcolor': "black"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "black",
                'steps': [
                    {'range': [low_price, high_price], 'color': 'whitesmoke'}],
                'threshold': {
                    'line': {'color': "green", 'width': 2},
                    'thickness': 0.75,
                    'value': current_price
                }}))

        fig.update_layout(
            title = dict(
                text = "52-Week Range:",
                x = 0.25,
                xanchor = 'center',
                yanchor = 'top',
            ),
            font = {"color": "black", "family": "Source Sans Pro"},
            height = 200,
            margin = dict(l=20, r=20, t=50, b=20),
        )

        # Display financial information and gauge chart side by side
        st.subheader("Stock Performance", divider=True)
        col1, col2 = st.columns([1, 2])

        with col1:
            st.metric(label="Price", value=f"${current_price:.2f}", delta=f"{info_df.iloc[0]['changes']:.2f}", delta_color="normal")
            st.metric("Market Cap", f"${info_df.iloc[0]['mktCap']:,.0f}")

        with col2:
            # Display the gauge chart
            st.plotly_chart(fig, use_container_width=True)

        # Show company metrics
        st.subheader("Financial Metrics", divider=True)

        #import data
        metrics_tab = pyg.to_html(metric_df)
        growth_tab = pyg.to_html(growth_df)

        # Embed pygwalker in streamlit with tabs
        tabs = st.tabs(["Fundamental Metrics", "Growth Metrics"])
        with tabs[0]:
            st.components.v1.html(metrics_tab, height=1200)
        with tabs[1]:
            st.components.v1.html(growth_tab, height=1200)
        

def financial_statements_page():
    ticker = st.session_state.get('ticker', '')
    if not ticker:
        st.warning("Please enter a ticker symbol in the sidebar.")
        return
    st.title(f"Financial Statements for {ticker}")
    period = st.selectbox("Select period:", ["annual", "quarterly", "ttm"])
    limit = st.number_input("Enter limit:", min_value=1, max_value=25, value=4)

    if period == "annual":
        if st.button("Fetch Financial Statements"):
            income_df, balance_df, cash_flow_df = fmp_fs_data(
                ticker, period, limit)

            st.subheader("Income Statement")
            st.dataframe(income_df)

            st.subheader("Balance Sheet")
            st.dataframe(balance_df)

            st.subheader("Cash Flow Statement")
            st.dataframe(cash_flow_df)
    else:
        if st.button("Fetch Financial Statements"):
            income_df, balance_df, cash_flow_df = fd_fs_data(
                ticker, period, limit)

            st.subheader("Income Statement")
            st.dataframe(income_df)

            st.subheader("Balance Sheet")
            st.dataframe(balance_df)

            st.subheader("Cash Flow Statement")
            st.dataframe(cash_flow_df)


def price_data_page():
    ticker = st.session_state.get('ticker', '')
    if not ticker:
        st.warning("Please enter a ticker symbol in the sidebar.")
        return
    st.title(f"Price Data for {ticker}")
    interval = st.selectbox(
        "Select interval:",
        ["second", "minute", "day", "week", "month", "quarter", "year"])
    multiplier = st.number_input("Enter interval multiplier:",
                                 min_value=1,
                                 value=1)
    start_date = st.date_input("Start date")
    end_date = st.date_input("End date")

    if st.button("Fetch Price Data"):
        price_df = cached_price_data(ticker, interval, multiplier, start_date,
                                     end_date)
        price_df['time_milliseconds'] = pd.to_datetime(
            price_df['time_milliseconds'], unit='ms')
        price_df['time_milliseconds'] = price_df[
            'time_milliseconds'].dt.strftime('%Y-%m-%d %H:%M:%S %Z')
        #price_df = price_df.drop(columns=['time_milliseconds'])
        #price_df['time'] = pd.to_datetime(price_df['time'], format='%Y-%m-%d %H:%M:%S %Z', errors='coerce')

        # Candlestick chart of price data using Plotly
        fig = go.Figure(data=[
            go.Candlestick(x=price_df['time_milliseconds'],
                           open=price_df['open'],
                           high=price_df['high'],
                           low=price_df['low'],
                           close=price_df['close'])
        ])
        fig.update_layout(title='Candlestick Chart',
                          xaxis_title='Date',
                          yaxis_title='Price (USD)')
        st.plotly_chart(fig, use_container_width=True)

        # Data table of price data
        st.data_editor(
            price_df,
            column_config={
                "open":
                st.column_config.NumberColumn(
                    "Open (in USD)",
                    help=
                    "The price of the stock at the start of the day in USD",
                    step=0.01,
                    format="$%.2f",
                ),
                "close":
                st.column_config.NumberColumn(
                    "Close (in USD)",
                    help="The price of the stock at the end of the day in USD",
                    step=0.01,
                    format="$%.2f",
                ),
                "high":
                st.column_config.NumberColumn(
                    "High (in USD)",
                    help="The highest price of the stock during the day in USD",
                    step=0.01,
                    format="$%.2f",
                ),
                "low":
                st.column_config.NumberColumn(
                    "Low (in USD)",
                    help="The lowest price of the stock during the day in USD",
                    step=0.01,
                    format="$%.2f",
                ),
                "time_milliseconds":
                None
            },
            hide_index=True,
        )


def macro_data_page():
    st.title("Macro Data")

    # Define series options available. Add more as needed.
    series_options = fred_options()

    # Create input fields for FRED series ID and date range
    selected_series_name = st.selectbox('Select a Data Series:',
                                        list(series_options.keys()),
                                        index=0)
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
                fig = go.Figure(data=go.Scatter(x=macro_data['date'],
                                                y=macro_data['value'],
                                                mode='lines+markers'))
                fig.update_layout(title=fred_series['title'],
                                  xaxis_title='Date',
                                  yaxis_title='Value')

                # Display the chart
                st.plotly_chart(fig, use_container_width=True)

                # Display the data table
                st.data_editor(macro_data,
                               column_config={
                                   "realtime_start": None,
                                   "realtime_end": None
                               })
            else:
                st.error("Failed to fetch data from FRED API.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


def news_page():
    ticker = st.session_state.get('ticker', '')
    if not ticker:
        st.warning("Please enter a ticker symbol in the sidebar.")
        return
    st.title(f"{ticker} News")
    
    if st.button("Fetch News"):
        news_data = get_news(f"{ticker}")

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
        """,
                    unsafe_allow_html=True)

        # Create a container for the news articles
        news_container = st.container()

        with news_container:
            if news_data:  # Check if news_data is not empty
                # Limit the number of columns (e.g., to 3)
                num_columns = min(len(news_data), 3)
                cols = st.columns(num_columns)

                # Iterate through the news articles and columns
                for i, article in enumerate(news_data):
                    with cols[i % num_columns]:
                        # Your existing code to display each article
                        st.markdown(f"""
                        <div class="news-item">
                            <img src="{article[4]}" alt="News Image">
                            <div class="news-title">{article[0]}</div>
                            <div class="news-description">{article[1]}</div>
                            <div class="news-published">Published At: {pd.to_datetime(article[2]).strftime('%B %d, %Y %I:%M %p')}</div>
                            <a href="{article[3]}" target="_blank">Read more</a>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.write("No news articles found.")


if __name__ == "__main__":
    main()
