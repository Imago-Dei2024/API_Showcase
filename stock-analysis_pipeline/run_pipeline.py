# ==================================================================================================================== # 
# Pipeline Orchestrator: Master script that runs the complete data pipeline in order - 
# fetches data, extracts metrics, formats values, and prepares data for dashboard display 
# ==================================================================================================================== # 

import sys 
from pathlib import Path 

# Import all Modules 
import data_fetcher as step1 
import data_extractor as step2 
import data_formatter as step3 


def run_full_pipeline(ticker): 
    """ 
    Runs the complete data pipeline: 
    1. Fetch data from Alpha Vantage API 
    2. Extract key metrics 
    3. Format numerical values 
    """ 

    print('='*70) 
    print(f"   STOCK FUNDAMENTAL ANALYSIS PIPELINE") 
    print(f"   Ticker: {ticker}") 
    print(f'='*70) 

    try: 
        print("STEP 1: Fetching data from Alpha Vantage API...") 
        print('-'*70) 
        step1.fetch_all_data(ticker) 
        print(f'\n√ Step 1 Complete\n') 

        print("STEP 2: Extracting Key Metrics...") 
        print('-'*70) 
        step2.extract_all_data(ticker) 
        print('\n√ Step 2 Complete\n') 

        print("STEP 3: Formatting numerical values...") 
        print('-'*70) 
        step3.format_all_data(ticker) 
        print('\n√ Step 3 Complete \n') 

        print(f'-'*70)  
        print(f'✅ Pipeline Complete for {ticker}!') 
        print(f'-'*70)  
        print('Next Steps:') 
        print(' -> View data: streamlit run 4_streamlit_app.py') 
        print(f'-> Data files saved in: ./data/{ticker}_*.json\n') 

        return True 
    
    except Exception as e: 
        print(f'\n❌ Error in pipeline: {str(e)}') 
        return False 
    

if __name__ == '__main__': 
    if len(sys.argv) > 1: 
        ticker = sys.argv[1].upper() 
    else: 
        ticker = input("Enter Symbol: ").upper() 

    run_full_pipeline(ticker)