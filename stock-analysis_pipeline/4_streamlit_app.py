# ==================================================================================================================== # 
# Streamlit Dashboard: Interactive web dashboard displaying company information, financial metrics,
# valuation ratios, profitability metrics, financial statements, earnings history, and corporate actions
# ==================================================================================================================== #  

import streamlit as st 
import json 
from pathlib import Path 
import pandas as pd 
from datetime import datetime 

st.set_page_config( 
    page_title="Stock Fundamental Analysis", 
    page_icon="♠︎", 
    layout="wide"
)   

def load_formatted_data(ticker): 
    data_file = Path('data')/f'{ticker}_formatted_data.json' 
    if not data_file.exists(): 
        return None 
    with open(data_file, 'r') as f: 
        return json.load(f) 
    
def display_company_info(data): 
    st.header("♦︎ Company Information") 

    col1, col2 = st.columns(2) 

    with col1: 
        st.markdown(f"**Company Name:** {data['Company Name']}") 
        st.markdown(f"**Symbol:** {data['Symbol']}") 
        st.markdown(f"**Exchange:** {data['Exchange']}")  

    with col2: 
        st.markdown(f"**Sector:** {data['Sector']}") 
        st.markdown(f"**Industry:** {data['Industry']}") 
    
    with st.expander("📝 Company Description"): 
        st.write(data['Description']) 

def display_metrics_card(metrics, title): 
    st.subheader(title) 
    cols = st.columns(3) 

    items = list(metrics.items()) 
    for idx, (key, value) in enumerate(items): 
        with cols[idx % 3]: 
            st.metric(label=key, value=value) 

def display_financial_summary(data): 
    st.header("💰 Financial Summary") 


    col1, col2 = st.columns(2) 
    
    with col1: 
        st.subheader("📊 Key Metrics") 
        for key, value in data['financial_metrics'].items(): 
            st.metric(label=key, value=value) 

    with col2: 
        st.subheader("📈 Valuation Ratios") 
        for key, value in data['valuation_metrics'].items(): 
            st.metric(label=key, value=value) 

def display_profitability(data): 
    st.header("💹 Profitability & Per Share Metrics") 

    col1, col2 = st.columns(2) 

    with col1: 
        st.subheader("🎯 Profitability") 
        for key, value in data['profitability_metrics'].items(): 
            st.metric(label=key, value=value) 

    with col2: 
        st.subheader("💵 Per Share Data")
        for key, value in data['per_share_metrics'].items(): 
            st.metric(label=key, value=value) 

def display_financial_statements(data): 
    st.header("🗒️ Financial Statements") 

    tab1, tab2, tab3 = st.tabs(["Balance Sheet", "Income Statement", "Cash Flow"]) 

    with tab1: 
        st.subheader("Balance Sheet") 
        df = pd.DataFrame([data['balance_sheet']]).T 
        df.columns = ['Value'] 
        st.dataframe(df, use_container_width=True) 

    with tab2: 
        st.subheader("Income Statement") 
        df = pd.DataFrame([data['income_statement']]).T 
        df.columns = ['Value'] 
        st.dataframe(df, use_container_width=True) 
    
    with tab3: 
        st.subheader("Cash Flow") 
        df = pd.DataFrame([data['cash_flow']]).T 
        df.columns = ['Value'] 
        st.dataframe(df, use_container_width=True)  

def display_earnings(data):
    st.header("📊 Earnings History & Forecast")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Quarterly Earnings")
        if data['earnings']['Quarterly Earnings']:
            df = pd.DataFrame(data['earnings']['Quarterly Earnings'])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No quarterly earnings data available")
    
    with col2:
        st.subheader("Annual Earnings")
        if data['earnings']['Annual Earnings']:
            df = pd.DataFrame(data['earnings']['Annual Earnings'])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No annual earnings data available")
    
    with col3:
        st.subheader("📅 Upcoming Earnings")
        if data['earnings']['Upcoming Earnings']:
            df = pd.DataFrame(data['earnings']['Upcoming Earnings'])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No upcoming earnings data available")

def display_corporate_actions(data):
    st.header("🎯 Corporate Actions")
    
    st.subheader("💵 Dividend History")
    if data['corporate_actions']['Dividends']:
        df = pd.DataFrame(data['corporate_actions']['Dividends'])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No dividend data available") 


def main(): 
    st.title("📈 Stock Fundamental Analysis Dashboard") 
    st.markdown("---") 

    ticker_input = st.text_input("Enter Symbol:", value="", placeholder="e.g., AAPL, MSFT") 

    if ticker_input: 
        ticker = ticker_input.upper() 
        data = load_formatted_data(ticker) 

        if data is None: 
            st.error(f"❌ No data found for {ticker}. Please run the data fetcher first.") 
            st.info("Run: 'python run_pipeline.py TICKER' or `python data_fetcher.py` → `python data_extractor.py` → `python data_formatter.py`") 

        else: 
            st.success(f"✅ Data loaded for {ticker}") 

            display_company_info(data['company_info']) 
            st.markdown("---") 

            display_financial_summary(data) 
            st.markdown("---") 

            display_profitability(data) 
            st.markdown("---") 

            display_financial_statements(data) 
            st.markdown("---") 
            
            display_earnings(data) 
            st.markdown("---") 

            display_corporate_actions(data) 

            st.markdown("---") 
            st.caption(f"Data generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}") 

if __name__ == '__main__': 
    main() 