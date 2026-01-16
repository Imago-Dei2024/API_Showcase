import email.mime 
import os 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import requests 
import pandas as pd 
import csv 

# ==================================================================================================================== # 
# Digital Current Weekly Data # 
# This API returns the weekly historical time series for a cryptocurrency (e.g., BTC) traded on a specific market (e.g., EUR/Euro), refreshed daily at midnight (UTC). Prices and volumes are quoted in both the market-specific currency and USD.

# API Parameters #
# 1. ❚ Required: function = DIGITAL_CURRENCY_WEEKLY

# 2. ❚ Required: symbol - The digital/crypto currency of your choice. It can be any of the currencies in the digital currency list. For example: symbol=ETH.

# 3. ❚ Required: market - The exchange market of your choice. It can be any of the market in the market list. For example: market=USD.

# 4. ❚ Required: apikey

# 5. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the daily time series in JSON format; csv returns the time series as a CSV (comma separated value) file.

# ==================================================================================================================== #  

def crypto_weekly(): 
    load_dotenv() 

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'DIGITAL_CURRENCY_WEEKLY' 
    crypto_ticker = input('Enter Ticker: ') 
    market = 'USD' 
   


    # Build URL 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': crypto_ticker, 
        'market': market,  
        'apikey': api_key,
        'datatype': 'csv'
    }  

    # Build Request URL 
    crypto_weekly_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(crypto_weekly_url) 
    Path('Crypto_Weekly_Data').mkdir(exist_ok=True)  

    filename = f'Crypto_Weekly_Data/{crypto_ticker}_{fn}.csv' 
    with open (filename, 'w') as csv_file: 
        csv_file.write(response.text) 

    print(f'Successfully Saved Weekly Crypto Data for {crypto_ticker} as {filename}')  

if __name__ == '__main__': 
    crypto_weekly()