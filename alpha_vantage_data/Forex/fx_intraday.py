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
# FX_INTRADAY - Forex Intraday Time Series # 
# This API returns intraday time series (timestamp, open, high, low, close) of the FX currency pair specified, updated realtime.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The time series of your choice. In this case, function=FX_INTRADAY

# 2. ❚ Required: from_symbol - A three-letter symbol from the forex currency list. For example: from_symbol=EUR

# 3. ❚ Required: to_symbol - A three-letter symbol from the forex currency list. For example: to_symbol=USD

# 4. ❚ Required: interval - Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min

# 5. ❚ Optional: outputsize - By default, outputsize=compact. Strings compact and full are accepted

# 6. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted

# 7. ❚ Required: apikey - Your API key

# ==================================================================================================================== #
def fx_intraday():
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()

    # Get Currency Pair Input
    from_symbol = input("Enter FROM currency (3-letter code, e.g., EUR): ").upper()
    to_symbol = input("Enter TO currency (3-letter code, e.g., USD): ").upper()

    # Validate currency codes (basic length check)
    if len(from_symbol) != 3 or len(to_symbol) != 3:
        print("Error: Currency codes must be exactly 3 letters.")
        return

    # Select Interval
    while True:
        print(f"Please Select an Interval for {from_symbol}/{to_symbol}:")
        print("1. 1min")
        print("2. 5min") 
        print("3. 15min")
        print("4. 30min")
        print("5. 60min")
        choice = input("Enter Choice (1-5): ")
        
        interval_map = {'1': '1min', '2': '5min', '3': '15min', '4': '30min', '5': '60min'}
        if choice in interval_map:
            interval = interval_map[choice]
            break
        else:
            print('Invalid Choice. Please Select 1-5.\n')

    # Select Output Size
    while True:
        print(f"Please Select an Output Size for {from_symbol}/{to_symbol}:")
        print("1. Compact - Latest 100 data points")
        print("2. Full - Full-length intraday series")
        choice = input("Enter Choice (1 or 2): ")

        if choice == '1':
            output_size = 'compact'
            break
        elif choice == '2':
            output_size = 'full'
            break
        else:
            print('Invalid Choice. Please Select 1 or 2.\n')

    # API url Format with Parameters
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'FX_INTRADAY',
        'from_symbol': from_symbol,
        'to_symbol': to_symbol,
        'interval': interval,
        'outputsize': output_size,
        'apikey': api_key,
        'datatype': 'csv'
    }

    # Build CSV URL with params
    CSV_URL = f"{base_url}?{urlencode(params)}"

    # Download and save the csv
    response = requests.get(CSV_URL)
    Path('Forex_Data').mkdir(exist_ok=True)

    filename = f"Forex_Data/{from_symbol}_{to_symbol}_{interval}_intraday.csv"
    with open(filename, 'w') as file:
        file.write(response.text)

    print(f"Successfully Downloaded FX Intraday Data for {from_symbol}/{to_symbol} ({interval}) to {filename}")

    # Rename the Column names of the CSV
    print(f'Converting Column names for {filename}...')

    df = pd.read_csv(filename)

    # Define the Column Mapping
    column_mapping = {
        'timestamp': 'Timestamp',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close'
    }

    # Rename Column names Using Mapping
    df.rename(columns=column_mapping, inplace=True)

    # Save Updated CSV
    df.to_csv(filename, index=False)

    print(f'Column names Successfully Converted for {filename}')


if __name__ == '__main__':
    fx_intraday()