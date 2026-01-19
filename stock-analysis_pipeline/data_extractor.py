# ==================================================================================================================== # 
# Data Extractor: Extracts key metrics from raw API data including company info, financial metrics 
# (market cap, revenue, debt), valuation ratios (P/E, PEG), profitability metrics, and earnings data 
# ==================================================================================================================== #  

import json 
from pathlib import Path 

def extract_company_info(overview): 
    return { 
        'name': overview.get('Name', 'N/A'), 
        'symbol': overview.get('Symbol', 'N/A'), 
        'exchange': overview.get('Exchange', 'N/A'), 
        'sector': overview.get('Sector', 'N/A'), 
        'industry': overview.get('Industry', 'N/A'), 
        'description': overview.get('Description', 'N/A')
    } 

def extract_financial_metrics(overview): 
    return { 
        'market_cap': overview.get('MarketCapitalization', 'N/A'), 
        'revenue_ttm': overview.get('RevenueTTM', 'N/A'), 
        'gross_profit_ttm': overview.get('GrossProfitTTM', 'N/A'), 
        'ebitda': overview.get('EBITDA', 'N/A'), 
        'profit_margin': overview.get('ProfitMargin', 'N/A') 
    } 

def extract_valuation_metrics(overview): 
    return { 
        'pe_ratio': overview.get('PERatio', 'N/A'), 
        'peg_ratio': overview.get('PEGRatio', 'N/A'), 
        'price_to_book': overview.get('PriceToBookRatio', 'N/A'), 
        'price_to_sales': overview.get('PriceToSalesRatioTTM', 'N/A'), 
        'ev_to_revenue': overview.get('EVToRevenue', 'N/A'), 
        'ev_to_ebitda': overview.get('EVToEBITDA', 'N/A')
        
    } 

def extract_profitability_metrics(overview): 
    return { 
        'profit_margin': overview.get('ProfitMargin', 'N/A'), 
        'operating_margin': overview.get('OperatingMarginTTM', 'N/A'), 
        'return_on_assets': overview.get('ReturnOnAssetsTTM', 'N/A'), 
        'return_on_equity': overview.get('ReturnOnEquityTTM', 'N/A')
    } 

def extract_per_share_metrics(overview): 
    return { 
        'eps': overview.get('EPS', 'N/A'), 
        'diluted_eps': overview.get('DilutedEPSTTM', 'N/A'), 
        'book_value': overview.get('BookValue', 'N/A'), 
        'dividend_per_share': overview.get('DividendPerShare', 'N/A'), 
        'dividend_yield': overview.get('DividendYield', 'N/A')
    } 

def extract_balance_sheet(balance_sheet): 
    if 'annualReports' not in balance_sheet or not balance_sheet['annualReports']: 
        return {}  
    
    latest = balance_sheet['annualReports'][0] 
    return { 
        'fiscal_date': latest.get('fiscalDateEnding', 'N/A'), 
        'total_assets': latest.get('totalAssets', 'N/A'), 
        'total_liabilities': latest.get('totalLiabilities', 'N/A'), 
        'total_shareholder_equity': latest.get('totalShareholderEquity', 'N/A'), 
        'current_assets': latest.get('totalCurrentAssets', 'N/A'), 
        'current_liabilities': latest.get('totalCurrentLiabilities', 'N/A'), 
        'cash': latest.get('cashAndCashEquivalentsAtCarryingValue', 'N/A'), 
        'total_debt': latest.get('shortLongTermDebtTotal', 'N/A') 
    } 

def extract_income_data(income_statement): 
    if 'annualReports' not in income_statement or not income_statement['annualReports']: 
        return {} 
    
    latest = income_statement['annualReports'][0] 
    return {
        'fiscal_date': latest.get('fiscalDateEnding', 'N/A'), 
        'revenue': latest.get('totalRevenue', 'N/A'), 
        'cost_of_revenue': latest.get('costOfRevenue', 'N/A'), 
        'gross_profit': latest.get('grossProfit'), 
        'operating_income': latest.get('operatingIncome', 'N/A'), 
        'net_income': latest.get('netIncome', 'N/A'), 
        'ebitda': latest.get('ebitda', 'N/A')
    } 

def extract_cash_flow_data(cash_flows): 
    if 'annualReports' not in cash_flows or not cash_flows['annualReports']: 
        return {} 
    
    latest = cash_flows['annualReports'][0] 
    return { 
        'fiscal_date': latest.get('fiscalDateEnding', 'N/A'), 
        'operating_cashflow': latest.get('operatingCashflow', 'N/A'), 
        'capital_expenditures': latest.get('capitalExpenditures', 'N/A'), 
        'free_cash_flow': latest.get('free_cash_flow', 'N/A'), 
        'dividend_payout': latest.get('dividendPayout', 'N/A')
    } 

def extract_earnings_data(earnings_history, earnings_calendar): 
    quarterly = [] 
    annual = [] 
    upcoming = [] 

    # Extract Historical Quarterly Earnings 
    if 'quarterlyEarnings' in earnings_history:  
        # [:4] --> shows the most recent 4 quarters
        for q in earnings_history['quarterlyEarnings'][:4]: 
            quarterly.append({ 
                'date': q.get('fiscalDateEnding', 'N/A'), 
                'reported_eps': q.get('reportedEPS', 'N/A'), 
                'estimated_eps': q.get('estimatedEPS', 'N/A'), 
                'surprise': q.get('surprise', 'N/A'), 
                'surprise_percentage': q.get('surprisePercentage'), 
               # Add Report Time once done 
            })  
            
    # Extract Annual Earnings  
    if 'annualEarnings' in earnings_history: 
        for a in earnings_history['annualEarnings'][:3]: 
            annual.append({ 
                'year': a.get('fiscalDateEnding', 'N/A'), 
                'reported_eps': a.get('reportedEPS', 'N/A')
            }) 

    # Extract Upcoming Earnings From Calendar (First 5 upcoming dates) 
    if earnings_calendar and isinstance(earnings_calendar, list): 
        for e in earnings_calendar[:5]: 
            upcoming.append({ 
                'report_date': e.get('reportDate', 'N/A'), 
                'fiscal_date_ending': e.get('fiscalDateEnding', 'N/A'), 
                'estimate': e.get('estimate', 'N/A')
            }) 
    
    return { 
        'quarterly_earnings': quarterly, 
        'annual_earnings': annual, 
        'upcoming_earnings': upcoming 
    } 

def extract_corporate_actions(dividends): 
    dividend_list = [] 

    if 'data' in dividends: 
        for d in dividends['data'][:10]: 
            dividend_list.append({ 
                'ex_date': d.get('ex_dividend_date', 'N/A'), 
                'payment_date': d.get('payment_date', 'N/A'), 
                'amount': d.get('amount', 'N/A') 
            }) 
    
    return { 
        'dividends': dividend_list 
    } 

def extract_all_data(ticker):  
    data_file = Path('data') / f'{ticker}_raw_data.json' 

    if not data_file.exists(): 
        raise FileNotFoundError(f'Data file not found: {data_file}') 
    
    with open(data_file, 'r') as f: 
        raw_data = json.load(f) 

    extracted = { 
        'company_info': extract_company_info(raw_data['overview']), 
        'financial_metrics': extract_financial_metrics(raw_data['overview']), 
        'valuation_metrics': extract_valuation_metrics(raw_data['overview']), 
        'profitability_metrics': extract_profitability_metrics(raw_data['overview']), 
        'per_share_metrics': extract_per_share_metrics(raw_data['overview']), 

        'balance_sheet': extract_balance_sheet(raw_data['balance_sheet']), 
        'income_statement': extract_income_data(raw_data['income_statement']), 
        'cash_flow': extract_cash_flow_data(raw_data['cash_flows']), 
        'earnings': extract_earnings_data(raw_data['earnings_history'], raw_data['earnings_calendar']), 
        'corporate_actions': extract_corporate_actions(raw_data['dividends']) 
    } 

    output_file = Path('data')/f'{ticker}_extracted_data.json' 
    with open(output_file, 'w') as f: 
        json.dump(extracted, f, indent=2) 

    print(f'\n√ Extracted data saved to {output_file}') 
    return extracted 

if __name__ == '__main__': 
    ticker = input(f'\nEnter Symbol: ').upper() 
    extract_all_data(ticker)