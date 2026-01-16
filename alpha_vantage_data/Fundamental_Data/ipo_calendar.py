import os 
import email.mime 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import requests 
import pandas as pd 
import json 

# ==================================================================================================================== # 
# ==== IPO Calendar ==== #
# This API returns a list of IPOs expected in the next 3 months.

# API Parameters #
# 1. ❚ Required: function = IPO_CALENDAR

# 2. ❚ Required: apikey 
# ==================================================================================================================== #  
def upcoming_ipos(): 
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'IPO_CALENDAR'  

    # Build API Params 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn,   
        'apikey': api_key
    } 

    # Build Request URL 
    ipo_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(ipo_url)   
    Path('IPO_Calendar_CSV').mkdir(exist_ok=True) 

    filename = f'IPO_Calendar_CSV/{fn}.csv' 
    with open (filename, 'w') as ipo_csv: 
        ipo_csv.write(response.text)   


    print(f'Successfully Saved IPO Calendar to {filename}')  

if __name__ == '__main__': 
    upcoming_ipos() 