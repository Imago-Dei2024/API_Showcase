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
# WILLR - Williams' %R # 
# This API returns the Williams' %R (WILLR) values. See also: mathematical reference.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The technical indicator of your choice. In this case, function=WILLR

# 2. ❚ Required: symbol - The name of the ticker of your choice. For example: symbol=IBM

# 3. ❚ Required: interval - Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly

# 4. ❚ Optional: month - Note: this parameter is ONLY applicable to intraday intervals for the equity markets

# 5. ❚ Required: time_period - Number of data points used to calculate each WILLR value. Positive integers are accepted

# 6. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted

# 7. ❚ Required: apikey - Your API key

# ==================================================================================================================== #
def willr_indicator():
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
            time_period = int(input("Enter Time Period (common: 14, 21, 28): "))
            if time_period > 0:
                break
            else:
                print("Time period must be a positive integer.\n")
        except ValueError:
            print("Please enter a valid positive integer.\n")

    # API url Format with Parameters
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'WILLR',
        'symbol': symbol,
        'interval': interval,
        'time_period': time_period,
        'apikey': api_key,
        'datatype': 'csv',
        'entitlement': 'realtime'
    }

    # Build CSV URL with params
    CSV_URL = f"{base_url}?{urlencode(params)}"

    # Download and save the csv
    response = requests.get(CSV_URL)
    Path('Technical_Indicators').mkdir(exist_ok=True)

    filename = f"Technical_Indicators/{symbol}_WILLR_{time_period}_{interval}.csv"
    with open(filename, 'w') as file:
        file.write(response.text)

    print(f"Successfully Downloaded Williams' %R Indicator for {symbol} to {filename}")

    # Rename the Column names of the CSV
    print(f'Converting Column names for {filename}...')

    df = pd.read_csv(filename)

    # Define the Column Mapping
    column_mapping = {
        'time': 'Date',
        'WILLR': f'Williams_R_{time_period}'
    }

    # Rename Column names Using Mapping
    df.rename(columns=column_mapping, inplace=True)

    # Save Updated CSV
    df.to_csv(filename, index=False)

    print(f'Column names Successfully Converted for {filename}')

if __name__ == '__main__':
    willr_indicator()