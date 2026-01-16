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

# Introduction to Stochastic Oscillator (STOCH) # 
# The Stochastic Oscillator measures where the close is in relation to the recent trading range. The values range from zero to 100. %D values over 75 indicate an overbought condition; values under 25 indicate an oversold condition. When the Fast %D crosses above the Slow %D, it is a buy signal; when it crosses below, it is a sell signal. The Raw %K is generally considered too erratic to use for crossover signals.
# See Links Below For More Information About STOCH: 
# Investopedia Article: https://www.investopedia.com/terms/s/stochasticoscillator.asp
# Mathematical Reference: https://www.fmlabs.com/reference/default.htm?url=StochasticOscillator.htm

# ==================================================================================================================== # 
# API PAMETERS # 
# 1. function (required) = 'STOCH' 
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

# 4. slowkmatype (optional) -> Moving Average Type for Slowk Moving Average 
#    a. 0 = SMA (default)
#    b. 1 = EMA 
#    c. 2 = WMA 
#    d. 3 = DEMA 
#    e. 4 = TEMA 
#    g. 5 = TRIMA 
#    h. 6 = T3 Moving Average 
#    j. 7 = KAMA 
#    k. 8 = MAMA 

# 5. slowmatype (optional) -> Moving Average for Slowd Moving Average  
#    a. - k. (see step 5 for same options) 

# 6. datatype (optional)  
#    a. json (default) 
#    b. csv 

# 7. apikey (required)
# ==================================================================================================================== #  
def stoch_indicator(): 
    load_dotenv() 

    api_key=os.getenv("ALPHA_VANTAGE_API_KEY") 

    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()  

    fn = 'STOCH' 
    ticker = input('Enter Ticker: ') 
    print('Intervals = 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly') 
    days = input("Enter Time Interval: ") 
    print('Available Types for Slowk & Slowm') 
    print('1. SMA, 2. EMA, 3. WMA, 4. TEMA, 5. TRIMA, 6. T3 Moving Averages, 7. KAMA, 8. MAMA') 
    slowk_choice = int(input("Select Slowk MA Type (1 - 8): ")) 
    slowd_choice = int(input("Select Slowd MA Type (1 - 8): ")) 

    # Build Url 
    base_url = 'https://www.alphavantage.co/query'  
    params =  { 
        'function': fn, 
        'symbol': ticker, 
        'interval': 'daily', 
        'slowkmatype': slowk_choice,  
        'slowdmatype': slowd_choice, 
        'datatype': 'csv', 
        'apikey': api_key
    } 

    # Build Request URL  
    stoch_csv_url = f'{base_url}?{urlencode(params)}' 

    # Download and Save CSV 
    response = requests.get(stoch_csv_url)  
    Path('Technical_Indicators_CSV').mkdir(exist_ok="True") 

    filename = f'Technical_Indicators_CSV/{ticker}_daily_{fn}.csv' 
    with open (filename, 'w') as csv_file: 
        csv_file.write(response.text)  

if __name__ == '__main__': 
    stoch_indicator() 