import os 
import email.mime 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import requests 
import pandas as pd 
import json 

# ==================================================================================================================== # 
# Earnings Estimates Trending # 
# This API returns the annual and quarterly EPS and revenue estimates for the company of interest, along with analyst count and revision history.

# API Parameters #
# 1. ❚ Required: function = EARNINGS_ESTIMATES

# 2. ❚ Required: symbol - The symbol of the ticker of your choice. For example: symbol=QQQ.

# 3. ❚ Required: apikey 
# ==================================================================================================================== #  
def fetch_fetch_earnings_estimates(): 
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'EARNINGS_ESTIMATES' 
    ticker = input('Enter Ticker: ') 

    # Build API Params 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': ticker, 
        'apikey': api_key
    } 

    # Build Request URL 
    earnings_estimates_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(earnings_estimates_url)  
    data = response.json() 
    Path('p_sql_two/Earnings_JSON').mkdir(exist_ok=True) 

    filename = f'p_sql_two/Earnings_JSON/{ticker}_{fn}.json' 
    with open (filename, 'w') as earnings_estimates_json: 
        json.dump(data, earnings_estimates_json, indent=2) 


    print(f'Successfully Saved Realtime Options Data for {ticker} as {filename}')  

if __name__ == '__main__': 
    fetch_fetch_earnings_estimates()