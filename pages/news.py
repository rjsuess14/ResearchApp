import streamlit as st
import pandas as pd

# Import functions from the existing file
from data.MarketauxNews import get_news
from menu import menu

def news_page():
    menu()

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

# Call the function to display the news page
news_page()