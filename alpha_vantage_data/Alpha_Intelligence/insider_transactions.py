import os 
import email.mime 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import requests 
import pandas as pd 
import json 

# ==================================================================================================================== # 
# Insider Transactions Trending
# This API returns the latest and historical insider transactions made by key stakeholders (e.g., founders, executives, board members, etc.) of a specific company.


# API Parameters #
# 1. ❚ Required: function = INSIDER_TRANSACTIONS

# 2. ❚ Required: symbol - The symbol of the ticker of your choice. For example: symbol=QQQ.

# 3. ❚ Required: apikey 
# ==================================================================================================================== #  
def fetch_insider_transactions(): 
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'INSIDER_TRANSACTIONS'  
    ticker = input('Enter Ticker: ') 

    # Build API Params 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn,  
        'symbol': ticker, 
        'apikey': api_key
    } 

    # Build Request URL 
    insider_transactions_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(insider_transactions_url)  
    data = response.json() 
    Path('Insider_Transactions_JSON').mkdir(exist_ok=True) 

    filename = f'Insider_Transactions_JSON/{fn}.json' 
    with open (filename, 'w') as insider_transactions_json: 
        json.dump(data, insider_transactions_json, indent=2)  


    print(f'Successfully Saved Top Gainers & Losers to {filename}')  

if __name__ == '__main__': 
    fetch_insider_transactions() 