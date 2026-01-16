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
 
# VWAP Introduction # 
# See Link Below for Informaon About the Volume Weighted Average Price (VWAP) for intraday time series: 
# https://www.investopedia.com/terms/v/vwap.asp 

# ==================================================================================================================== #  
# API PAMETERS # 
# 1. function (required) = 'VWAP' 
# 2. symbol (required)
# 3. interval (required) - (time interval between two consecutive data points in time series) 
#    a. 1min 
#    b. 5min 
#    c. 15min 
#    d. 30min 
#    e. 60min 

# 4. datatype (optional)  
#    a. json (default) 
#    b. csv 

# 5. apikey (required) 
# ==================================================================================================================== #  
def vwap_indicator(): 
    load_dotenv() 

    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 

    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 

    fn = 'VWAP' 
    ticker = input("Enter Ticker for VWAP: ") 

    # Select Time Interval Logic 
    while True: 
        print('Please Select Time Interval In Between Data Points: ') 
        print('1. 1 Minute ') 
        print('2. 5 Minute ') 
        print('3. 15 Minute ') 
        print('4. 30 Minute ') 
        print('5. 60 Minute ')  
        choice = input('Select 1 - 5: ') 

        if choice == '1': 
            interval_choice = '1min' 
            break 

        elif choice == '2': 
            interval_choice = '5min' 
            break 

        elif choice == '3': 
            interval_choice = '15min' 
            break 

        elif choice == '4':
            interval_choice = '30min' 
            break 

        elif choice == '5': 
            interval_choice = '60min' 
            break 

        else: 
            print("Please Select a Valid Time Interval (1 - 5)...")  


    # Format Request URL 
    base_url = 'https://www.alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': ticker, 
        'interval': interval_choice, 
        'datatype': 'csv', 
        'apikey': api_key
    } 

    # Build Request URL 
    vwap_csv_url = f'{base_url}?{urlencode(params)}' 

    # Fetch Data and Save as CSV 
    response = requests.get(vwap_csv_url) 
    Path('Technical_Indicators_CSV').mkdir(exist_ok=True)  

    filename = f'Technical_Indicators_CSV/{ticker}_{interval_choice}_{fn}.csv' 
    with open (filename, 'w') as csv_file: 
        csv_file.write(response.text) 


if __name__ == '__main__': 
    vwap_indicator()