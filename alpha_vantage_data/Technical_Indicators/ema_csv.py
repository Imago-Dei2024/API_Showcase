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
# 1. function (required) = 'EMA' 
# 2. symbol (required)
# 3. interval (required) - (time interval between two consecutive data points in time series) 
#    a. 1min 
#    b. 5min 
#    c. 15min 
#    d. 30min 
#    e. 60min 
#    f. daily 
#    g. weekly 
#    h. monthly

# 4. time_period (required) -> Number of Data Points used to Calculate each moving Average value: 
#    a. 60 
#    b. 200 

# 5. series_type (required) -> Desired Price Type in Series 
#    a. close 
#    b. open 
#    c. high 
#    d. low 

# 6. datatype (optional)  
#    a. json (default) 
#    b. csv 

# 7. apikey (required)  

# ==================================================================================================================== #  
def fetch_ema(): 
    load_dotenv() 

    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')  

    if not api_key: 
        print('ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory') 
        exit() 

    fn = 'EMA'
    ticker = input('Enter Ticker: ') 
    days = int(input("How Many Days: "))

    # Format API URL 
    base_url = 'https://www.alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': ticker, 
        'interval': 'daily', 
        'time_period': days,
        'series_type': 'close', 
        'datatype': 'csv',
        'entitlement': 'realtime',
        'apikey': api_key
    } 

    # Build URL 
    ema_csv_url = f'{base_url}?{urlencode(params)}' 

    response = requests.get(ema_csv_url) 

    Path('Technical_Indicators_CSV').mkdir(exist_ok=True)  

    filename = f'Technical_Indicators_CSV/{ticker}_{days}_{fn}.csv' 
    with open (filename, 'w') as csv_file: 
        csv_file.write(response.text)  

    # Rename Columns 'time' and 'value' to 'Date' and 'EMA{days} 
    df = pd.read_csv(filename) 
    df = df.rename(columns={'time': 'Date', 'EMA': f'EMA{days}'}) 
    df.to_csv(filename, index=False)

if __name__ == '__main__': 
    fetch_ema() 