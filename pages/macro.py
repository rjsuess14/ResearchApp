import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Import functions from the existing file
from data.FredData import fred_data, series_info, fred_options
from menu import menu

def macro_data_page():
    menu()
    
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

# Call the function to display the macro page
macro_data_page()