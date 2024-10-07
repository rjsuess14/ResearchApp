import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Import functions from the existing file
from data.FdData import price_data
from menu import menu

@st.cache_data
def cached_price_data(ticker, interval, multiplier, start_date, end_date):
    return price_data(ticker, interval, multiplier, start_date, end_date)

def price_data_page():
    menu()
    
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

# Call the function to display the price page
price_data_page()