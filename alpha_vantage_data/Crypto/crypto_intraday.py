import email.mime 
import os 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import requests 
import pandas as pd 
import csv 

# ==================================================================================================================== # 
# This API returns intraday time series (timestamp, open, high, low, close, volume) of the cryptocurrency specified, updated realtime.

# API Parameters #
# 1. ❚ Required: function = CRYPTO_INTRADAY

# 2. ❚ Required: symbol - The digital/crypto currency of your choice. It can be any of the currencies in the digital currency list. For example: symbol=ETH.

# 3. ❚ Required: market - The exchange market of your choice. It can be any of the market in the market list. For example: market=USD.

# 4. ❚ Required: interval - Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min

# 5. ❚ Optional: outputsize - By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns the full-length intraday time series. The "compact" option is recommended if you would like to reduce the data size of each API call.

# 6. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the intraday time series in JSON format; csv returns the time series as a CSV (comma separated value) file.

# 7. ❚ Required: apikey
# ==================================================================================================================== #  

def crypto_intraday(): 
    load_dotenv() 

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'CRYPTO_INTRADAY' 
    crypto_ticker = input('Enter Ticker: ') 
    market = 'USD' 
    print("Supported Intervals (time between two consecutive data points): 1min, 5min, 15min, 30min, 60min") 
    data_interval = input("Enter a Valid Time Interval: ") 
    print('Output Sizes: ') 
    print('1. compact (default) - 100 trading days') 
    print('2. full - all data') 
    data_size = input('Select Valid Output Size: ') 
    print('Two Datatypes Supported: JSON & CSV - For this Data we will save as CSV...') 
    format = 'csv'  


    # Build URL 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': crypto_ticker, 
        'market': market, 
        'interval': data_interval, 
        'outputsize': data_size, 
        'datatype': format, 
        'apikey': api_key
    }  

    # Build Request URL 
    crypto_intraday_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(crypto_intraday_url) 
    Path('Crypto_Intraday_CSV').mkdir(exist_ok=True)  

    filename = f'Crypto_Intraday_CSV/{crypto_ticker}_{fn}.csv' 
    with open (filename, 'w') as csv_file: 
        csv_file.write(response.text) 

    print(f'Successfully Saved Realtime Options Data for {crypto_ticker} as {filename}')  

if __name__ == '__main__': 
    crypto_intraday()