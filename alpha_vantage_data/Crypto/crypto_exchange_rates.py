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
import json 
import requests 
import pandas as pd 

# ==================================================================================================================== # 
# ==================================================================================================================== # 
# ==================================================================================================================== # 
# Currency Exchange Rate # 
# This API returns the realtime exchange rate for any pair of cryptocurrency (e.g., Bitcoin) or physical currency (e.g., USD).

# ==== API Parameters ==== #
# 1. ❚ Required: function - The function of your choice. In this case, function=CURRENCY_EXCHANGE_RATE

# 2. ❚ Required: from_currency - The currency you would like to get the exchange rate for. It can either be a physical currency or cryptocurrency. For example: from_currency=USD or from_currency=BTC

# 3. ❚ Required: to_currency - The destination currency for the exchange rate. It can either be a physical currency or cryptocurrency. For example: to_currency=USD or to_currency=BTC

# 4. ❚ Required: apikey - Your API key

# ==================================================================================================================== #
def crypto_exchange_rates():
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()

    fn = 'CURRENCY_EXCHANGE_RATE'
    # Get Currency Input
    f_currency = input("Enter FROM currency (e.g., BTC, USD, EUR): ").upper()
    t_currency = input("Enter TO currency (e.g., USD, BTC, EUR): ").upper()

    # API url Format with Parameters
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': fn,
        'from_currency': f_currency,
        'to_currency': t_currency,
        'apikey': api_key
    }

    # Build URL with params
    API_URL = f"{base_url}?{urlencode(params)}"

    # Make API request
    response = requests.get(API_URL)
    data = response.json()

    # Create directories
    Path('Crypto_Exchange_Rates').mkdir(exist_ok=True)

    # Save raw JSON response
    filename_json = f"Crypto_Exchange_Rates/{f_currency}_to_{t_currency}.json"
    with open(filename_json, 'w') as file:
        json.dump(data, file, indent=2)

    print(f"Successfully Downloaded Exchange Rate for {f_currency} to {t_currency}")

    # Extract exchange rate data
    if "Realtime Currency Exchange Rate" in data:
        exchange_data = data["Realtime Currency Exchange Rate"]
        
        # Create DataFrame for CSV export
        df_data = {
            'From Currency Code': [exchange_data.get('1. From_Currency Code', '')],
            'From Currency Name': [exchange_data.get('2. From_Currency Name', '')],
            'To Currency Code': [exchange_data.get('3. To_Currency Code', '')], 
            'To Currency Name': [exchange_data.get('4. To_Currency Name', '')],
            'Exchange Rate': [exchange_data.get('5. Exchange Rate', '')],
            'Last Refreshed': [exchange_data.get('6. Last Refreshed', '')],
            'Time Zone': [exchange_data.get('7. Time Zone', '')],
            'Bid Price': [exchange_data.get('8. Bid Price', '')],
            'Ask Price': [exchange_data.get('9. Ask Price', '')]
        }
        
        df = pd.DataFrame(df_data)
        
        # Save as CSV
        filename_csv = f"Crypto_Exchange_Rates/{f_currency}_to_{t_currency}.csv"
        df.to_csv(filename_csv, index=False)
        exchange_data.get('9. Ask Price', 'N/A') 
        
        print(f"Data saved to {filename_csv}")
        
    else:
        print("Error: Unable to retrieve exchange rate data")
        print("API Response:", data)


if __name__ == '__main__':
    crypto_exchange_rates()