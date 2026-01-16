import email.mime 
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
import json  


# API PARAMETERS # 
# 1. function (required) = 'NEWS_SENTIMENT' 

# 2. tickers (optional)

# 4. topics (optional), Supported Topics: 
#    a. blockchain 
#    b. earnings 
#    c. ipo 
#    d. mergers_and_acquisitions  # Fixed spelling
#    e. financial_markets 
#    f. economy_fiscal (tax reform, government spending) 
#    g. economy_monetary (interest rates, inflation) 
#    h. economy_macro (macro/overal) 
#    i. energy_transportation 
#    j. finance 
#    k. life_sciences 
#    l. manufacturing 
#    m. real_estate 
#    n. retail_wholesale 
#    o. technology 

# 5. time_from AND time_to (optional) (time range of news articles I would like) (YYYYMMDDTHHMM format) 
#    a. if time_from is specified, but time_to is missing, it returns articles published between time_from and current time 

# 6. sort (optional) 
#    a. sort = LATEST (returns latest articles first) 
#    b. sort = EARLIEST (oldest first) 
#    c. sort = RELEVANCE (based on use case) 

# 7. limit (optional) 
#    a. default = 50 --> max = 1000 

# # 3. apikey (required)  


# Create a function for external use 
def market_news_intro(): 
    console = Console()

    print('')
    print('')
    
    # Create the main title
    title = Text("Market News & Sentiment Analysis Module", style="bold bright_blue")
    
    # Create the description content
    description = Text()
    description.append("📰 WHAT THIS MODULE DOES:\n", style="bold bright_blue")
    description.append("This module fetches live and historical market news & sentiment data from ")
    description.append("premier news outlets worldwide. It provides comprehensive coverage with ")
    description.append("advanced sentiment analysis for informed investment decisions.\n\n")
    
    description.append("📊 COVERAGE:\n", style="bold bright_blue")
    description.append("• Stocks, Cryptocurrencies, Forex markets\n", style="bright_green")
    description.append("• 15+ topic categories (Technology, Finance, IPOs, M&A, etc.)\n", style="bright_green")
    description.append("• Sentiment analysis for each article\n", style="bright_green")
    description.append("• Customizable date ranges and result limits\n\n", style="bright_green")
    
    description.append("🔍 FILTERING OPTIONS:\n", style="bold bright_blue")
    description.append("• Specific tickers/symbols\n", style="bright_green")
    description.append("• News topics and sectors\n", style="bright_green")
    description.append("• Date ranges (last 7 days to custom ranges)\n", style="bright_green")
    description.append("• Sort by latest, earliest, or relevance\n", style="bright_green")
    description.append("• Result limits (1-1000 articles)\n\n", style="bright_green")
    
    description.append("📋 OUTPUT:\n", style="bold bright_blue")
    description.append("• JSON format with article titles, summaries, URLs\n", style="bright_green")
    description.append("• Sentiment scores and classifications\n", style="bright_green")
    description.append("• Publication timestamps and source information\n", style="bright_green")
    description.append("• Ticker relevance scores\n\n", style="bright_green")
    
    description.append("Ready to analyze market sentiment and news trends!", style="bold white")
    
    # Create and display the panel
    panel = Panel(
        description,
        title=title,
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()  # Add some spacing


def fetch_market_news_and_sentiments(): 
    
    print('')
    print('')
    
    # ==================================================================================================================== # 
    # Print Intro Panel
    market_news_intro()
    # ==================================================================================================================== # 

    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 

    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    ticker_list = input("Input Ticker(s) (comma-separated, or press Enter to skip): ").strip()
    if not ticker_list:
        ticker_list = None
    
    fn = 'NEWS_SENTIMENT'  

# ==================================================================================================================== # 
# Make Logic that Displays Available Topics, and Let's them Choose which one to search. 

    search_topic = input("Would You Like to Search a Specific Topic? (Yes/No): ") 

    if search_topic.lower() == 'yes':
        while True: 
            console.print("Please See List of Available Search Topics:", style="bold bright_blue") 
            console.print('1. Blockchain', style="bright_green") 
            console.print('2. Earnings', style="bright_green") 
            console.print('3. IPO', style="bright_green") 
            console.print('4. Mergers & Acquisitions', style="bright_green") 
            console.print('5. Financial Markets', style="bright_green") 
            console.print('6. Economy - Fiscal Policy (e.g, tax reform, government spending)', style="bright_green") 
            console.print('7. Economy - Monetary Policy (e.g, interest rates, inflation)', style="bright_green") 
            console.print('8. Economy - Macro/Overall', style="bright_green") 
            console.print('9. Energy & Transportation', style="bright_green")
            console.print('10. Finance', style="bright_green") 
            console.print('11. Life Sciences', style="bright_green") 
            console.print('12. Manufacturing', style="bright_green") 
            console.print('13. Real Estate & Construction', style="bright_green") 
            console.print('14. Retail & Wholesale', style="bright_green") 
            console.print('15. Technology', style="bright_green") 
            choice = input('Select an Option (1 - 15): ')   

            if choice == '1': 
                topic = 'blockchain' 
                break 

            elif choice == '2': 
                topic = 'earnings' 
                break 

            elif choice == '3': 
                topic = 'ipo' 
                break 

            elif choice == '4': 
                topic = 'mergers_and_acquisitions'  # Fixed underscore
                break 

            elif choice == '5': 
                topic = 'financial_markets' 
                break 

            elif choice == '6': 
                topic = 'economy_fiscal' 
                break 

            elif choice == '7': 
                topic = 'economy_monetary' 
                break 

            elif choice == '8': 
                topic = 'economy_macro' 
                break 

            elif choice == '9': 
                topic ='energy_transportation' 
                break 

            elif choice == '10': 
                topic = 'finance' 
                break 

            elif choice == '11': 
                topic = 'life_sciences' 
                break 

            elif choice == '12': 
                topic = 'manufacturing' 
                break 

            elif choice == '13': 
                topic = 'real_estate' 
                break 

            elif choice == '14':  
                topic = 'retail_wholesale' 
                break 

            elif choice == '15': 
                topic = 'technology' 
                break 

            else: 
                print("Invalid Selection, Please Select from '1 - 15' ")

    else: 
        topic = None 
        print("No Specific Topic Selected, Moving on to Next Step...")  

# ==================================================================================================================== #  

# ==================================================================================================================== #  
# Would You Like Specific Date Ranges Section 

    date_ranges = input("Would You Like Specific Date Ranges? (Yes / No): ") 

    if date_ranges.lower() == 'yes': 
        while True: 
            console.print("Please Select Start Date (required) & End Date (optional, if left blank returns results between start date and present):", style="bold bright_blue")  
            console.print("")
            console.print("1. Last 7 Days", style="bright_green")
            console.print("2. Last 30 Days", style="bright_green") 
            console.print("3. Last 90 Days", style="bright_green")
            console.print("4. Last 6 Months", style="bright_green")
            console.print("5. Last Year", style="bright_green")
            console.print("6. Custom Date Range", style="bright_green")
            choice = input(' === Select an Option (1 - 6) ===: ')

            if choice == '1':
                # Last 7 days
                from datetime import datetime, timedelta
                time_to = datetime.now().strftime('%Y%m%dT%H%M')
                time_from = (datetime.now() - timedelta(days=7)).strftime('%Y%m%dT%H%M')
                break

            elif choice == '2':
                # Last 30 days  
                time_to = datetime.now().strftime('%Y%m%dT%H%M')
                time_from = (datetime.now() - timedelta(days=30)).strftime('%Y%m%dT%H%M')
                break

            elif choice == '3':
                # Last 90 days
                time_to = datetime.now().strftime('%Y%m%dT%H%M')
                time_from = (datetime.now() - timedelta(days=90)).strftime('%Y%m%dT%H%M')
                break

            elif choice == '4':
                # Last 6 months
                time_to = datetime.now().strftime('%Y%m%dT%H%M')
                time_from = (datetime.now() - timedelta(days=180)).strftime('%Y%m%dT%H%M')
                break

            elif choice == '5':
                # Last year
                time_to = datetime.now().strftime('%Y%m%dT%H%M')
                time_from = (datetime.now() - timedelta(days=365)).strftime('%Y%m%dT%H%M')
                break

            elif choice == '6':
                # Custom date range
                time_from = input("Enter start date (YYYYMMDDTHHMM format): ")
                time_to_input = input("Enter end date (YYYYMMDDTHHMM format, or press Enter to use current time): ")
                if time_to_input.strip():
                    time_to = time_to_input
                else:
                    time_to = datetime.now().strftime('%Y%m%dT%H%M')
                break

            else:
                console.print('Invalid Choice. Please Select 1-6.', style="bold red")

    else:
        time_from = None
        time_to = None
        console.print("No Specific Date Range Selected, Moving on to Next Step...", style="bright_green") 


# ==================================================================================================================== #  

# Sort Logic  
    while True: 
        console.print("How Would You Like to Sort The Results:", style="bold bright_blue") 
        console.print('1. Latest (latest articles first)', style="bright_green") 
        console.print('2. Earliest (oldest article first)', style="bright_green") 
        console.print('3. Relevance (sort by relevance to search case)', style="bright_green") 
        choice = input("Select an Option (1 - 3): ") 

        if choice == '1': 
            sort = 'LATEST'
            break 

        elif choice == '2': 
            sort = 'EARLIEST' 
            break 

        elif choice == '3': 
            sort = 'RELEVANCE' 
            break 

        else: 
            console.print("Invalid Selection, Please Select an Option (1 - 3)...", style="bold red") 

# ==================================================================================================================== #  

# Limit Logic (How Many Results Would You Like) 
    console.print("How Many Results Would You Like?", style="bold bright_blue")
    while True: 
        try:
            limit = int(input("Enter Number of Results (1 - 1000): ")) 
            if 1 <= limit <= 1000:
                break
            else:
                console.print("Please enter a number between 1 and 1000", style="bold red")
        except ValueError:
            console.print("Please enter a valid number", style="bold red")

# ==================================================================================================================== #  

# Format URL Params - Build params dict dynamically to exclude None values
    base_url = 'https://www.alphavantage.co/query'  # Fixed URL
    params = { 
        'function': fn,  
        'apikey': api_key
    } 
    
    # Only add parameters that are not None
    if ticker_list:
        params['tickers'] = ticker_list  # Fixed parameter name
    if topic:
        params['topics'] = topic
    if time_from:
        params['time_from'] = time_from
    if time_to:
        params['time_to'] = time_to
    if sort:
        params['sort'] = sort
    if limit:
        params['limit'] = limit

# ==================================================================================================================== #  
# Build the Request URL 
    News_Sentiment_Url = f"{base_url}?{urlencode(params)}" 
    print(f"Request URL: {News_Sentiment_Url}")  # For debugging

    # Fetch and Format as JSON 
    response = requests.get(News_Sentiment_Url) 
    data = response.json() 

    Path("p_sql_two/News_Sentiment_JSON").mkdir(exist_ok=True) 

    # Save the results to a filename based on available parameters (ticker OR topic) 
    filename_parts = []
    if ticker_list:
        # Replace commas and special characters for filename
        clean_tickers = ticker_list.replace(',', '_').replace(':', '_')
        filename_parts.append(clean_tickers)
    if topic:
        filename_parts.append(topic)
    
    if filename_parts:
        filename_base = '_'.join(filename_parts)
    else:
        filename_base = 'general_news'
        
    filename = f'p_sql_two/News_Sentiment_JSON/{filename_base}_News_&_Sentiments_{limit}.json'   
    with open(filename, 'w') as news_sentiments: 
        json.dump(data, news_sentiments, indent = 4) 
        
    print(f"Successfully saved news sentiment data to: {filename}")

if __name__ == '__main__': 
    fetch_market_news_and_sentiments()