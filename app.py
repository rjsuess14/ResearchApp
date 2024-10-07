import os
import streamlit as st

# Import the menu module
from menu import menu

# Set page config at the top
st.set_page_config(page_title="Equity Research App", layout="wide")


def home_page():
    menu()

    st.header("Equity Research Assistant", divider=True)
    st.write(
        "Analyze company data, news and macroeconomic indicators. Use the sidebar to enter a ticker and navigate between different pages."
    )

    ticker = st.session_state.get('ticker', '')
    if ticker:
        st.write(f"Current Ticker: {ticker}")
    else:
        st.write("Please enter a ticker symbol in the sidebar to begin your analysis.")


if __name__ == "__main__":
    home_page()
