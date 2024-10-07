import streamlit as st

# Import functions from the existing file
from data.FdData import fd_fs_data
from data.FmpData import fmp_fs_data
from menu import menu

def financial_statements_page():
    menu()
    
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

# Call the function to display the financial statements page
financial_statements_page()