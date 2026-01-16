from email.mime import base 
from email.quoprimime import body_check
import os 
import re 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import csv 
import requests 
import pandas as pd  
import json  

# MACD Introduction # 
# See Link Below for Information about the Moving Average Convergence/Divergence (MACD) 
# Mathematical Reference: https://www.fmlabs.com/reference/default.htm?url=MACD.htm 
# Investopedia Article: https://www.investopedia.com/articles/forex/05/macddiverge.asp 

# ==================================================================================================================== #  
# API PAMETERS # 
# 1. function (required) = 'MACD' 
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

# 4. series_type (required) -> Desired Price Type in Series 
#    a. close 
#    b. open 
#    c. high 
#    d. low 

# 6. datatype (optional)  
#    a. json (default) 
#    b. csv 

# 7. apikey (required)  
# ==================================================================================================================== #  

def get_macd(): 
    load_dotenv() 

    api_key=os.getenv("ALPHA_VANTAGE_API_KEY") 

    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()  

    fn = 'MACD' 
    ticker = input('Enter Ticker: ') 
    print('Intervals = 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly') 
    days = input("Enter Time Interval: ")

    # Build Url 
    base_url = 'https://www.alphavantage.co/query'  
    params =  { 
        'function': fn, 
        'symbol': ticker, 
        'interval': 'daily', 
        'series_type': 'close', 
        'datatype': 'csv', 
        'apikey': api_key
    } 

    # Build Request URL  
    macd_url = f'{base_url}?{urlencode(params)}' 

    # Download and Save CSV 
    response = requests.get(macd_url) 
    Path('Technical_Indicators_CSV').mkdir(exist_ok="True") 

    filename = f'Technical_Indicators_CSV/{ticker}_daily_{fn}.csv' 
    with open (filename, 'w') as macd_file: 
        macd_file.write(response.text) 

if __name__ == '__main__': 
    get_macd()