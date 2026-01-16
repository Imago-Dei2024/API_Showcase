import streamlit as st
import pandas as pd
import json
import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlencode
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="AlphaVantage API Interface",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# App title and description
st.title("📈 AlphaVantage API Interface")
st.markdown("Professional financial data analysis with real-time API integration")

# Sidebar for API selection and parameters
with st.sidebar:
    st.header("API Configuration")
    
    # API function selection
    api_function = st.selectbox(
        "Select API Function",
        ["ANALYTICS_FIXED_WINDOW", "NEWS_SENTIMENT", "TIME_SERIES_DAILY", 
         "COMPANY_OVERVIEW", "EARNINGS"],
        help="Choose the AlphaVantage API endpoint to use"
    )
    
    st.divider()
    
    # Dynamic parameter inputs based on selected function
    if api_function == "ANALYTICS_FIXED_WINDOW":
        st.subheader("Fixed Window Analytics")
        st.markdown("**What this does:** Calculates advanced financial metrics like variance, returns, correlations over specific time periods")
        
        symbols = st.text_input(
            "Symbols*", 
            value="AAPL,MSFT,GOOGL",
            help="Comma-separated stock symbols (up to 50 for premium)"
        )
        
        time_range = st.text_input(
            "Time Range*",
            value="full",
            help="Options: full, 1day, 1week, 1month, 1year, or custom dates"
        )
        
        interval = st.selectbox(
            "Interval*",
            ["1min", "5min", "15min", "30min", "60min", "DAILY", "WEEKLY", "MONTHLY"],
            index=5,
            help="Time interval between data points"
        )
        
        calculations = st.multiselect(
            "Calculations*",
            ["MIN", "MAX", "MEAN", "MEDIAN", "CUMULATIVE_RETURN", 
             "VARIANCE", "STDDEV", "MAX_DRAWDOWN", "HISTOGRAM", 
             "AUTOCORRELATION", "COVARIANCE", "CORRELATION"],
            default=["MEAN", "STDDEV", "CUMULATIVE_RETURN"],
            help="Select analytics metrics to calculate"
        )
        
        # Build params
        params = {
            'function': api_function,
            'SYMBOLS': symbols,
            'RANGE': time_range,
            'INTERVAL': interval,
            'CALCULATIONS': ','.join(calculations)
        }
    
    elif api_function == "NEWS_SENTIMENT":
        st.subheader("News Sentiment Analysis")
        st.markdown("**What this does:** Fetches market news with sentiment analysis from premier outlets worldwide")
        
        tickers = st.text_input(
            "Tickers",
            value="AAPL,MSFT",
            help="Stock symbols to filter news (optional)"
        )
        
        topics = st.multiselect(
            "Topics",
            ["blockchain", "earnings", "ipo", "mergers_and_acquisitions", 
             "financial_markets", "economy_fiscal", "economy_monetary", 
             "economy_macro", "energy_transportation", "finance", 
             "life_sciences", "manufacturing", "real_estate", 
             "retail_wholesale", "technology"],
            default=["earnings", "technology"],
            help="News topics to include"
        )
        
        sort_order = st.selectbox(
            "Sort Order",
            ["LATEST", "EARLIEST", "RELEVANCE"],
            help="How to sort the news results"
        )
        
        limit = st.slider(
            "Article Limit",
            min_value=1,
            max_value=1000,
            value=50,
            help="Number of articles to fetch (max 1000)"
        )
        
        # Build params
        params = {
            'function': api_function,
            'sort': sort_order,
            'limit': str(limit)
        }
        
        if tickers:
            params['tickers'] = tickers
        if topics:
            params['topics'] = ','.join(topics)
    
    else:
        st.info(f"Parameter configuration for {api_function} coming soon!")
        params = {'function': api_function}

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # API call button and status
    if st.button("🚀 Fetch Data", type="primary", use_container_width=True):
        # Check for API key
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        
        if not api_key:
            st.error("❌ API key not found! Please add ALPHA_VANTAGE_API_KEY to your .env file")
        else:
            with st.spinner("Fetching data from AlphaVantage..."):
                try:
                    # Make API call
                    base_url = 'https://www.alphavantage.co/query'
                    params['apikey'] = api_key
                    
                    response = requests.get(f'{base_url}?{urlencode(params)}')
                    data = response.json()
                    
                    # Save to session state
                    st.session_state.api_data = data
                    st.session_state.api_params = params
                    
                    # Save to file
                    json_dir = Path('Analytics_JSON') / 'Streamlit_Results'
                    json_dir.mkdir(parents=True, exist_ok=True)
                    filename = json_dir / f'{api_function}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                    
                    with open(filename, 'w') as f:
                        json.dump(data, f, indent=2)
                    
                    st.success(f"✅ Data fetched successfully! Saved to {filename}")
                    
                except Exception as e:
                    st.error(f"❌ Error fetching data: {str(e)}")

with col2:
    # API status and info
    st.subheader("API Status")
    if os.getenv("ALPHA_VANTAGE_API_KEY"):
        st.success("🔑 API Key: Found")
    else:
        st.error("🔑 API Key: Missing")
    
    # Show current parameters
    with st.expander("Current Parameters"):
        st.json(params)

# Display results if available
if 'api_data' in st.session_state:
    st.divider()
    st.header("📊 Results")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Analysis", "📋 Raw Data", "💾 Download", "📊 Visualizations"])
    
    with tab1:
        # Formatted analysis view
        data = st.session_state.api_data
        
        if api_function == "ANALYTICS_FIXED_WINDOW" and 'payload' in data:
            st.subheader("Financial Analytics Results")
            
            # Convert to DataFrame for better display
            results_data = []
            for symbol, metrics in data['payload'].items():
                row = {'Symbol': symbol}
                row.update(metrics)
                results_data.append(row)
            
            if results_data:
                df = pd.DataFrame(results_data)
                st.dataframe(df, use_container_width=True)
                
                # Key metrics summary
                col1, col2, col3, col4 = st.columns(4)
                
                if 'MEAN' in df.columns:
                    with col1:
                        st.metric("Avg Return", f"{df['MEAN'].mean():.4f}")
                
                if 'STDDEV' in df.columns:
                    with col2:
                        st.metric("Avg Volatility", f"{df['STDDEV'].mean():.4f}")
                
                if 'CUMULATIVE_RETURN' in df.columns:
                    with col3:
                        st.metric("Best Performer", 
                                df.loc[df['CUMULATIVE_RETURN'].idxmax(), 'Symbol'])
                
                with col4:
                    st.metric("Symbols Analyzed", len(df))
        
        elif api_function == "NEWS_SENTIMENT" and 'feed' in data:
            st.subheader("News Sentiment Analysis")
            
            # Display key metrics
            articles = data['feed']
            if articles:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Total Articles", len(articles))
                
                with col2:
                    sentiments = [article.get('overall_sentiment_label', 'Neutral') for article in articles]
                    positive_count = sentiments.count('Bullish')
                    st.metric("Bullish Articles", positive_count)
                
                with col3:
                    negative_count = sentiments.count('Bearish')
                    st.metric("Bearish Articles", negative_count)
                
                # Display articles
                st.subheader("Recent Articles")
                for i, article in enumerate(articles[:10]):  # Show first 10
                    with st.expander(f"📰 {article.get('title', 'No Title')[:100]}..."):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Summary:** {article.get('summary', 'No summary available')[:300]}...")
                            st.write(f"**Source:** {article.get('source', 'Unknown')}")
                            if article.get('url'):
                                st.link_button("Read Full Article", article['url'])
                        
                        with col2:
                            sentiment = article.get('overall_sentiment_label', 'Neutral')
                            sentiment_score = article.get('overall_sentiment_score', 0)
                            
                            if sentiment == 'Bullish':
                                st.success(f"🟢 {sentiment}")
                            elif sentiment == 'Bearish':
                                st.error(f"🔴 {sentiment}")
                            else:
                                st.info(f"🟡 {sentiment}")
                            
                            st.metric("Score", f"{float(sentiment_score):.3f}")
        
        else:
            st.info("Analysis view not yet implemented for this API function")
            st.json(data)
    
    with tab2:
        # Raw JSON view
        st.subheader("Raw API Response")
        st.json(st.session_state.api_data)
    
    with tab3:
        # Download options
        st.subheader("Download Results")
        
        # JSON download
        json_str = json.dumps(st.session_state.api_data, indent=2)
        st.download_button(
            label="📄 Download JSON",
            data=json_str,
            file_name=f"{api_function}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        # CSV download (if applicable)
        if api_function == "ANALYTICS_FIXED_WINDOW" and 'payload' in st.session_state.api_data:
            results_data = []
            for symbol, metrics in st.session_state.api_data['payload'].items():
                row = {'Symbol': symbol}
                row.update(metrics)
                results_data.append(row)
            
            if results_data:
                df = pd.DataFrame(results_data)
                csv = df.to_csv(index=False)
                st.download_button(
                    label="📊 Download CSV",
                    data=csv,
                    file_name=f"{api_function}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    with tab4:
        # Visualizations
        st.subheader("Data Visualizations")
        
        if api_function == "ANALYTICS_FIXED_WINDOW" and 'payload' in st.session_state.api_data:
            # Create visualizations for analytics data
            results_data = []
            for symbol, metrics in st.session_state.api_data['payload'].items():
                row = {'Symbol': symbol}
                row.update(metrics)
                results_data.append(row)
            
            if results_data:
                df = pd.DataFrame(results_data)
                
                # Returns comparison
                if 'CUMULATIVE_RETURN' in df.columns:
                    fig = px.bar(df, x='Symbol', y='CUMULATIVE_RETURN', 
                               title="Cumulative Returns by Symbol")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Risk vs Return scatter
                if 'MEAN' in df.columns and 'STDDEV' in df.columns:
                    fig = px.scatter(df, x='STDDEV', y='MEAN', text='Symbol',
                                   title="Risk vs Return Analysis",
                                   labels={'STDDEV': 'Risk (Standard Deviation)', 
                                          'MEAN': 'Expected Return'})
                    fig.update_traces(textposition="top center")
                    st.plotly_chart(fig, use_container_width=True)
        
        elif api_function == "NEWS_SENTIMENT" and 'feed' in st.session_state.api_data:
            # Sentiment distribution
            articles = st.session_state.api_data['feed']
            if articles:
                sentiments = [article.get('overall_sentiment_label', 'Neutral') for article in articles]
                sentiment_counts = pd.Series(sentiments).value_counts()
                
                fig = px.pie(values=sentiment_counts.values, names=sentiment_counts.index,
                           title="News Sentiment Distribution")
                st.plotly_chart(fig, use_container_width=True)
                
                # Sentiment over time (if timestamp available)
                sentiment_scores = []
                timestamps = []
                for article in articles:
                    if 'time_published' in article:
                        sentiment_scores.append(float(article.get('overall_sentiment_score', 0)))
                        timestamps.append(article['time_published'])
                
                if sentiment_scores and timestamps:
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=timestamps[:20], y=sentiment_scores[:20],
                                           mode='lines+markers', name='Sentiment Score'))
                    fig.update_layout(title="Sentiment Score Over Time (Recent 20 Articles)",
                                    xaxis_title="Time", yaxis_title="Sentiment Score")
                    st.plotly_chart(fig, use_container_width=True)
        
        else:
            st.info("Visualizations not yet implemented for this API function")

# Footer
st.divider()
st.markdown("Built with Streamlit • AlphaVantage API • Made for Financial Analysis")

# Development info in sidebar
with st.sidebar:
    st.divider()
    if st.checkbox("Show Debug Info"):
        st.subheader("Debug Information")
        st.write("Session State Keys:", list(st.session_state.keys()))
        if 'api_params' in st.session_state:
            st.write("Last API Params:", st.session_state.api_params)