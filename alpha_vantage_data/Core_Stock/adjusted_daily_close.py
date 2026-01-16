from email.mime import base
import os
import re 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 

import csv 
import requests 
import pandas as pd 

def fetch_adjusted_daily_closing(): 
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")  
    if not api_key: 
        print("ERROR: Unable to Locate Alpha Vantage API Key") 
        return False

    # Get Ticker Input 
    ticker = input("Enter Ticker: ")  

    # Select Time Range for Data (Loop Until Valid Selection) 
    while True: 
        print(f"Please Select an Output Size for {ticker}: ") 
        print("1. Compact - 100 Trading Days") 
        print("2. Full - All Historical Data (max 20 years)") 
        choice = input("Enter Choice (1 or 2): ") 

        if choice == '1': 
            output_size='compact' 
            break 

        elif choice == '2': 
            output_size='full' 
            break 

        else: 
            print('Invalid Choice. Please Select 1 or 2.\n')

    # API url Format with Parameters 
    base_url = 'https://www.alphavantage.co/query' 
    params = { 
        'function': 'TIME_SERIES_DAILY_ADJUSTED', 
        'symbol': ticker, 
        'interval': '1min', 
        'apikey': api_key, 
        'datatype': 'csv', 
        'outputsize': 'full',  # All historical Data 
        'entitlement': 'realtime',
    } 

    # Build original csv url with adjusted params 
    CSV_URL = f"{base_url}?{urlencode(params)}" 

    # Download and save the csv 
    response = requests.get(CSV_URL) 
    Path('Daily_Historical_Data').mkdir(exist_ok=True) 

    filename = f"Daily_Historical_Data/{ticker}.csv" 
    with open(filename, 'w') as file: 
        file.write(response.text) 

    print(f"Successfully Downloaded Historical ADC for {ticker} to {filename}")  

    # Rename the Column names of the Csv for compatibility with QsTrader Backtesting 
    print(f'Converting Column names for {filename}...') 

    df = pd.read_csv(filename) 

    # Define the Column Mapping 
    column_mapping = { 
        'timestamp': 'Date', 
        'open': 'Open', 
        'high': 'High', 
        'low': 'Low', 
        'close': 'Close',   
        'adjusted_close': 'Adj Close', 
        'volume': 'Volume', 
        'dividend_amount': 'Dividend Amount', 
        'split_coefficient': 'Split Coefficient'
    } 

    # Rename Column names Using Mapping 
    df.rename(columns=column_mapping, inplace=True) 

    # Save Update CSV 
    df.to_csv(filename, index = False) 

    print(f'Column names Sucessfully Converted for {filename}') 
    print('')
    print('')
    return True

def main():
    while True:
        success = fetch_adjusted_daily_closing()
        
        if not success:
            break
            
        while True:
            continue_choice = input("Do you want to fetch another ticker? (y/n): ").lower()
            if continue_choice in ['y', 'yes']:
                break
            elif continue_choice in ['n', 'no']:
                print("Exiting...")
                return
            else:
                print("Please enter 'y' for yes or 'n' for no.")

if __name__ == '__main__': 
    main()