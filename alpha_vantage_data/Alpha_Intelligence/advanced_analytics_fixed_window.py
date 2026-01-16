import os 
import email.mime 
from dotenv import load_dotenv 
from urllib.parse import urlencode 
from pathlib import Path 
import pandas as pd 

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

# Aside from the "full" value which represents the entire time series, the other values specify an interval to return the series for as measured backwards from the current date/time.
# To specify start & end dates for your analytics calcuation, simply add two RANGE parameters in your API request. For example: RANGE=2023-07-01&RANGE=2023-08-31 or RANGE=2020-12-01T00:04:00&RANGE=2020-12-06T23:59:59 with minute-level precision for intraday analytics. If the end date is missing, the end date is assumed to be the last trading date. In addition, you can request a full month of data by using YYYY-MM format like 2020-12. One day of intraday data can be requested by using YYYY-MM-DD format like 2020-12-06

# 4. ❚ Optional: OHLC - This allows you to choose which open, high, low, or close field the calculation will be performed on. By default, OHLC=close. Valid values for these fields are open, high, low, close.

# 5. ❚ Required: INTERVAL - Time interval between two consecutive data points in the time series. The following values are supported: 1min, 5min, 15min, 30min, 60min, DAILY, WEEKLY, MONTHLY.

# 6. ❚ Required: CALCULATIONS - A comma separated list of the analytics metrics you would like to calculate:
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

# 7. ❚ Required: apikey
# ==================================================================================================================== #  
def fixed_window_intro(): 
    console = Console()

    print('')
    print('')
    
    # Create the main title
    title = Text("Alpha Vantage Advanced Analytics - Fixed Window", style="bold blue")
    
    # Create the description content
    description = Text()
    description.append("📊 WHAT THIS TOOL DOES:\n", style="bold green")
    description.append("This tool provides comprehensive statistical analysis of stock price movements over specific time periods. ")
    description.append("It calculates advanced financial metrics that help you understand risk, returns, and correlations.\n\n")
    
    description.append("💡 KEY INSIGHTS YOU'LL GET:\n", style="bold yellow")
    description.append("• Risk Metrics: Variance, standard deviation, and maximum drawdown to assess volatility\n")
    description.append("• Return Analysis: Mean, median, cumulative returns, and return distributions\n") 
    description.append("• Statistical Properties: Autocorrelation patterns and return histograms\n")
    description.append("• Portfolio Analysis: Covariance and correlation matrices for multiple stocks\n")
    description.append("• Performance Benchmarks: Min/max returns and risk-adjusted metrics\n\n")
    
    description.append("🎯 PERFECT FOR:\n", style="bold cyan")
    description.append("• Portfolio optimization and risk assessment\n")
    description.append("• Comparing volatility across different stocks or time periods\n")
    description.append("• Understanding correlation relationships between assets\n")
    description.append("• Backtesting investment strategies\n")
    description.append("• Academic research and financial modeling\n\n")
    
    description.append("📈 SUPPORTED ANALYSIS:\n", style="bold magenta")
    description.append("• Up to 50 symbols simultaneously (Premium) or 5 symbols (Free)\n")
    description.append("• Multiple time intervals: 1min to Monthly data\n")
    description.append("• Flexible date ranges: Days, weeks, months, years, or custom periods\n")
    description.append("• 12 different analytical metrics available\n\n")
    
    description.append("Ready to dive deep into your financial data analysis!", style="bold white")
    
    # Create and display the panel
    panel = Panel(
        description,
        title=title,
        border_style="blue",
        padding=(1, 2)
    )
    
    console.print(panel)
    console.print()  # Add some spacing


def advanced_analytics_fixed_window(): 
    print('') 
    print('')

    # ==================================================================================================================== # 
    # Print Intro Panel 
    fixed_window_intro()
    # ==================================================================================================================== # 

    load_dotenv() 
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY") 
    if not api_key: 
        console.print("ERROR: Unable to Locate API Key. Please Make Sure All API Keys are stored in a .env file in the root directory", style="bold red") 
        exit() 


    fn = 'ANALYTICS_FIXED_WINDOW' 
    tickers = input("Enter Ticker(s) (separated by commas, up to 50 tickers at once): ")   

    console.print("For Now, time range for all of equity history = 'full'...", style="bright_green") 
    time_range = input("Enter Range (full): ") 

    console.print("Valid Time Intervals: 1min, 5min, 15min, 30min, 60min, DAILY, WEEKLY, MONTHLY", style="bold bright_blue") 
    time_interval = input("Select Valid Interval for Time Series: ") 

    console.print("Valid Calculation Fields for Data:", style="bold bright_blue") 
    console.print('1. MIN: The minimum return (largest negative or smallest positive) for all values in the series', style="bright_green")
    console.print('2. MAX: The maximum return for all values in the series', style="bright_green")
    console.print('3. MEAN: The mean of all returns in the series', style="bright_green")
    console.print('4. MEDIAN: The median of all returns in the series', style="bright_green")
    console.print('5. CUMULATIVE_RETURN: The total return from the beginning to the end of the series range', style="bright_green")
    console.print('6. VARIANCE: The population variance of returns in the series range. Optionally, you can use VARIANCE(annualized=True)to normalize the output to an annual value. By default, the variance is not annualized.', style="bright_green")
    console.print('7. STDDEV: The population standard deviation of returns in the series range for each symbol. Optionally, you can use STDDEV(annualized=True)to normalize the output to an annual value. By default, the standard deviation is not annualized.', style="bright_green")
    console.print('8. MAX_DRAWDOWN: Largest peak to trough interval for each symbol in the series range', style="bright_green")
    console.print('9. HISTOGRAM: For each symbol, place the observed total returns in bins. By default, bins=10. Use HISTOGRAM(bins=20) to specify a custom bin value (e.g., 20).', style="bright_green")
    console.print('10. AUTOCORRELATION: For each symbol place, calculate the autocorrelation for the given lag (e.g., the lag in neighboring points for the autocorrelation calculation). By default, lag=1. Use AUTOCORRELATION(lag=2) to specify a custom lag value (e.g., 2).', style="bright_green")
    console.print('11. COVARIANCE: Returns a covariance matrix for the input symbols. Optionally, you can use COVARIANCE(annualized=True)to normalize the output to an annual value. By default, the covariance is not annualized.', style="bright_green")
    console.print('12. CORRELATION: Returns a correlation matrix for the input symbols, using the PEARSON method as default. You can also specify the KENDALL or SPEARMAN method through CORRELATION(method=KENDALL) or CORRELATION(method=SPEARMAN), respectively.', style="bright_green") 
    calculation_metrics = input('Select Calculation Metrics (separated by commas): ')  


    # Build API Params 
    base_url='https://www.alphavantage.co/query' 
    params = { 
        'function': fn,  
        'SYMBOLS': tickers, 
        'RANGE': time_range, 
        'INTERVAL': time_interval, 
        'CALCULATIONS': calculation_metrics, 
        'apikey': api_key
    } 

    # Build Request URL 
    analytics_fixed_window_url = f'{base_url}?{urlencode(params)}' 

    # Fetch and Save Data 
    response = requests.get(analytics_fixed_window_url)  
    data = response.json() 
    Path('p_sql_two/Analytics_JSON/Fixed_Window').mkdir(parents=True, exist_ok=True) 

    filename = f'p_sql_two/Analytics_JSON/Fixed_Window/{fn}.json' 
    with open (filename, 'w') as analytics_fixed_window_json: 
        json.dump(data, analytics_fixed_window_json, indent=2)   


    console.print(f'Successfully Saved Advanced Analytics - Fixed Window to {filename}', style="bold bright_green")  

    df = pd.DataFrame(data['payload']) 
    csv_filename = f'Analytics_JSON/Fixed_Window/{fn}.csv'
    df.to_csv(csv_filename)

    console.print(f'Successfully Saved DataFrame to {csv_filename}', style="bold bright_green")
    print(df.head())
    # ==================================================================================================================== # 

if __name__ == '__main__': 
    advanced_analytics_fixed_window()