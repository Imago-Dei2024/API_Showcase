from email.mime import base 
import os 
import re 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import csv 
import requests 
import pandas as pd  
import json 

# Alpha Limit = 150 requests per minute (no daily max), real time market data. #  
# UNFORMATTED URL for fetching treasury yield data: 
# https://www.alphavantage.co/query?function=TREASURY_YIELD&interval=monthly&maturity=10year&apikey=demo 

# Break URL into Params 
def fetch_risk_free_rate(): 
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 

    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 

    # Select Time Interval 
    while True: 
        print("Select Time Interval For Treasury Yield Data: ")  
        print("1. Daily") 
        print("2. Weekly") 
        print('3. Monthly') 
        choice = input("Select 1 - 3: ") 

        if choice == '1': 
            interval_choice = 'daily' 
            break 

        elif choice == '2': 
            interval_choice = 'weekly' 
            break 

        elif choice == '3': 
            interval_choice = 'monthly' 
            break 

        else: 
            print("Invalid Selection, Please Try Again...\n")  

    # Select the desired file for data results 
    while True: 
        print("Please Select How You Want The Data Stored: ") 
        print('1. JSON file')  
        print('2. CSV file') 
        choice = input('Select File Type (1 or 2)') 

        if choice == '1': 
            file_type = 'json' 
            break 

        elif choice == '2': 
            file_type = 'csv' 
            break 

        else: 
            print("Invalid Selection, Please Try Again...") 

        
    # Format API URL 
    base_url = 'https://www.alphavantage.co/query' 
    params = { 
        'function': 'TREASURY_YIELD', 
        'interval': interval_choice,
        'datatype': file_type, 
        'apikey': api_key 
    } 

    # Build Original URL with params 
    TR_URL = f"{base_url}?{urlencode(params)}" 

    # Download and Save the json file 
    response = requests.get(TR_URL)
    data = response.json() 

    Path("Treasury_Yield_Data").mkdir(exist_ok=True) 

    filename = f"{interval_choice}_treasury_rate_data.json" 
    with open (filename, 'w') as json_file: 
        json.dump(data, json_file, indent=2)  

    print(f'Successfully Saved the {interval_choice} Treasury Yield Rates Historical Data to {filename}') 

if __name__ == '__main__': 
    fetch_risk_free_rate()

