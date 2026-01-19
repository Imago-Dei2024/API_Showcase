# ==================================================================================================================== # 
# Data Fetcher: Fetches fundamental data from Alpha Vantage API including company overview, 
# financial statements (income, balance sheet, cash flow), earnings history, and corporate actions (dividends, splits)
# ==================================================================================================================== # 

import os 
import json 
import requests 
from pathlib import Path 
from dotenv import load_dotenv
from urllib.parse import urlencode  
import csv 
from io import StringIO

# Load API 
load_dotenv() 

# API Modules - Python File #1. 
def fetch_company_overview(ticker, api_key): 
    base_url = 'https://www.alphavantage.co/query' 
    params = {'function': 'OVERVIEW', 'symbol': ticker, 'apikey': api_key} 
    response = requests.get(f'{base_url}?{urlencode(params)}') 
    return response.json() 

def fetch_income_statement(ticker, api_key): 
    base_url = 'https://www.alphavantage.co/query' 
    params = {'function': 'INCOME_STATEMENT', 'symbol': ticker, 'apikey': api_key} 
    response = requests.get(f'{base_url}?{urlencode(params)}') 
    return response.json()  

def fetch_balance_sheet(ticker, api_key): 
    base_url = "https://www.alphavantage.co/query" 
    params = {'function': 'BALANCE_SHEET', 'symbol': ticker, 'apikey': api_key} 
    response = requests.get(f'{base_url}?{urlencode(params)}') 
    return response.json() 

def fetch_cash_flow(ticker, api_key): 
    base_url = "https://www.alphavantage.co/query" 
    params = {'function': 'CASH_FLOW', 'symbol': ticker, 'apikey': api_key} 
    response = requests.get(f'{base_url}?{urlencode(params)}') 
    return response.json() 

def fetch_earnings_history(ticker, api_key): 
    base_url = "https://www.alphavantage.co/query" 
    params = {'function': 'EARNINGS', 'symbol': ticker, 'apikey': api_key} 
    response = requests.get(f'{base_url}?{urlencode(params)}') 
    return response.json() 

def fetch_earnings_estimates(ticker, api_key): 
    base_url = 'https://www.alphavantage.co/query'
    params = {'function': 'EARNINGS_ESTIMATES', 'symbol': ticker, 'apikey': api_key} 
    response = requests.get(f'{base_url}?{urlencode(params)}') 
    return response.json() 

def fetch_earnings_calendar(ticker, api_key): 
    base_url = 'https://www.alphavantage.co/query' 
    params = {'function': 'EARNINGS_CALENDAR', 'symbol': ticker, 'horizon': '12month', 'apikey': api_key} 
    response = requests.get(f'{base_url}?{urlencode(params)}') 

    # EARNINGS_CALENDAR returns CSV by default, not JSON
    # Parse CSV and convert to list of dictionaries 
    csv_data = StringIO(response.text) 
    reader = csv.DictReader(csv_data) 
    return list(reader) 

def fetch_dividends(ticker, api_key): 
    base_url = 'https://www.alphavantage.co/query' 
    params = {'function': 'DIVIDENDS', 'symbol': ticker, 'apikey': api_key} 
    response = requests.get(f'{base_url}?{urlencode(params)}') 
    return response.json() 

def fetch_all_data(ticker): 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        raise ValueError("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
    
    print(f"\n{'='*50}") 
    print(f'Fetching data for {ticker}...') 
    print(f"\n{'='*50}")  

    data_dir = Path('data') 
    data_dir.mkdir(exist_ok=True) 

    # Create empty dictionary (container that stores key-value pairs) 
    # NOTE: Main storage structure that collects all API responses before saving them to a single .JSON file 
    all_data = {} 

    print(f'[1/8] Fetching Company Overview...') 
    all_data['overview'] = fetch_company_overview(ticker, api_key) 

    print(f'[2/8] Fetching Income Statement...') 
    all_data['income_statement'] = fetch_income_statement(ticker, api_key) 

    print(f'[3/8] Fetching Balance Sheet...') 
    all_data['balance_sheet'] = fetch_balance_sheet(ticker, api_key) 

    print(f'[4/8] Fetching Statement of Cash Flows...') 
    all_data['cash_flows'] = fetch_cash_flow(ticker, api_key) 

    print(f'[5/8] Fetching Earnings History...') 
    all_data['earnings_history'] = fetch_earnings_history(ticker, api_key) 

    print(f'[6/8] Fetching Earnings Estimates...') 
    all_data['earnings_estimates'] = fetch_earnings_estimates(ticker, api_key) 

    print(f'[7/8] Fetching Earnings Calendar (Upcoming 12 Months)...') 
    all_data['earnings_calendar'] = fetch_earnings_calendar(ticker, api_key) 

    print(f'[8/8] Fetching Dividend Information (if applicable)...') 
    all_data['dividends'] = fetch_dividends(ticker, api_key) 

    # Save all_data as one JSON file 
    filename = data_dir / f'{ticker}_raw_data.json' 
    with open(filename, 'w') as f: 
        json.dump(all_data, f, indent=2) 

    print(f'\n√ All data saved to {filename}') 
    return all_data 


if __name__ == '__main__': 
    ticker = input(f'\nEnter Symbol: ').upper() 
    fetch_all_data(ticker)