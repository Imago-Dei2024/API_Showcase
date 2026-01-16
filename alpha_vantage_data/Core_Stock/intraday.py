from email.mime import base 
import os 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 

import requests 
import pandas as pd 


# ==================================================================================================================== # 
# ==================================================================================================================== # 
# Time Series Intraday Stock Data # 
# This API returns current and 20+ years of historical intraday OHLCV time series of the equity specified, covering pre-market and post-market hours where applicable (e.g., 4:00am to 8:00pm Eastern Time for the US market). You can query both raw (as-traded) and split/dividend-adjusted intraday data from this endpoint. The OHLCV data is sometimes called "candles" in finance literature.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The time series of your choice. In this case, function=TIME_SERIES_INTRADAY

# 2. ❚ Required: symbol - The name of the equity of your choice. For example: symbol=IBM

# 3. ❚ Required: interval - Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min

# 4. ❚ Optional: adjusted - By default, adjusted=true and the output time series is adjusted by historical split and dividend events. Set adjusted=false to query raw (as-traded) intraday values.

# 5. ❚ Optional: extended_hours - By default, extended_hours=true and the output time series will include both the regular trading hours and the extended (pre-market and post-market) trading hours (4:00am to 8:00pm Eastern Time for the US market). Set extended_hours=false to query regular trading hours (9:30am to 4:00pm US Eastern Time) only.

# 6. ❚ Optional: month - By default, this parameter is not set and the API will return intraday data for the most recent days of trading. You can use the month parameter (in YYYY-MM format) to query a specific month in history. For example, month=2009-01. Any month in the last 20+ years since 2000-01 (January 2000) is supported.

# 7. ❚ Optional: outputsize - By default, outputsize=compact. Strings compact and full are accepted with the following specifications: compact returns only the latest 100 data points in the intraday time series; full returns trailing 30 days of the most recent intraday data if the month parameter is not specified, or the full intraday data for a specific month in history if the month parameter is specified.

# 8. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the intraday time series in JSON format; csv returns the time series as a CSV (comma separated value) file.

# 9. ❚ Required: apikey - Your API key

# ==================================================================================================================== #
# ==================================================================================================================== # 
def fetch_intraday_stocks(): 
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")  
    if not api_key: 
        print("ERROR: Unable to Locate Alpha Vantage API Key") 
        exit()

    # Get Ticker Input 
    ticker = input("Enter Ticker: ")

    # Select Interval
    while True:
        print(f"Please Select an Interval for {ticker}:")
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
        print(f"Please Select an Output Size for {ticker}:")
        print("1. Compact - Latest 100 data points")
        print("2. Full - Trailing 30 days")
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
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': ticker,
        'interval': interval,
        'apikey': api_key,
        'datatype': 'csv',
        'outputsize': output_size,
        'adjusted': 'true',
        'extended_hours': 'true',
        'entitlement': 'realtime'
    }

    # Build CSV URL with params
    CSV_URL = f"{base_url}?{urlencode(params)}"

    # Download and save the csv
    response = requests.get(CSV_URL)
    Path('p_sql_two/Intraday_Data').mkdir(exist_ok=True)

    filename = f"p_sql_two/Intraday_Data/{ticker}_{interval}.csv"
    with open(filename, 'w') as file:
        file.write(response.text)

    print(f"Successfully Downloaded Intraday Data for {ticker} ({interval}) to {filename}")

    # Rename the Column names of the CSV
    print(f'Converting Column names for {filename}...')

    df = pd.read_csv(filename)

    # Define the Column Mapping
    column_mapping = {
        'timestamp': 'Timestamp',
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


if __name__ == '__main__':
    fetch_intraday_stocks()