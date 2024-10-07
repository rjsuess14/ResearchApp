import streamlit as st

def menu():
    st.sidebar.title("Navigation")

    # Ticker input on the sidebar
    ticker = st.sidebar.text_input("Enter ticker symbol:", value="").upper()
    # Store the ticker in session state if it's not empty
    if ticker:
        st.session_state['ticker'] = ticker

    # Use st.sidebar.page_link to create navigation links
    st.sidebar.page_link("app.py", label="Home", icon ="🏠")
    st.sidebar.page_link("pages/overview.py", label="Overview", icon = "🔍")
    st.sidebar.page_link("pages/financials.py", label="Financial Statements", icon = "📊")
    st.sidebar.page_link("pages/price.py", label="Price Data", icon= "📈")
    st.sidebar.page_link("pages/filings.py", label="Filing Summary", icon= "📁")
    st.sidebar.page_link("pages/news.py", label="News", icon = "🗒️")
    st.sidebar.page_link("pages/macro.py", label="Macro Data", icon= "💸")

    