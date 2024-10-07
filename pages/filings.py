import streamlit as st
import pandas as pd

# Import functions from the existing file
from data.SecExtractor import fd_filing_data, get_filing_summary
from menu import menu

def filing_summary_page():
    menu()
    
    ticker = st.session_state.get('ticker', '')
    if not ticker:
        st.warning("Please enter a ticker symbol in the sidebar.")
        return
    st.title("SEC Filing Summary")

    # Dropdown for filing type
    filing_types = ["10-K", "10-Q", "8-K"]  # Add more as needed
    selected_types = st.multiselect("Select filing type(s):", filing_types)

    if selected_types:
        # Fetch filings data for selected types
        filings_df = fd_filing_data(ticker, selected_types)
        
        if not filings_df.empty:
            # Create a selectbox with options from the 'report_date' column
            selected_date = st.selectbox('Select a period:', filings_df['report_date'].unique())

            # Define a function that uses the selected option
            def process_selection(date, dataframe):
                selected_row = dataframe[dataframe['report_date'] == date].iloc[0]
                return selected_row

            # User prompt input
            user_prompt = st.text_area("Enter your prompt:")

            if st.button("Get Summary"):
                if ticker and user_prompt:
                    with st.spinner(f"Fetching {ticker} filing summary..."):
                        selected_filing = process_selection(selected_date, filings_df)
                        summary = get_filing_summary(ticker, selected_filing, user_prompt)
                        st.subheader(f"Summary of filing for {ticker}", divider=True)
                        st.write(summary)
                else:
                    st.warning("Please enter a ticker symbol and provide a prompt.")
        else:
            st.warning("No filings found for the selected type(s).")
    else:
        st.warning("Please select at least one filing type.")

# Call the function to display the filing summary page
filing_summary_page()