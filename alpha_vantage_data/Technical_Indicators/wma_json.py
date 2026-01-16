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

# WMA Introduction # 
# The Weighted Moving Average calculates a weight for each value in the series. The more recent values are assigned greater weights. The Weighted Moving Average is similar to a Simple Moving average in that it is not cumulative, that is, it only includes values in the time period (unlike an Exponential Moving Average). The Weighted Moving Average is similar to an Exponential Moving Average in that more recent data has a greater contribution to the average.

# ==================================================================================================================== # 
# API PAMETERS # 
# 1. function (required) = 'SMA' 
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

load_dotenv() 

api_key=os.getenv("ALPHA_VANTAGE_API_KEY") 

if not api_key: 
    print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
    exit()  

fn = 'WMA' 
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
    'datatype': 'json', 
    'apikey': api_key
} 

wma_url = f'{base_url}?{urlencode(params)}' 

response = requests.get(wma_url) 
data = response.json() 

Path('Technical_Indicators_JSON').mkdir(exist_ok=True)

filename = f'Technical_Indicators_JSON/{ticker}_{days}_Day_{fn}.json' 
with open (filename, 'w') as wma_file: 
    json.dump(data, wma_file, indent = 2)  

# ==================================================================================================================== #  
