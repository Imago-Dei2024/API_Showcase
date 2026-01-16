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

# TRIMA Introduction # 
# The Triangular Moving Average is a form of Weighted Moving Average wherein the weights are assigned in a triangular pattern. For example, the weights for a 7 period Triangular Moving Average would be 1, 2, 3, 4, 3, 2, 1. This gives more weight to the middle of the time series and less weight to the oldest and newest data.

# The Triangular Moving Average is mathematically equivalent to a Simple Moving Average of a Simple Moving Average. 

# ==================================================================================================================== #  
# API PAMETERS # 
# 1. function (required) = 'TRIMA' 
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
def trima_indicator():  
    load_dotenv() 

    api_key=os.getenv("ALPHA_VANTAGE_API_KEY") 

    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()  

    fn = 'TRIMA' 
    ticker = input('Enter Ticker: ') 
    days = int(input('How many Days?: '))  

    # Build Url 
    base_url = 'https://www.alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': ticker, 
        'interval': 'daily', 
        'time_period': days, 
        'series_type': 'close',
        'apikey': api_key
    } 

    trima_url = f'{base_url}?{urlencode(params)}' 

    response = requests.get(trima_url) 
    data = response.json() 

    Path('Technical_Indicators_JSON').mkdir(exist_ok=True)

    filename = f'Technical_Indicators_JSON/{ticker}_{days}_Day_{fn}.json' 
    with open (filename, 'w') as trima_file: 
        json.dump(data, trima_file, indent = 2)  

# ==================================================================================================================== # 
if __name__ == '__main__': 
    trima_indicator() 
