import os 
import email.mime 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import requests 
import pandas as pd 
import json 

# ==================================================================================================================== # 
# ETF Profile & Holdings
# This API returns key ETF metrics (e.g., net assets, expense ratio, and turnover), along with the corresponding ETF holdings / constituents with allocation by asset types and sectors.


# API Parameters #
# 1. ❚ Required: function = ETF_PROFILE

# 2. ❚ Required: symbol - The symbol of the ticker of your choice. For example: symbol=QQQ.

# 3. ❚ Required: apikey 
# ==================================================================================================================== # 
def fetch_etf_holdings(): 
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'ETF_PROFILE' 
    etf_ticker = input('Enter ETF Ticker: ') 

    # Build API Params 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': etf_ticker, 
        'apikey': api_key
    } 

    # Build Request URL 
    etf_holdings_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(etf_holdings_url)  
    data = response.json() 
    Path('ETF_Holdings_JSON').mkdir(exist_ok=True) 

    filename = f'ETF_Holdings_JSON/{etf_ticker}_{fn}.json' 
    with open (filename, 'w') as etf_holdings: 
        json.dump(data, etf_holdings, indent=2) 


    print(f'Successfully Saved Realtime Options Data for {etf_ticker} as {filename}')  

if __name__ == '__main__': 
    fetch_etf_holdings()
