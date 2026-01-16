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
# Real GDP Per Capita Economic Data # 
# This API returns the quarterly Real GDP per Capita data of the United States.
# Source: U.S. Bureau of Economic Analysis, Real gross domestic product per capita, retrieved from FRED, Federal Reserve Bank of St. Louis. This data feed uses the FRED® API but is not endorsed or certified by the Federal Reserve Bank of St. Louis. By using this data feed, you agree to be bound by the FRED® API Terms of Use.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The function of your choice. In this case, function=REAL_GDP_PER_CAPITA

# 2. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the time series in JSON format; csv returns the time series as a CSV (comma separated value) file.

# 3. ❚ Required: apikey - Your API key

# ==================================================================================================================== #
def gdp_per_capita():
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()

    # API url Format with Parameters
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'REAL_GDP_PER_CAPITA',
        'apikey': api_key,
        'datatype': 'csv'
    }

    # Build CSV URL with params
    CSV_URL = f"{base_url}?{urlencode(params)}"

    # Download and save the csv
    response = requests.get(CSV_URL)
    Path('Economic_Data').mkdir(exist_ok=True)

    filename = f"Economic_Data/real_gdp_per_capita.csv"
    with open(filename, 'w') as file:
        file.write(response.text)

    print(f"Successfully Downloaded Real GDP Per Capita Data to {filename}")

    # Rename the Column names of the CSV
    print(f'Converting Column names for {filename}...')

    df = pd.read_csv(filename)

    # Define the Column Mapping
    column_mapping = {
        'date': 'Date',
        'value': 'Real GDP Per Capita (Chained 2012 Dollars)'
    }

    # Rename Column names Using Mapping
    df.rename(columns=column_mapping, inplace=True)

    # Save Updated CSV
    df.to_csv(filename, index=False)

    print(f'Column names Successfully Converted for {filename}')
# ==================================================================================================================== # 

if __name__ == '__main__':
    gdp_per_capita()