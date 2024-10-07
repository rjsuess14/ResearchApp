import streamlit as st
import plotly.graph_objects as go
import pygwalker as pyg

# Import functions from the existing file
from data.FmpData import fmp_company_info, fmp_company_metrics, fmp_growth_metrics
from menu import menu

def profile_page():
    menu()

    ticker = st.session_state.get('ticker', '')
    if not ticker:
        st.warning("Please enter a ticker symbol in the sidebar.")
        return
        
    st.title(f"Company Overview for {ticker}")
        
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


# Call the function to display the profile page
profile_page()