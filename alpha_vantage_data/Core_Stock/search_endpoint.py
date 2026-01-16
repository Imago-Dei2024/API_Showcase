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
# ==================================================================================================================== # 
# ==================================================================================================================== # 
# Search Endpoint Utility # 
# Looking for some specific symbols or companies? Trying to build an auto-complete search box? We've got you covered! The Search Endpoint returns the best-matching symbols and market information based on keywords of your choice. The search results also contain match scores that provide you with the full flexibility to develop your own search and filtering logic.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The API function of your choice. In this case, function=SYMBOL_SEARCH

# 2. ❚ Required: keywords - A text string of your choice. For example: keywords=microsoft

# 3. ❚ Optional: datatype - By default, datatype=json. Strings json and csv are accepted with the following specifications: json returns the search results in JSON format; csv returns the search results as a CSV (comma separated value) file.

# 4. ❚ Required: apikey - Your API key

# ==================================================================================================================== #
def ticker_search_tool():
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit()

    # Get Keywords Input
    keywords = input("Enter search keywords (e.g., microsoft, apple, tesla): ")

    # API url Format with Parameters
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'SYMBOL_SEARCH',
        'keywords': keywords,
        'apikey': api_key,
        'datatype': 'csv',
        'entitlement': 'realtime'
    }

    # Build CSV URL with params
    CSV_URL = f"{base_url}?{urlencode(params)}"

    # Download and save the csv
    response = requests.get(CSV_URL)
    Path('Search_Results').mkdir(exist_ok=True)

    # Clean keywords for filename
    clean_keywords = re.sub(r'[^\w\s-]', '', keywords).strip().replace(' ', '_')
    filename = f"Search_Results/search_{clean_keywords}.csv"
    
    with open(filename, 'w') as file:
        file.write(response.text)

    print(f"Successfully Downloaded Search Results for '{keywords}' to {filename}")

    # Rename the Column names of the CSV
    print(f'Converting Column names for {filename}...')

    df = pd.read_csv(filename)

    # Define the Column Mapping
    column_mapping = {
        'symbol': 'Symbol',
        'name': 'Company Name',
        'type': 'Type',
        'region': 'Region',
        'marketOpen': 'Market Open',
        'marketClose': 'Market Close',
        'timezone': 'Timezone',
        'currency': 'Currency',
        'matchScore': 'Match Score'
    }

    # Rename Column names Using Mapping
    df.rename(columns=column_mapping, inplace=True)

    # Save Updated CSV
    df.to_csv(filename, index=False)

    print(f'Column names Successfully Converted for {filename}')

    # Display results using Rich
    if not df.empty:
        console.print(f"\n[bold green]Search Results for '{keywords}':[/bold green]")
        for index, row in df.head(10).iterrows():
            console.print(f"[cyan]{row.get('Symbol', 'N/A')}[/cyan] - {row.get('Company Name', 'N/A')} ({row.get('Type', 'N/A')}) - Match: {row.get('Match Score', 'N/A')}")


if __name__ == '__main__':
    ticker_search_tool()