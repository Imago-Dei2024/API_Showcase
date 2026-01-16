from email.mime import base 
import os 
import re 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import csv 
import requests 
import pandas as pd  
import json   

# API PAMETERS # 
# 1. function = 'CASH_FLOW' 
# 2. symbol 
# 3. apikey  


def fetch_cash_flow_statement(): 

    load_dotenv() 
    api_key=os.getenv("ALPHA_VANTAGE_API_KEY") 

    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 

    ticker = input("Enter Ticker: ") 
    fn = 'CASH_FLOW' 

    # Format API Url
    base_url = 'https://www.alphavantage.co/query' 
    params={ 
        'function': fn, 
        'symbol': ticker, 
        'apikey': api_key
    } 

    # Build Request URL 
    Cash_Flow_URL = f'{base_url}?{urlencode(params)}' 

    # Fetch and Format as JSON 
    response = requests.get(Cash_Flow_URL) 
    data = response.json() 

    Path("Cash_Flow_Statements_JSON").mkdir(exist_ok=True) 

    # Save Data 
    filename = f'Cash_Flow_Statements_JSON/{ticker}_Cash_Flow.json' 
    with open (filename, 'w') as cash_flow: 
        json.dump(data, cash_flow, indent=2) 


if __name__ == '__main__': 
    fetch_cash_flow_statement() 