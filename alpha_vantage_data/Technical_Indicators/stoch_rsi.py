from email.mime import base
import os
import re 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 

from rich.console import Console 
from rich.panel import Panel 
from rich.text import Text 
console = Console() 

import csv 
import requests 
import pandas as pd 

# ==================================================================================================================== # 
# STOCHRSI - Stochastic Relative Strength Index # 
# This API returns the stochastic relative strength index (STOCHRSI) values. See also: mathematical reference.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The technical indicator of your choice. In this case, function=STOCHRSI

# 2. ❚ Required: symbol - The name of the ticker of your choice. For example: symbol=IBM

# 3. ❚ Required: interval - Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly

# 4. ❚ Optional: month - Note: this parameter is ONLY applicable to intraday intervals for the equity markets

# 5. ❚ Required: time_period - Number of data points used to calculate each STOCHRSI value. Positive integers are accepted

# 6. ❚ Required: series_type - The desired price type in the time series. Four types are supported: close, open, high, low

# 7. ❚ Optional: fastkperiod - The time period of the fastk moving average. By default, fastkperiod=5

# 8. ❚ Optional: fastdperiod - The time period of the fastd moving average. By default, fastdperiod=3

# 9. ❚ Optional: fastdmatype - Moving average type for the fastd moving average. By default, fastdmatype=0

# 10. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted

# 11. ❚ Required: apikey - Your API key

# ==================================================================================================================== #
def stochrsi_indicator():
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()

    # Get Symbol Input
    symbol = input("Enter Symbol: ").upper()

    # Select Interval
    while True:
        print(f"Please Select an Interval for {symbol}:")
        print("1. 1min")
        print("2. 5min") 
        print("3. 15min")
        print("4. 30min")
        print("5. 60min")
        print("6. daily")
        print("7. weekly")
        print("8. monthly")
        choice = input("Enter Choice (1-8): ")
        
        interval_map = {
            '1': '1min', '2': '5min', '3': '15min', '4': '30min', 
            '5': '60min', '6': 'daily', '7': 'weekly', '8': 'monthly'
        }
        if choice in interval_map:
            interval = interval_map[choice]
            break
        else:
            print('Invalid Choice. Please Select 1-8.\n')

    # Get Time Period
    while True:
        try:
            time_period = int(input("Enter Time Period (common: 14, 21, 30): "))
            if time_period > 0:
                break
            else:
                print("Time period must be a positive integer.\n")
        except ValueError:
            print("Please enter a valid positive integer.\n")

    # Select Series Type
    while True:
        print("Please Select Series Type:")
        print("1. close")
        print("2. open") 
        print("3. high")
        print("4. low")
        choice = input("Enter Choice (1-4): ")
        
        series_map = {'1': 'close', '2': 'open', '3': 'high', '4': 'low'}
        if choice in series_map:
            series_type = series_map[choice]
            break
        else:
            print('Invalid Choice. Please Select 1-4.\n')

    # Optional Parameters
    print("\nOptional Parameters (press Enter for defaults):")
    
    fastkperiod_input = input("Fast K period (default: 5): ")
    fastkperiod = 5 if fastkperiod_input == "" else int(fastkperiod_input)
    
    fastdperiod_input = input("Fast D period (default: 3): ")
    fastdperiod = 3 if fastdperiod_input == "" else int(fastdperiod_input)

    # Fast D Moving Average Type
    print("\nFast D Moving Average Type:")
    print("0. SMA - Simple Moving Average")
    print("1. EMA - Exponential Moving Average") 
    print("2. WMA - Weighted Moving Average")
    print("3. DEMA - Double Exponential Moving Average")
    print("4. TEMA - Triple Exponential Moving Average")
    print("5. TRIMA - Triangular Moving Average")
    print("6. T3 - T3 Moving Average")
    print("7. KAMA - Kaufman Adaptive Moving Average")
    print("8. MAMA - MESA Adaptive Moving Average")
    
    fastdmatype_input = input("Enter Fast D MA Type (0-8, default: 0): ")
    fastdmatype = 0 if fastdmatype_input == "" else int(fastdmatype_input)

    # API url Format with Parameters
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'STOCHRSI',
        'symbol': symbol,
        'interval': interval,
        'time_period': time_period,
        'series_type': series_type,
        'fastkperiod': fastkperiod,
        'fastdperiod': fastdperiod,
        'fastdmatype': fastdmatype,
        'apikey': api_key,
        'datatype': 'csv',
        'entitlement': 'realtime'
    }

    # Build CSV URL with params
    CSV_URL = f"{base_url}?{urlencode(params)}"

    # Download and save the csv
    response = requests.get(CSV_URL)
    Path('Technical_Indicators').mkdir(exist_ok=True)

    filename = f"Technical_Indicators/{symbol}_STOCHRSI_{time_period}_{interval}_{series_type}.csv"
    with open(filename, 'w') as file:
        file.write(response.text)

    print(f"Successfully Downloaded STOCHRSI Indicator for {symbol} to {filename}")

    # Rename the Column names of the CSV
    print(f'Converting Column names for {filename}...')

    df = pd.read_csv(filename)

    # Define the Column Mapping
    column_mapping = {
        'time': 'Date',
        'FastK': f'FastK_{fastkperiod}',
        'FastD': f'FastD_{fastdperiod}'
    }

    # Rename Column names Using Mapping
    df.rename(columns=column_mapping, inplace=True)

    # Save Updated CSV
    df.to_csv(filename, index=False)

    print(f'Column names Successfully Converted for {filename}')

   

if __name__ == '__main__':
    stochrsi_indicator()