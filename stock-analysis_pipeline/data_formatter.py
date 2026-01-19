# ==================================================================================================================== #  
# Data Formatter: Formats numerical values into readable formats - currencies ($1.23B), 
# percentages (15.67%), and ratios (23.45) for dashboard display 
# ==================================================================================================================== #  


import json 
from pathlib import Path

from altair import Type 

def currency_format(c, fmt='${:,.0f}'): 
    if c is None or c == 'N/A' or c == 'None' or c == '': 
        return 'N/A' 
    try: 
        return fmt.format(float(c)) 
    except (ValueError, TypeError): 
        return 'N/A' 

def currency_format_decimal(c2, fmt='${:,.2f}'): 
    if c2 is None or c2 == 'N/A' or c2 == 'None' or c2 == '': 
        return 'N/A' 
    try: 
        return fmt.format(float(c2)) 
    except (ValueError, TypeError): 
        return 'N/A' 

def number_format(n, fmt='{:,.2f}'): 
    if n is None or n == 'N/A' or n == 'None' or n =='': 
        return 'N/A' 
    try: 
        return fmt.format(float(n)) 
    except (ValueError, TypeError): 
        return 'N/A' 
    
def rate_format(r, fmt='{:.2%}'): 
    if r is None or r == 'N/A' or r == 'None' or r == '': 
        return 'N/A' 
    try: 
        return fmt.format(float(r)) 
    except (ValueError, TypeError): 
        return 'N/A' 
    
def format_company_info(data): 
    return { 
        'Company Name': data.get('name', 'N/A'), 
        'Symbol': data.get('symbol', 'N/A'), 
        'Exchange': data.get('exchange', 'N/A'), 
        'Sector': data.get('sector', 'N/A'), 
        'Industry': data.get('industry', 'N/A'), 
        'Description': data.get('description', 'N/A')
    } 

def format_financial_metrics(data): 
    return { 
        'Market Cap': currency_format(data.get('market_cap')), 
        'Revenue (TTM)': currency_format(data.get('revenue_ttm')), 
        'Gross Profit (TTM)': currency_format(data.get('gross_profit_ttm')), 
        'EBITDA': currency_format(data.get('ebitda')), 
        'Profit Margin': rate_format(data.get('profit_margin')) 
    } 

def format_valuation_metrics(data): 
    return { 
        'P/E Ratio': number_format(data.get('pe_ratio')), 
        'PEG Ratio': number_format(data.get('peg_ratio')), 
        'Price-to-Book(P/B) Ratio': number_format(data.get('price_to_book')), 
        'Price-to-Sales(P/S) Ratio': number_format(data.get('price_to_sales')), 
        'EV-to-Revenue(EV/R) Ratio': number_format(data.get('ev_to_revenue')), 
        'EV/EBITDA Ratio': number_format(data.get('ev_to_ebitda')) 
    } 

def format_profitability_metrics(data): 
    return { 
        'Profit Margin': rate_format(data.get('profit_margin')), 
        'Operating Margin': rate_format(data.get('operating_margin')), 
        'Return-on-Assets (ROA)': rate_format(data.get('return_on_assets')), 
        'Return-on-Equity (ROE)': rate_format(data.get('return_on_equity'))
    } 

def format_per_share_metrics(data):
    return {
        'EPS': currency_format_decimal(data.get('eps')),
        'Diluted EPS': currency_format_decimal(data.get('diluted_eps')),
        'Book Value': currency_format_decimal(data.get('book_value')),
        'Dividend Per Share': currency_format_decimal(data.get('dividend_per_share')),
        'Dividend Yield': rate_format(data.get('dividend_yield'))
    }

def format_balance_sheet(data):
    return {
        'Fiscal Date': data.get('fiscal_date', 'N/A'),
        'Total Assets': currency_format(data.get('total_assets')),
        'Total Liabilities': currency_format(data.get('total_liabilities')),
        'Shareholder Equity': currency_format(data.get('total_shareholder_equity')),
        'Current Assets': currency_format(data.get('current_assets')),
        'Current Liabilities': currency_format(data.get('current_liabilities')),
        'Cash': currency_format(data.get('cash')),
        'Total Debt': currency_format(data.get('total_debt'))
    }

def format_income_statement(data):
    return {
        'Fiscal Date': data.get('fiscal_date', 'N/A'),
        'Revenue': currency_format(data.get('revenue')),
        'Cost of Revenue': currency_format(data.get('cost_of_revenue')),
        'Gross Profit': currency_format(data.get('gross_profit')),
        'Operating Income': currency_format(data.get('operating_income')),
        'Net Income': currency_format(data.get('net_income')),
        'EBITDA': currency_format(data.get('ebitda'))
    }

def format_cash_flow(data):
    return {
        'Fiscal Date': data.get('fiscal_date', 'N/A'),
        'Operating Cash Flow': currency_format(data.get('operating_cashflow')),
        'Capital Expenditures': currency_format(data.get('capital_expenditures')),
        'Free Cash Flow': data.get('free_cash_flow', 'N/A'),
        'Dividend Payout': currency_format(data.get('dividend_payout'))
    }

def format_earnings(data):
    quarterly = []
    for q in data.get('quarterly_earnings', []):
        quarterly.append({
            'Date': q.get('date', 'N/A'),
            'Reported EPS': currency_format_decimal(q.get('reported_eps')),
            'Estimated EPS': currency_format_decimal(q.get('estimated_eps')),
            'Surprise': currency_format_decimal(q.get('surprise')),
            'Surprise %': rate_format(q.get('surprise_percentage'))
        })
    
    annual = []
    for a in data.get('annual_earnings', []):
        annual.append({
            'Year': a.get('year', 'N/A'),
            'Reported EPS': currency_format_decimal(a.get('reported_eps'))
        })
    
    upcoming = []
    for u in data.get('upcoming_earnings', []):
        upcoming.append({
            'Report Date': u.get('report_date', 'N/A'),
            'Fiscal Period End': u.get('fiscal_date_ending', 'N/A'),
            'EPS Estimate': currency_format_decimal(u.get('estimate'))
        })
    
    return {
        'Quarterly Earnings': quarterly,
        'Annual Earnings': annual,
        'Upcoming Earnings': upcoming
    }

def format_corporate_actions(data):
    dividends = []
    for d in data.get('dividends', []):
        dividends.append({
            'Ex-Date': d.get('ex_date', 'N/A'),
            'Payment Date': d.get('payment_date', 'N/A'),
            'Amount': currency_format_decimal(d.get('amount'))
        })
    
    return {
        'Dividends': dividends
    }

def format_all_data(ticker):
    input_file = Path('data') / f'{ticker}_extracted_data.json'
    
    if not input_file.exists():
        raise FileNotFoundError(f"Extracted data file not found: {input_file}")
    
    with open(input_file, 'r') as f:
        extracted_data = json.load(f)
    
    formatted = {
        'company_info': format_company_info(extracted_data['company_info']),
        'financial_metrics': format_financial_metrics(extracted_data['financial_metrics']),
        'valuation_metrics': format_valuation_metrics(extracted_data['valuation_metrics']),
        'profitability_metrics': format_profitability_metrics(extracted_data['profitability_metrics']),
        'per_share_metrics': format_per_share_metrics(extracted_data['per_share_metrics']),
        'balance_sheet': format_balance_sheet(extracted_data['balance_sheet']),
        'income_statement': format_income_statement(extracted_data['income_statement']),
        'cash_flow': format_cash_flow(extracted_data['cash_flow']),
        'earnings': format_earnings(extracted_data['earnings']),
        'corporate_actions': format_corporate_actions(extracted_data['corporate_actions'])
    }
    
    output_file = Path('data') / f'{ticker}_formatted_data.json'
    with open(output_file, 'w') as f:
        json.dump(formatted, f, indent=2)
    
    print(f"\n✓ Formatted data saved to {output_file}")
    return formatted

if __name__ == '__main__':
    ticker = input(f'\nEnter Symbol: ').upper() 
    format_all_data(ticker)




