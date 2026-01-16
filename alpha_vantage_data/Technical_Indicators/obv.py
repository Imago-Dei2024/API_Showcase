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
# OBV - On Balance Volume # 
# This API returns the on balance volume (OBV) values. See also: Investopedia article and mathematical reference.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The technical indicator of your choice. In this case, function=OBV

# 2. ❚ Required: symbol - The name of the ticker of your choice. For example: symbol=IBM

# 3. ❚ Required: interval - Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, daily, weekly, monthly

# 4. ❚ Optional: month - Note: this parameter is ONLY applicable to intraday intervals (1min, 5min, 15min, 30min, and 60min) for the equity markets. By default, this parameter is not set and the technical indicator values will be calculated based on the most recent 30 days of intraday data.

# 5. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted

# 6. ❚ Required: apikey - Your API key

# ==================================================================================================================== #
def obv_indicator():
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

    # API url Format with Parameters
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'OBV',
        'symbol': symbol,
        'interval': interval,
        'apikey': api_key,
        'datatype': 'csv',
        'entitlement': 'realtime'
    }

    # Build CSV URL with params
    CSV_URL = f"{base_url}?{urlencode(params)}"

    # Download and save the csv
    response = requests.get(CSV_URL)
    Path('Technical_Indicators').mkdir(exist_ok=True)

    filename = f"Technical_Indicators/{symbol}_OBV_{interval}.csv"
    with open(filename, 'w') as file:
        file.write(response.text)

    print(f"Successfully Downloaded OBV (On Balance Volume) Indicator for {symbol} to {filename}")

    # Rename the Column names of the CSV
    print(f'Converting Column names for {filename}...')

    df = pd.read_csv(filename)

    # Define the Column Mapping
    column_mapping = {
        'time': 'Date',
        'OBV': 'On_Balance_Volume'
    }

    # Rename Column names Using Mapping
    df.rename(columns=column_mapping, inplace=True)

    # Save Updated CSV
    df.to_csv(filename, index=False)

    print(f'Column names Successfully Converted for {filename}')

    # Display recent data using Rich with OBV interpretation
    if not df.empty:
        console.print(f"\n[bold green]Recent OBV (On Balance Volume) Data for {symbol} ({interval}):[/bold green]")
        
        # Calculate trend from recent values for interpretation
        recent_data = df.tail(5)
        
        for index, row in recent_data.iterrows():
            date = row.get('Date', 'N/A')
            obv_value = row.get('On_Balance_Volume', 'N/A')
            
            # Simple trend analysis (compare with previous value if available)
            trend_indicator = ""
            if index > 0:
                prev_value = df.iloc[index-1].get('On_Balance_Volume', None)
                if prev_value is not None and obv_value != 'N/A':
                    try:
                        current_val = float(obv_value)
                        prev_val = float(prev_value)
                        if current_val > prev_val:
                            trend_indicator = "[green]↗ (Accumulation)[/green]"
                        elif current_val < prev_val:
                            trend_indicator = "[red]↘ (Distribution)[/red]"
                        else:
                            trend_indicator = "[yellow]→ (Neutral)[/yellow]"
                    except ValueError:
                        pass
            
            # Format large numbers for readability
            if obv_value != 'N/A':
                try:
                    obv_float = float(obv_value)
                    obv_formatted = f"{obv_float:,.0f}"
                    console.print(f"[cyan]{date}:[/cyan] {obv_formatted} {trend_indicator}")
                except ValueError:
                    console.print(f"[cyan]{date}:[/cyan] {obv_value} {trend_indicator}")
            else:
                console.print(f"[cyan]{date}:[/cyan] {obv_value}")
        
        # Add interpretation note
        console.print(f"\n[bold yellow]Note:[/bold yellow] Rising OBV confirms uptrend (buying pressure), falling OBV confirms downtrend (selling pressure)")


if __name__ == '__main__':
    obv_indicator()