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
# API Parameters # 
# 1. function (required) = 'REALTIME_OPTIONS'  

# 2. symbol (required) 

# 3. require_greeks (optional) - Enable greeks and Implied Volatility Fields (IV).
#    a. required_greeks = false (default) 
#    b. required_greeks = true 
  
# 4. contract (optional) - US options contract you would like to specify (by defualt, contract param not set & returns entire option chain for given symbol )

# 5. datetype - json by default, csv optional 

# 6. apikey 
# ==================================================================================================================== #  
# ==================================================================================================================== # 

def live_options_intro(): 
    console = Console()
    
    # Create the main title
    title = Text("Alpha Vantage REALTIME Options - Live Market Data", style="bold blue")
    
    # Create the description content
    description = Text()
    description.append("⚡ WHAT THIS TOOL DELIVERS:\n", style="bold green")
    description.append("Access live, real-time options data for the entire US options market. Get complete option chains ")
    description.append("with current pricing, volume, and advanced Greeks calculations. This is institutional-grade ")
    description.append("options data that updates in real-time as the market moves.\n\n")
    
    description.append("📋 COMPREHENSIVE OPTIONS DATA:\n", style="bold yellow")
    description.append("• Complete Option Chains: All strikes and expirations for any stock\n")
    description.append("• Live Pricing: Real-time bid, ask, last price, and volume data\n") 
    description.append("• Advanced Greeks: Delta, gamma, theta, vega, and rho (optional)\n")
    description.append("• Implied Volatility: Current IV levels for each contract\n")
    description.append("• Open Interest: See where the smart money is positioned\n")
    description.append("• Contract Details: Strike prices, expiration dates, contract types\n\n")
    
    description.append("🎯 PERFECT FOR:\n", style="bold cyan")
    description.append("• Options trading and strategy development\n")
    description.append("• Volatility analysis and implied volatility tracking\n")
    description.append("• Greeks-based risk management\n")
    description.append("• Options market making and arbitrage\n")
    description.append("• Institutional portfolio hedging strategies\n")
    description.append("• Academic research on options pricing\n\n")
    
    description.append("🔥 KEY FEATURES:\n", style="bold magenta")
    description.append("• Real-Time Data: Live market updates, not delayed\n")
    description.append("• Full Market Coverage: Complete US options universe\n")
    description.append("• Smart Organization: Sorted by expiration, then by strike price\n")
    description.append("• Flexible Output: JSON for programming, CSV for spreadsheets\n")
    description.append("• Optional Greeks: Enable advanced risk metrics when needed\n")
    description.append("• Single Contract Focus: Target specific options contracts\n\n")
    
    description.append("💰 TRADING SCENARIOS:\n", style="bold red")
    description.append("• \"What's the current IV on Tesla weekly calls?\" → Full chain analysis\n")
    description.append("• \"How sensitive is this option to price moves?\" → Check delta values\n")
    description.append("• \"Which strikes have the most volume?\" → Review trading activity\n")
    description.append("• \"What's the time decay on my positions?\" → Monitor theta values\n")
    description.append("• \"Where are support/resistance levels?\" → Analyze open interest\n\n")
    
    description.append("⚠️ PREMIUM FEATURE:\n", style="bold yellow")
    description.append("This is professional-grade options data designed for serious traders, institutions, ")
    description.append("and quantitative researchers who need real-time accuracy and comprehensive coverage.\n\n")
    
    description.append("🚀 PRO TIP: ", style="bold cyan")
    description.append("Enable Greeks and IV calculations for advanced options strategies - they're essential ")
    description.append("for proper risk management and position sizing!\n\n")
    
    description.append("Ready to access real-time options market data!", style="bold white")
    
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

def fetch_live_options_chain(): 
    print('')
    print('') 

    # ==================================================================================================================== # 
    # Print Intro Panel 
    live_options_intro() 
    # ==================================================================================================================== # 

    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'REALTIME_OPTIONS' 
    ticker = input('Enter Ticker: ') 
    greeks_enabled = input('Include Greeks (true/false): ') 
    format = 'csv' 

    # Build API Params 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': ticker, 
        'require_greeks': greeks_enabled, 
        'datatype': format, 
        'apikey': api_key
    } 

    # Build Request URL 
    realtime_options_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(realtime_options_url) 
    Path('Realtime_Options_CSV').mkdir(exist_ok=True) 

    filename = f'Realtime_Options_CSV/{ticker}_{fn}.csv' 
    with open (filename, 'w') as csv_file: 
        csv_file.write(response.text) 

    print(f'Successfully Saved Realtime Options Data for {ticker} as {filename}')  
    # ==================================================================================================================== # 
    # ==================================================================================================================== # 

if __name__ == '__main__': 
    fetch_live_options_chain()
