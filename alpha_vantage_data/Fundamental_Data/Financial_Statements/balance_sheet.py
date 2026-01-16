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
# 1. function = 'BALANCE_SHEET' 
# 2. symbol 
# 3. apikey 


def fetch_balance_sheet(): 

    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")  

    if not api_key: 
        print('ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory') 
        exit()  

    ticker = input("Enter Ticker: ") 
    fn = 'BALANCE_SHEET' 

    base_url = 'https://alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': ticker, 
        'apikey': api_key 
    } 

    # Build URL 
    Balance_Sheet_URL = f'{base_url}?{urlencode(params)}' 

    # Fetch and Format Data 
    response = requests.get(Balance_Sheet_URL) 
    data = response.json() 

    # Store it 
    Path('p_sql_two/Balance_Sheets_JSON').mkdir(exist_ok=True) 

    # Save It 
    filename=f'p_sql_two/Balance_Sheets_JSON/{ticker}_Balance_Sheet.json' 
    with open(filename, 'w') as balance_sheet: 
        json.dump(data, balance_sheet, indent=2) 

if __name__ == '__main__': 
    fetch_balance_sheet() 