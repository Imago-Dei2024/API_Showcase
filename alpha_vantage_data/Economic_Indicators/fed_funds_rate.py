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
# ==================================================================================================================== # 
# Federal Funds Rate Economic Data # 
# This API returns the daily, weekly, and monthly federal funds rate (interest rate) of the United States.
# Source: Board of Governors of the Federal Reserve System (US), Federal Funds Effective Rate, retrieved from FRED, Federal Reserve Bank of St. Louis (https://fred.stlouisfed.org/series/FEDFUNDS). This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The function of your choice. In this case, function=FEDERAL_FUNDS_RATE

# 2. ❚ Optional: interval - By default, interval=monthly. Strings daily, weekly, and monthly are accepted.

# 3. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file.

# 4. ❚ Required: apikey - Your API key

# ==================================================================================================================== #
def fed_funds_rate():
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()

    # Select Interval
    while True:
        print("Please Select an Interval for Federal Funds Rate Data:")
        print("1. Daily")
        print("2. Weekly")
        print("3. Monthly")
        choice = input("Enter Choice (1-3): ")
        
        if choice == '1':
            interval = 'daily'
            break
        elif choice == '2':
            interval = 'weekly'
            break
        elif choice == '3':
            interval = 'monthly'
            break
        else:
            print('Invalid Choice. Please Select 1-3.\n')

    # API url Format with Parameters
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'FEDERAL_FUNDS_RATE',
        'interval': interval,
        'apikey': api_key,
        'datatype': 'csv'
    }

    # Build CSV URL with params
    CSV_URL = f"{base_url}?{urlencode(params)}"

    # Download and save the csv
    response = requests.get(CSV_URL)
    Path('Economic_Data').mkdir(exist_ok=True)

    filename = f"Economic_Data/federal_funds_rate_{interval}.csv"
    with open(filename, 'w') as file:
        file.write(response.text)

    print(f"Successfully Downloaded Federal Funds Rate ({interval}) Data to {filename}")

    # Rename the Column names of the CSV
    print(f'Converting Column names for {filename}...')

    df = pd.read_csv(filename)

    # Define the Column Mapping
    column_mapping = {
        'date': 'Date',
        'value': 'Federal Funds Rate (%)'
    }

    # Rename Column names Using Mapping
    df.rename(columns=column_mapping, inplace=True)

    # Save Updated CSV
    df.to_csv(filename, index=False)

    print(f'Column names Successfully Converted for {filename}')

# ==================================================================================================================== # 

if __name__ == '__main__':
    fed_funds_rate()