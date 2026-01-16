# This API returns the full historical options chain for a specific symbol on a specific date, covering 15+ years of history. Implied volatility (IV) and common Greeks (e.g., delta, gamma, theta, vega, rho) are also returned. Option chains are sorted by expiration dates in chronological order. Within the same expiration date, contracts are sorted by strike prices from low to high.
import email.mime 
import os 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 

from rich.console import Console 
from rich.panel import Panel 
from rich.text import Text
console = Console() 

import requests 
import pandas as pd 
import csv 
import json 

# ==================================================================================================================== #  
# Historical Options Trending

# This API returns the full historical options chain for a specific symbol on a specific date, covering 15+ years of history. 
# Implied volatility (IV) and common Greeks (e.g., delta, gamma, theta, vega, rho) are also returned. 
# Option chains are sorted by expiration dates in chronological order. 
# Within the same expiration date, contracts are sorted by strike prices from low to high.

# API Parameters # 
# 1. function (required) = 'REALTIME_OPTIONS'  

# 2. symbol (required) 
  
# 3. date (optional) - By default, the date parameter is not set and the API will return data for the previous trading session. Any date later than 2008-01-01 is accepted. For example, date=2017-11-15

# 4. datetype (optional) - json by default, csv optional 

# 5. apikey 
# ==================================================================================================================== #  
# ==================================================================================================================== #  

def historical_options_intro(): 
    console = Console()
    
    # Create the main title
    title = Text("Alpha Vantage HISTORICAL Options - Time Machine for Options Data", style="bold blue")
    
    # Create the description content
    description = Text()
    description.append("🕐 WHAT THIS TOOL UNLOCKS:\n", style="bold green")
    description.append("Travel back in time to see exactly what options chains looked like on any trading day ")
    description.append("since 2008. Get complete historical option chains with pricing, Greeks, and implied volatility ")
    description.append("as they existed on specific dates - perfect for backtesting and research.\n\n")
    
    description.append("📚 COMPREHENSIVE HISTORICAL DATA:\n", style="bold yellow")
    description.append("• 15+ Years of History: Options data back to 2008 and beyond\n")
    description.append("• Complete Option Chains: All strikes and expirations as they existed\n") 
    description.append("• Full Greeks Suite: Delta, gamma, theta, vega, rho for every contract\n")
    description.append("• Historical Implied Volatility: IV levels from any past date\n")
    description.append("• Exact Pricing: Bid, ask, last prices from specific trading sessions\n")
    description.append("• Smart Organization: Sorted by expiration, then strike price\n\n")
    
    description.append("🎯 PERFECT FOR:\n", style="bold cyan")
    description.append("• Strategy backtesting and performance analysis\n")
    description.append("• Academic research on options pricing models\n")
    description.append("• Volatility pattern analysis over time\n")
    description.append("• Options market behavior during major events\n")
    description.append("• Risk model validation and stress testing\n")
    description.append("• Historical volatility vs implied volatility studies\n\n")
    
    description.append("🔬 RESEARCH APPLICATIONS:\n", style="bold magenta")
    description.append("• Event Studies: How did options react to earnings, splits, or news?\n")
    description.append("• Market Crash Analysis: Options behavior during 2008, 2020 crashes\n")
    description.append("• Volatility Surface Evolution: Track how IV surfaces changed\n")
    description.append("• Strategy Performance: Test covered calls, straddles historically\n")
    description.append("• Greeks Behavior: Study how options sensitivities evolved\n\n")
    
    description.append("💡 POWERFUL SCENARIOS:\n", style="bold red")
    description.append("• \"What if I bought Tesla calls before earnings in 2019?\" → Historical backtesting\n")
    description.append("• \"How did Apple options behave during iPhone launches?\" → Event analysis\n")
    description.append("• \"What was IV doing before the 2020 crash?\" → Pre-crisis volatility patterns\n")
    description.append("• \"Did my strategy work in past bear markets?\" → Multi-year backtesting\n")
    description.append("• \"How accurate were pricing models in 2015?\" → Model validation\n\n")
    
    description.append("📊 DATA ADVANTAGES:\n", style="bold cyan")
    description.append("• Point-in-Time Accuracy: Exact data as it existed, no survivorship bias\n")
    description.append("• Complete Context: Full chains show market sentiment and positioning\n")
    description.append("• Greeks Included: No need to recalculate complex derivatives\n")
    description.append("• Flexible Dates: Any trading day since 2008 is available\n")
    description.append("• Research Ready: JSON or CSV formats for any analysis tool\n\n")
    
    description.append("🚀 PRO TIP: ", style="bold yellow")
    description.append("Compare historical IV to realized volatility to identify when options were ")
    description.append("consistently over/underpriced - a goldmine for systematic strategies!\n\n")
    
    description.append("Ready to explore the options market's history!", style="bold white")
    
    # Create and display the panel
    panel = Panel(
        description,
        title=title,
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()  # Add some spacing



# ==================================================================================================================== # 
# ==================================================================================================================== # 

def fetch_historical_options_chain(): 
    print('')
    print('') 

    # ==================================================================================================================== # 
    # Print Intro Panel 
    historical_options_intro() 
    # ==================================================================================================================== # 

    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'HISTORICAL_OPTIONS' 
    ticker = input('Enter Ticker: ')  
    data_range = input('Enter Starting Date for Historical Data (YYYY-MM-DD): ')
    format = 'csv' 

    # Build API Params 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': ticker,  
        'date': data_range, 
        'datatype': format, 
        'apikey': api_key
    } 

    # Build Request URL 
    historical_options_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(historical_options_url) 
    Path('Historical_Options_CSV').mkdir(exist_ok=True) 

    filename = f'Historical_Options_CSV/{ticker}_{data_range}_{fn}.csv' 
    with open (filename, 'w') as csv_file: 
        csv_file.write(response.text) 

    print(f'Successfully Saved Historical Options Data for {ticker} as {filename}')  

if __name__ == '__main__': 
    fetch_historical_options_chain()