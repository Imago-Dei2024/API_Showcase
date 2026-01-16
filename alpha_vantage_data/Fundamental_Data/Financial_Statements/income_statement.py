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
# 1. function = 'INCOME_STATEMENT' 
# 2. symbol 
# 3. apikey 
def fetch_income_statement(): 
    load_dotenv() 

    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')  

    if not api_key: 
        print('ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory') 
        exit() 

    ticker = input('Enter Ticker: ') 

    # Format API URL 
    base_url = 'https://alphavantage.co/query' 
    params = { 
        'function': 'INCOME_STATEMENT', 
        'symbol': ticker, 
        'apikey': api_key 
    } 

    # Build URL With Params 
    Income_Statement_URL = f'{base_url}?{urlencode(params)}' 

    # Download and Save Data As JSON File 
    response = requests.get(Income_Statement_URL) 
    data = response.json()  

    Path('p_sql_two/Income_Statements_JSON').mkdir(exist_ok=True) 

    # Save the File 
    filename = f'p_sql_two/Income_Statements_JSON/{ticker}_Income_Statement.json' 
    with open(filename, 'w') as income_statement: 
        json.dump(data, income_statement, indent=2)  



if __name__ == '__main__': 
    fetch_income_statement() 