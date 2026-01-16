import os 
import email.mime 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import requests 
import pandas as pd 
import json 

# ==================================================================================================================== # 
# Top Gainers, Losers, and Most Actively Traded Tickers (US Market) # 
# This endpoint returns the top 20 gainers, losers, and the most active traded tickers in the US market.


# API Parameters #
# 1. ❚ Required: function = EARNINGS_ESTIMATES

# 2. ❚ Required: apikey 
# ==================================================================================================================== #  
def market_movers(): 
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'TOP_GAINERS_LOSERS'  

    # Build API Params 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn,  
        'apikey': api_key
    } 

    # Build Request URL 
    market_movers_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(market_movers_url)  
    data = response.json() 

    
    Path('Market_Movers_JSON').mkdir(exist_ok=True) 

    filename = f'Market_Movers_JSON/{fn}.json' 
    with open (filename, 'w') as market_movers_json: 
        json.dump(data, market_movers_json, indent=2)  


    print(f'Successfully Saved Top Gainers & Losers to {filename}')  

if __name__ == '__main__': 
    market_movers()