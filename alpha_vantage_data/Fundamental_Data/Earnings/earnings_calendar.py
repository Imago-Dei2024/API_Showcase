import os 
import email.mime 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import requests 
import pandas as pd 
import csv 

# ==================================================================================================================== # 
# Earnings Estimates Trending # 
# This API returns the annual and quarterly EPS and revenue estimates for the company of interest, along with analyst count and revision history.
# To ensure optimal API response time, this endpoint uses the CSV format which is more memory-efficient than JSON

# API Parameters #
# 1. ❚ Required: function = EARNINGS_CALENDAR

# 2. ❚ optional: symbol - When no symbol is set, earnings for all companies is returned (default).  

# 3. ❚ optional: horizon
#      a. horizon = 3month (Expected Company Earnings for Next 3 months) 
#      b. horizon = 6month (Expected Company Earnings for Next 6 months) 
#      c. horizon = 12month (Expected Company Earnings for Next 12 months) 

# 3. ❚ Required: apikey 
# ==================================================================================================================== #  
def fetch_earnings_calendar(): 
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'EARNINGS_CALENDAR' 
    print('Valid Time Horizons: 3month, 6month, 12month') 
    time_horizon = input("Select a Valid Time Horizon: ") 

    # Build API Params 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn,  
        'horizon': time_horizon, 
        'apikey': api_key
    } 

    # Build Request URL 
    earnings_calendar_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(earnings_calendar_url)  

    Path('p_sql_two/Earnings_Calendar_CSV').mkdir(exist_ok=True) 

    filename = f'p_sql_two/Earnings_Calendar_CSV/{time_horizon}_{fn}.csv' 
    with open (filename, 'w') as earnings_calendar: 
        earnings_calendar.write(response.text)


    print(f'Successfully Saved {filename}')  

if __name__ == '__main__': 
    fetch_earnings_calendar()