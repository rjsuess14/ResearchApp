# ResearchApp

## Overview

This equity research app is a comprehensive Streamlit-based web application designed to help users quickly analyze company data, news, and macroeconomic indicators. This tool provides a user-friendly interface for accessing and visualizing financial information, price history and various performance metrics.

## Features

- **Company Overview**: Get detailed company information, including key metrics and growth indicators.
- **Financial Statements**: Access and analyze income statements, balance sheets, and cash flow statements.
- **Price Data**: Visualize historical stock price data with customizable time intervals.
- **News**: View the latest company-specific news articles.
- **Macro Data**: Explore and visualize various macroeconomic indicators.

## Data Sources
- [Financial Modeling Prep](https://site.financialmodelingprep.com/)
- [Financial Datasets](https://www.financialdatasets.ai/)
- [Marketaux](https://www.marketaux.com/)
- [FRED](https://fred.stlouisfed.org/docs/api/fred/)


## Installation

1. Clone this repository
2. Install the required dependencies: [pip install -r requirements.txt]
3. Set up your environment variables:
Create a `.env` file in the root directory and add your API keys:
- `FMP_KEY=your_financial_modeling_prep_api_key`
- `FDAI_KEY=your_financial_datasets_api_key`
- `MARKETAUX_KEY=your_marketaux_api_key`
- `FRED_API_KEY=your_fred_api_key`


## Usage

1. Run the Streamlit app:

2. Open your web browser and navigate to the provided local URL (usually `http://localhost:8501`).

3. Use the sidebar to enter a ticker symbol and navigate between different pages of the application.

## Structure

- `StreamlitApp/main.py`: The main Streamlit application file.
- `StreamlitApp/SourceData/`: Contains modules for fetching data from various sources:
- `FdData.py`: Functions for fetching financial data.
- `FmpData.py`: Functions for fetching data from Financial Modeling Prep API.
- `FredData.py`: Functions for fetching macroeconomic data from FRED.
- `MarketauxNews.py`: Functions for fetching news data.

## Contributing

Contributions to improve the Equity Research Assistant are welcome. Please feel free to submit pull requests or open issues to discuss potential enhancements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer

This tool is for informational purposes only and should not be considered as financial advice. Always conduct your own research and consult with a qualified financial advisor before making investment decisions.
