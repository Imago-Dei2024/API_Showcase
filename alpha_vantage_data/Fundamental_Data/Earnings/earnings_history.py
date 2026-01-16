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
# 1. ❚ Required: function = EARNINGS

# 2. ❚ Required: symbol - The symbol of the ticker of your choice. For example: symbol=QQQ.

# 3. ❚ Required: apikey 
# ==================================================================================================================== #  
def fetch_earnings_history(): 
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'EARNINGS' 
    ticker = input('Enter Ticker: ') 

    # Build API Params 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': ticker, 
        'apikey': api_key
    } 

    # Build Request URL 
    earnings_history_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(earnings_history_url)  
    data = response.json() 
    Path('Earnings_CSV/Earnings_History').mkdir(exist_ok=True) 

    filename = f'Earnings_CSV/Earnings_History/{ticker}_{fn}.json' 
    with open (filename, 'w') as earnings_history_json: 
        json.dump(data, earnings_history_json, indent=2) 


    print(f'Successfully Saved Realtime Options Data for {ticker} as {filename}')   

if __name__ == '__main__': 
    fetch_earnings_history()
