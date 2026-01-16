import os
import json
import requests
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

def fetch_company_overview(ticker, api_key):
    base_url = 'https://www.alphavantage.co/query'
    params = {'function': 'OVERVIEW', 'symbol': ticker, 'apikey': api_key}
    response = requests.get(f'{base_url}?{urlencode(params)}')
    return response.json()

def fetch_income_statement(ticker, api_key):
    base_url = 'https://alphavantage.co/query'
    params = {'function': 'INCOME_STATEMENT', 'symbol': ticker, 'apikey': api_key}
    response = requests.get(f'{base_url}?{urlencode(params)}')
    return response.json()

def fetch_balance_sheet(ticker, api_key):
    base_url = 'https://alphavantage.co/query'
    params = {'function': 'BALANCE_SHEET', 'symbol': ticker, 'apikey': api_key}
    response = requests.get(f'{base_url}?{urlencode(params)}')
    return response.json()

def fetch_cash_flow(ticker, api_key):
    base_url = 'https://www.alphavantage.co/query'
    params = {'function': 'CASH_FLOW', 'symbol': ticker, 'apikey': api_key}
    response = requests.get(f'{base_url}?{urlencode(params)}')
    return response.json()

def fetch_earnings(ticker, api_key):
    base_url = 'https://www.alphavantage.co/query'
    params = {'function': 'EARNINGS', 'symbol': ticker, 'apikey': api_key}
    response = requests.get(f'{base_url}?{urlencode(params)}')
    return response.json()

def fetch_dividends(ticker, api_key):
    base_url = 'https://www.alphavantage.co/query'
    params = {'function': 'DIVIDENDS', 'symbol': ticker, 'apikey': api_key}
    response = requests.get(f'{base_url}?{urlencode(params)}')
    return response.json()

def fetch_splits(ticker, api_key):
    base_url = 'https://www.alphavantage.co/query'
    params = {'function': 'SPLITS', 'symbol': ticker, 'apikey': api_key}
    response = requests.get(f'{base_url}?{urlencode(params)}')
    return response.json()

def fetch_all_data(ticker):
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Add ALPHA_VANTAGE_API_KEY to .env file")
    
    print(f"\n{'='*60}")
    print(f"Fetching data for {ticker}...")
    print(f"{'='*60}\n")
    
    data_dir = Path('data')
    data_dir.mkdir(exist_ok=True)
    
    all_data = {}
    
    print(f"[1/7] Fetching company overview...")
    all_data['overview'] = fetch_company_overview(ticker, api_key)
    
    print(f"[2/7] Fetching income statement...")
    all_data['income_statement'] = fetch_income_statement(ticker, api_key)
    
    print(f"[3/7] Fetching balance sheet...")
    all_data['balance_sheet'] = fetch_balance_sheet(ticker, api_key)
    
    print(f"[4/7] Fetching cash flow statement...")
    all_data['cash_flow'] = fetch_cash_flow(ticker, api_key)
    
    print(f"[5/7] Fetching earnings data...")
    all_data['earnings'] = fetch_earnings(ticker, api_key)
    
    print(f"[6/7] Fetching dividends...")
    all_data['dividends'] = fetch_dividends(ticker, api_key)
    
    print(f"[7/7] Fetching stock splits...")
    all_data['splits'] = fetch_splits(ticker, api_key)
    
    filename = data_dir / f'{ticker}_raw_data.json'
    with open(filename, 'w') as f:
        json.dump(all_data, f, indent=2)
    
    print(f"\n✓ All data saved to {filename}")
    return all_data

if __name__ == '__main__':
    ticker = input("Enter ticker symbol: ").upper()
    fetch_all_data(ticker)