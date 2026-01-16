import os 
import email.mime 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 

from rich.console import Console 
from rich.panel import Panel 
from rich.text import Text 
console = Console() 

import requests 
import pandas as pd 
import json 

# ==================================================================================================================== # 
# Advanced Analytics (Fixed Window) # 
# This endpoint returns a rich set of advanced analytics metrics (e.g., total return, variance, auto-correlation, etc.) for a given time series over a fixed temporal window.

# ==== API Parameters ==== #
# 1. ❚ Required: function - The function of your choice. In this case, function=ANALYTICS_FIXED_WINDOW

# 2. ❚ Required: SYMBOLS - A list of symbols for the calculation. It can be a comma separated list of symbols as a string. Free API keys can specify up to 5 symbols per API request. Premium API keys can specify up to 50 symbols per API request.

# 3. ❚ Required: RANGE - This is the date range for the series being requested. By default, the date range is the full set of data for the equity history. This can be further modified by the LIMIT variable.
#   RANGE can take certain text values as inputs. They are:
#       a. full
#       b. N}day
#       c. {N}week
#       d. {N}month
#       e. {N}year
# For intraday time series, the following RANGE values are also accepted:
#       a. {N}minute
#       b. {N}hour

# Aside from the “full” value which represents the entire time series, the other values specify an interval to return the series for as measured backwards from the current date/time.
# To specify start & end dates for your analytics calcuation, simply add two RANGE parameters in your API request. For example: RANGE=2023-07-01&RANGE=2023-08-31 or RANGE=2020-12-01T00:04:00&RANGE=2020-12-06T23:59:59 with minute-level precision for intraday analytics. If the end date is missing, the end date is assumed to be the last trading date. In addition, you can request a full month of data by using YYYY-MM format like 2020-12. One day of intraday data can be requested by using YYYY-MM-DD format like 2020-12-06

# 4. ❚ Optional: OHLC - This allows you to choose which open, high, low, or close field the calculation will be performed on. By default, OHLC=close. Valid values for these fields are open, high, low, close.

# 5. ❚ Required: INTERVAL - Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, DAILY, WEEKLY, MONTHLY.

# 6. ❚ Required: WINDOW_SIZE - An integer representing the size of the moving window. A hard lower boundary of 10 has been set though it is recommended to make this window larger to make sure the running calculations are statistically significant.

# 7. ❚ Required: CALCULATIONS - A comma separated list of the analytics metrics you would like to calculate:
#       a. MIN: The minimum return (largest negative or smallest positive) for all values in the series
#       b. MAX: The maximum return for all values in the series
#       c. MEAN: The mean of all returns in the series
#       d. MEDIAN: The median of all returns in the series
#       e. CUMULATIVE_RETURN: The total return from the beginning to the end of the series range
#       f. VARIANCE: The population variance of returns in the series range. Optionally, you can use VARIANCE(annualized=True)to normalize the output to an annual value. By default, the variance is not annualized.
#       g. STDDEV: The population standard deviation of returns in the series range for each symbol. Optionally, you can use STDDEV(annualized=True)to normalize the output to an annual value. By default, the standard deviation is not annualized.
#       h. MAX_DRAWDOWN: Largest peak to trough interval for each symbol in the series range
#       i. HISTOGRAM: For each symbol, place the observed total returns in bins. By default, bins=10. Use HISTOGRAM(bins=20) to specify a custom bin value (e.g., 20).
#       j. AUTOCORRELATION: For each symbol place, calculate the autocorrelation for the given lag (e.g., the lag in neighboring points for the autocorrelation calculation). By default, lag=1. Use AUTOCORRELATION(lag=2) to specify a custom lag value (e.g., 2).
#       k. COVARIANCE: Returns a covariance matrix for the input symbols. Optionally, you can use COVARIANCE(annualized=True)to normalize the output to an annual value. By default, the covariance is not annualized.
#       l. CORRELATION: Returns a correlation matrix for the input symbols, using the PEARSON method as default. You can also specify the KENDALL or SPEARMAN method through CORRELATION(method=KENDALL) or CORRELATION(method=SPEARMAN), respectively.

# 8. ❚ Required: apikey
# ==================================================================================================================== #  
def sliding_window_intro():
    console = Console()
    print('')
    print('')
    
    # Create the main title
    title = Text("Alpha Vantage Advanced Analytics - Sliding Window", style="bold blue")
    
    # Create the description content
    description = Text()
    description.append("📈 WHAT THIS TOOL DOES:\n", style="bold green")
    description.append("This tool analyzes how financial metrics evolve over time using a moving window approach. ")
    description.append("Instead of calculating metrics for a single period, it shows you how volatility, correlations, ")
    description.append("and returns change as the analysis window slides through your data.\n\n")
    
    description.append("🔄 HOW SLIDING WINDOWS WORK:\n", style="bold yellow")
    description.append("Imagine analyzing 100-day volatility, then moving forward one day and recalculating with ")
    description.append("the next 100 days. This creates a timeline showing how metrics trend over time:\n")
    description.append("• Day 1-100: Calculate metric → Data Point 1\n")
    description.append("• Day 2-101: Calculate metric → Data Point 2\n")
    description.append("• Day 3-102: Calculate metric → Data Point 3\n")
    description.append("• And so on...\n\n")
    
    description.append("💡 KEY INSIGHTS YOU'LL DISCOVER:\n", style="bold cyan")
    description.append("• Volatility Trends: See when stocks became more or less risky over time\n")
    description.append("• Correlation Evolution: Track how asset relationships strengthen or weaken\n") 
    description.append("• Return Patterns: Identify periods of consistent performance changes\n")
    description.append("• Market Regime Changes: Spot transitions between bull/bear markets\n")
    description.append("• Risk Management: Monitor when portfolios became riskier or safer\n\n")
    
    description.append("🎯 PERFECT FOR:\n", style="bold magenta")
    description.append("• Dynamic portfolio rebalancing strategies\n")
    description.append("• Market timing and regime detection\n")
    description.append("• Risk management and early warning systems\n")
    description.append("• Quantitative research and backtesting\n")
    description.append("• Understanding market cycles and trends\n\n")
    
    description.append("⚙️ TECHNICAL CAPABILITIES:\n", style="bold red")
    description.append("• Window Sizes: Minimum 10 data points (larger recommended for significance)\n")
    description.append("• Multiple Metrics: Mean, variance, correlation matrices, and more\n")
    description.append("• Time Flexibility: From 1-minute to monthly intervals\n")
    description.append("• Multi-Asset Analysis: Up to 50 symbols simultaneously (Premium)\n")
    description.append("• Custom Date Ranges: Analyze specific periods or full history\n\n")
    
    description.append("🚨 PRO TIP: ", style="bold yellow")
    description.append("Larger window sizes provide more statistically significant results but show less granular changes. ")
    description.append("Smaller windows are more sensitive but may be noisier!\n\n")
    
    description.append("Ready to track how your financial metrics evolve over time!", style="bold white")
    
    # Create and display the panel
    panel = Panel(
        description,
        title=title,
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()  # Add some spacing


def advanced_analytics_sliding_window(): 
    print('') 
    print('') 

    # ==================================================================================================================== # 
    # Print Intro Panel 
    sliding_window_intro() 
    # ==================================================================================================================== # 
    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory") 
        exit() 


    fn = 'ANALYTICS_SLIDING_WINDOW' 
    tickers = input("Enter Ticker(s) (seperated by commas, up to 50 tickers at once): ")   

    print("For Now, time range for all of equity history = 'full'... ") 
    time_range = input("Enter Range (full): ") 

    print('Valid Time Intervals: 1min, 5min, 15min, 30min, 60min, DAILY, WEEKLY, MONTHLY ') 
    time_interval = input("Select Valid Interval for Time Series: ") 

    print("Select Window_Size - A hard lower boundary of 10 has been set though it is recommended to make this window larger to make sure the running calculations are statistically significant.")
    window_size = int(input('Enter Window_Size (integer): ')) 

    print("Valid Calculation Fields for Data: ") 
    print('1. MIN: The minimum return (largest negative or smallest positive) for all values in the series')
    print('2. MAX: The maximum return for all values in the series')
    print('3. MEAN: The mean of all returns in the series')
    print('4. MEDIAN: The median of all returns in the series')
    print('5. CUMULATIVE_RETURN: The total return from the beginning to the end of the series range')
    print('6. VARIANCE: The population variance of returns in the series range. Optionally, you can use VARIANCE(annualized=True)to normalize the output to an annual value. By default, the variance is not annualized.')
    print('7. STDDEV: The population standard deviation of returns in the series range for each symbol. Optionally, you can use STDDEV(annualized=True)to normalize the output to an annual value. By default, the standard deviation is not annualized.')
    print('8. MAX_DRAWDOWN: Largest peak to trough interval for each symbol in the series range')
    print('9. HISTOGRAM: For each symbol, place the observed total returns in bins. By default, bins=10. Use HISTOGRAM(bins=20) to specify a custom bin value (e.g., 20).')
    print('10. AUTOCORRELATION: For each symbol place, calculate the autocorrelation for the given lag (e.g., the lag in neighboring points for the autocorrelation calculation). By default, lag=1. Use AUTOCORRELATION(lag=2) to specify a custom lag value (e.g., 2).')
    print('11. COVARIANCE: Returns a covariance matrix for the input symbols. Optionally, you can use COVARIANCE(annualized=True)to normalize the output to an annual value. By default, the covariance is not annualized.')
    print('12. CORRELATION: Returns a correlation matrix for the input symbols, using the PEARSON method as default. You can also specify the KENDALL or SPEARMAN method through CORRELATION(method=KENDALL) or CORRELATION(method=SPEARMAN), respectively.') 
    calculation_metrics = input('Select Calculation Metrics (seperated by commas): ')  


    # Build API Params 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn,  
        'SYMBOLS': tickers, 
        'RANGE': time_range, 
        'INTERVAL': time_interval, 
        'WINDOW_SIZE': window_size, 
        'CALCULATIONS': calculation_metrics, 
        'apikey': api_key
    } 

    # Build Request URL 
    analytics_sliding_window_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(analytics_sliding_window_url)  
    data = response.json() 
    Path('Analytics_JSON/Sliding_Window').mkdir(exist_ok=True) 

    filename = f'Analytics_JSON/Sliding_Window/{fn}.json' 
    with open (filename, 'w') as analytics_sliding_window_json: 
        json.dump(data, analytics_sliding_window_json, indent=2)  


    print(f'Successfully Saved Advanced Analytics - Sliding Window to {filename}')  
    # ==================================================================================================================== # 

if __name__ == '__main__': 
    advanced_analytics_sliding_window()