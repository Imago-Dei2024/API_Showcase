from email.mime import base
import os
import re 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 

# from rich.console import Console 
# from rich.panel import Panel 
# from rich.text import Text 
# console = Console() 

import csv 
import requests 
import pandas as pd 


# ==================================================================================================================== # 
# ==================================================================================================================== # 
# Time Series Weekly Stock Data # 
# This API returns monthly adjusted time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly adjusted close, monthly volume, monthly dividend) of the equity specified, covering 20+ years of historical data.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The time series of your choice. In this case, function=TIME_SERIES_MONTHLY_ADJUSTED

# 2. ❚ Required: symbol - The name of the equity of your choice. For example: symbol=IBM

# 3. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the weekly time series in JSON format; csv returns the time series as a CSV (comma separated value) file.

# 4. ❚ Required: apikey - Your API key

# ==================================================================================================================== #

# ==================================================================================================================== # 
# ==================================================================================================================== # 
def time_series_monthly_adjusted(): 
    load_dotenv() 
    api_key=os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()

    # Get Ticker Input
    ticker = input("Enter Ticker: ")

    # API url Format with Parameters
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_MONTHLY_ADJUSTED',
        'symbol': ticker,
        'apikey': api_key,
        'datatype': 'csv',
        'entitlement': 'realtime'
    }

    # Build CSV URL with params
    CSV_URL = f"{base_url}?{urlencode(params)}"

    # Download and save the csv
    response = requests.get(CSV_URL)
    Path('Monthly_Adjusted_Data').mkdir(exist_ok=True)

    filename = f"Monthly_Adjusted_Data/{ticker}_monthly_adjusted.csv"
    with open(filename, 'w') as file:
        file.write(response.text)

    print(f"Successfully Downloaded Monthly Adjusted Data for {ticker} to {filename}")

    # Rename the Column names of the CSV
    print(f'Converting Column names for {filename}...')

    df = pd.read_csv(filename)

    # Define the Column Mapping
    column_mapping = {
        'timestamp': 'Date',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'close': 'Close',
        'volume': 'Volume'
    }

    # Rename Column names Using Mapping
    df.rename(columns=column_mapping, inplace=True)

    # Save Updated CSV
    df.to_csv(filename, index=False)

    print(f'Column names Successfully Converted for {filename}')
# ==================================================================================================================== # 
# ==================================================================================================================== # 


if __name__ == '__main__':
    time_series_monthly_adjusted()