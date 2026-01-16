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
# MACDEXT - Moving Average Convergence / Divergence Extended # 
# This API returns the moving average convergence / divergence values with controllable moving average type. See also: Investopedia article and mathematical reference.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The technical indicator of your choice. In this case, function=MACDEXT

# 2. ❚ Required: symbol - The name of the ticker of your choice. For example: symbol=IBM

# 3. ❚ Required: interval - Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly

# 4. ❚ Optional: month - Note: this parameter is ONLY applicable to intraday intervals for the equity markets

# 5. ❚ Required: series_type - The desired price type in the time series. Four types are supported: close, open, high, low

# 6. ❚ Optional: fastperiod - Positive integers are accepted. By default, fastperiod=12

# 7. ❚ Optional: slowperiod - Positive integers are accepted. By default, slowperiod=26

# 8. ❚ Optional: signalperiod - Positive integers are accepted. By default, signalperiod=9

# 9. ❚ Optional: fastmatype - Moving average type for the faster moving average. By default, fastmatype=0

# 10. ❚ Optional: slowmatype - Moving average type for the slower moving average. By default, slowmatype=0

# 11. ❚ Optional: signalmatype - Moving average type for the signal moving average. By default, signalmatype=0

# 12. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted

# 13. ❚ Required: apikey - Your API key

# ==================================================================================================================== #
def macdext_indicator():
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
    
    fastperiod_input = input("Fast period (default: 12): ")
    fastperiod = 12 if fastperiod_input == "" else int(fastperiod_input)
    
    slowperiod_input = input("Slow period (default: 26): ")
    slowperiod = 26 if slowperiod_input == "" else int(slowperiod_input)
    
    signalperiod_input = input("Signal period (default: 9): ")
    signalperiod = 9 if signalperiod_input == "" else int(signalperiod_input)

    # Moving Average Type Selection Helper
    def get_ma_type(ma_name):
        print(f"\n{ma_name} Moving Average Type:")
        print("0. SMA - Simple Moving Average")
        print("1. EMA - Exponential Moving Average") 
        print("2. WMA - Weighted Moving Average")
        print("3. DEMA - Double Exponential Moving Average")
        print("4. TEMA - Triple Exponential Moving Average")
        print("5. TRIMA - Triangular Moving Average")
        print("6. T3 - T3 Moving Average")
        print("7. KAMA - Kaufman Adaptive Moving Average")
        print("8. MAMA - MESA Adaptive Moving Average")
        
        matype_input = input(f"Enter {ma_name} MA Type (0-8, default: 0): ")
        return 0 if matype_input == "" else int(matype_input)

    fastmatype = get_ma_type("Fast")
    slowmatype = get_ma_type("Slow")
    signalmatype = get_ma_type("Signal")

    # API url Format with Parameters
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'MACDEXT',
        'symbol': symbol,
        'interval': interval,
        'series_type': series_type,
        'fastperiod': fastperiod,
        'slowperiod': slowperiod,
        'signalperiod': signalperiod,
        'fastmatype': fastmatype,
        'slowmatype': slowmatype,
        'signalmatype': signalmatype,
        'apikey': api_key,
        'datatype': 'csv',
        'entitlement': 'realtime'
    }

    # Build CSV URL with params
    CSV_URL = f"{base_url}?{urlencode(params)}"

    # Download and save the csv
    response = requests.get(CSV_URL)
    Path('Technical_Indicators').mkdir(exist_ok=True)

    filename = f"Technical_Indicators/{symbol}_MACDEXT_{fastperiod}_{slowperiod}_{signalperiod}_{interval}_{series_type}.csv"
    with open(filename, 'w') as file:
        file.write(response.text)

    print(f"Successfully Downloaded MACDEXT Indicator for {symbol} to {filename}")

    # Rename the Column names of the CSV
    print(f'Converting Column names for {filename}...')

    df = pd.read_csv(filename)

    # Define the Column Mapping
    column_mapping = {
        'time': 'Date',
        'MACD': f'MACD_{fastperiod}_{slowperiod}',
        'MACD_Hist': f'MACD_Hist_{signalperiod}',
        'MACD_Signal': f'MACD_Signal_{signalperiod}'
    }

    # Rename Column names Using Mapping
    df.rename(columns=column_mapping, inplace=True)

    # Save Updated CSV
    df.to_csv(filename, index=False)

    print(f'Column names Successfully Converted for {filename}')



if __name__ == '__main__':
    macdext_indicator()