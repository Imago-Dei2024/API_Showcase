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
# ==================================================================================================================== # 
# Realtime Bulk Quotes # 
# This API returns realtime quotes for US-traded symbols in bulk, accepting up to 100 symbols per API request and covering both regular and extended (pre-market and post-market) trading hours. You can use this endpoint as a high-throughput alternative to the Global Quote API, which accepts one symbol per API request.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The time series of your choice. In this case, function=REALTIME_BULK_QUOTES

# 2. ❚ Required: symbol - Up to 100 symbols separated by comma. For example: symbol=MSFT,AAPL,IBM. If more than 100 symbols are provided, only the first 100 symbols will be honored as part of the API input.

# 3. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the search results in JSON format; csv returns the search results as a CSV (comma separated value) file.

# 4. ❚ Required: apikey - Your API key

# ==================================================================================================================== #


# ==================================================================================================================== # 
# ==================================================================================================================== # 
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
# ==================================================================================================================== # 
# Realtime Bulk Quotes # 
# This API returns realtime quotes for US-traded symbols in bulk, accepting up to 100 symbols per API request and covering both regular and extended (pre-market and post-market) trading hours. You can use this endpoint as a high-throughput alternative to the Global Quote API, which accepts one symbol per API request.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The time series of your choice. In this case, function=REALTIME_BULK_QUOTES

# 2. ❚ Required: symbol - Up to 100 symbols separated by comma. For example: symbol=MSFT,AAPL,IBM. If more than 100 symbols are provided, only the first 100 symbols will be honored as part of the API input.

# 3. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the search results in JSON format; csv returns the search results as a CSV (comma separated value) file.

# 4. ❚ Required: apikey - Your API key

# ==================================================================================================================== #


# ==================================================================================================================== # 
# ==================================================================================================================== # 
def realtime_bulk_quotes():
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()

    # Get Symbols Input
    print("Enter up to 100 stock symbols separated by commas (e.g., AAPL,MSFT,GOOGL):")
    symbols_input = input("Symbols: ")
    
    # Clean up the input and validate
    symbols = [symbol.strip().upper() for symbol in symbols_input.split(',')]
    
    if len(symbols) > 100:
        print(f"Warning: You entered {len(symbols)} symbols. Only the first 100 will be processed.")
        symbols = symbols[:100]
    
    symbols_string = ','.join(symbols)

    # API url Format with Parameters
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'REALTIME_BULK_QUOTES',
        'symbol': symbols_string,
        'apikey': api_key,
        'datatype': 'csv',
        'entitlement': 'realtime'
    }

    # Build CSV URL with params
    CSV_URL = f"{base_url}?{urlencode(params)}"

    # Download and save the csv
    response = requests.get(CSV_URL)
    Path('Bulk_Quotes_Data').mkdir(exist_ok=True)

    filename = f"Bulk_Quotes_Data/bulk_quotes_{len(symbols)}_symbols.csv"
    with open(filename, 'w') as file:
        file.write(response.text)

    print(f"Successfully Downloaded Bulk Quotes for {len(symbols)} symbols to {filename}")

    # Rename the Column names of the CSV
    print(f'Converting Column names for {filename}...')

    df = pd.read_csv(filename)

    # Define the Column Mapping (adjust based on actual API response columns)
    column_mapping = {
        'symbol': 'Symbol',
        'open': 'Open',
        'high': 'High',
        'low': 'Low',
        'price': 'Price',
        'volume': 'Volume',
        'latest_trading_day': 'Latest Trading Day',
        'previous_close': 'Previous Close',
        'change': 'Change',
        'change_percent': 'Change Percent'
    }

    # Rename Column names Using Mapping
    df.rename(columns=column_mapping, inplace=True)

    # Save Updated CSV
    df.to_csv(filename, index=False)

    print(f'Column names Successfully Converted for {filename}')


if __name__ == '__main__':
    realtime_bulk_quotes()