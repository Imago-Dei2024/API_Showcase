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

# Introdution to Average Directional Movement Index (ADX) # 
# Technical Indicator Used by Traders to determine the Strength of a Financial Securities Price Trend. 
# Widely used to gauge the strength of a trend because it is so Reliable 
# The ADX is a Welles Wilder style moving average of the Directional Movement Index (DX). The values range from 0 to 100, but rarely get above 60. To interpret the ADX, consider a high number to be a strong trend, and a low number, a weak trend.

# For More Information about ADX, use below links: 
# Investopedia Article: https://www.investopedia.com/articles/trading/07/adx-trend-indicator.asp 
# Mathematical Reference: https://www.fmlabs.com/reference/default.htm?url=ADX.htm 

# ==================================================================================================================== #  
# API PAMETERS # 
# 1. function (required) = 'ADX' 
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

# 4. time_period (required) 
#    a. example: time_period=60, time_period=200 

# 6. datatype (optional)  
#    a. json (default) 
#    b. csv 

# 7. apikey (required) 
# ==================================================================================================================== #  
def adx_indicator(): 
    load_dotenv() 

    api_key=os.getenv("ALPHA_VANTAGE_API_KEY") 

    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()  

    fn = 'ADX' 
    ticker = input('Enter Ticker: ') 
    print('Intervals = 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly') 
    days = input("Enter Time Interval: ") 
    time_period_input = int(input('Enter Time Period (positive integer): ')) 

    # Build Url 
    base_url = 'https://www.alphavantage.co/query'  
    params =  { 
        'function': fn, 
        'symbol': ticker, 
        'interval': days,  
        'time_period': time_period_input, 
        'datatype': 'csv', 
        'apikey': api_key
    } 

    # Build Request URL  
    adx_csv_url = f'{base_url}?{urlencode(params)}' 

    # Download and Save CSV 
    response = requests.get(adx_csv_url)  
    Path('Technical_Indicators_CSV').mkdir(exist_ok="True") 

    filename = f'Technical_Indicators_CSV/{ticker}_daily_{fn}.csv' 
    with open (filename, 'w') as csv_file: 
        csv_file.write(response.text)   

if __name__ == '__main__': 
    adx_indicator()