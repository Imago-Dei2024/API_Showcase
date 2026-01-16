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

# ==================================================================================================================== # 
# API PAMETERS # 
# 1. function = 'OVERVIEW' 
# 2. symbol 
# 3. apikey 
# ==================================================================================================================== # 
# ==================================================================================================================== # 
def company_overview_intro(): 
    console = Console()
    
    print('')
    print('')

    # Create the main title
    title = Text("Alpha Vantage Company Overview - Fundamental Analysis", style="bold blue")
    
    # Create the description content
    description = Text()
    description.append("🏢 WHAT THIS TOOL PROVIDES:\n", style="bold green")
    description.append("Get a comprehensive snapshot of any publicly traded company's financial health and key metrics. ")
    description.append("This is your one-stop source for essential company fundamentals, ratios, and business information ")
    description.append("that professional investors use to make informed decisions.\n\n")
    
    description.append("📊 KEY DATA YOU'LL RECEIVE:\n", style="bold yellow")
    description.append("• Company Basics: Name, sector, industry, description, and headquarters\n")
    description.append("• Financial Health: Market cap, revenue, profit margins, and debt ratios\n") 
    description.append("• Valuation Metrics: P/E ratio, P/B ratio, PEG ratio, and dividend yield\n")
    description.append("• Performance Indicators: ROE, ROA, profit margins, and earnings growth\n")
    description.append("• Stock Metrics: Beta, 52-week highs/lows, shares outstanding\n")
    description.append("• Dividend Information: Yield, payout ratio, and payment dates\n\n")
    
    description.append("💡 PERFECT FOR:\n", style="bold cyan")
    description.append("• Stock screening and fundamental analysis\n")
    description.append("• Company research before investing\n")
    description.append("• Comparing financial health across competitors\n")
    description.append("• Building investment portfolios based on fundamentals\n")
    description.append("• Academic research and financial modeling\n\n")
    
    description.append("⚡ KEY ADVANTAGES:\n", style="bold magenta")
    description.append("• Fresh Data: Updated same day companies report earnings\n")
    description.append("• Comprehensive: 50+ financial metrics in one API call\n")
    description.append("• Ready-to-Use: Pre-calculated ratios save you time\n")
    description.append("• Professional Grade: Institutional-quality financial data\n")
    description.append("• Simple Integration: Single ticker symbol gets everything\n\n")
    
    description.append("🎯 IDEAL USER SCENARIOS:\n", style="bold red")
    description.append("• \"Is this stock fairly valued?\" → Check P/E, P/B, and PEG ratios\n")
    description.append("• \"How profitable is this company?\" → Review profit margins and ROE\n")
    description.append("• \"Is this a dividend stock?\" → Examine dividend yield and payout ratio\n")
    description.append("• \"How risky is this investment?\" → Analyze beta and debt ratios\n")
    description.append("• \"What sector is this in?\" → Get industry classification details\n\n")
    
    description.append("📈 DATA FRESHNESS:\n", style="bold yellow")
    description.append("Financial data is refreshed the same day companies report earnings, ")
    description.append("ensuring you're working with the most current fundamental information available!\n\n")
    
    description.append("Ready to dive deep into company fundamentals!", style="bold white")
    
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

def fetch_company_overview(): 
    print('')
    print('')
    
    # ==================================================================================================================== #  
    # Print Intro Panel 
    company_overview_intro() 
    # ==================================================================================================================== #  

    load_dotenv() 
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY') 
    if not api_key: 
        print('ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory') 
        exit()  

    ticker = input("Enter Ticker: ") 
    fn = 'OVERVIEW' 

    # Build URL Params 
    base_url = 'https://www.alphavantage.co/query' 
    params = { 
        'function': fn, 
        'symbol': ticker, 
        'apikey': api_key 
    }

    # Build Request URL 
    Overview_URL = f'{base_url}?{urlencode(params)}' 

    # Fetch and Format as JSON 
    response = requests.get(Overview_URL) 
    data = response.json() 

    Path('Company_Overviews_JSON').mkdir(exist_ok=True) 

    # Save the File 
    filename = f"Company_Overviews_JSON/{ticker}_Overview.json" 
    with open (filename, 'w') as company_overview: 
        json.dump(data, company_overview, indent = 2) 
    
    print(f'Successfully Printed {ticker}_company_overview.json to {filename}')
    # ==================================================================================================================== # 

if __name__ == '__main__': 
    fetch_company_overview()
