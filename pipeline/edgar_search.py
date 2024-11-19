import os
from edgar import *
import argparse
import requests
from edgar.financials import Financials
import pandas as pd
import warnings
from utils import write_to_markdown, write_to_csv
warnings.filterwarnings("ignore", category=FutureWarning)

# python edgar-extract-data.py cik --format markdown



def fetch_company_sheets(filing):
    # another way to get balance sheet
    # tenk = Company("AAPL").get_filings(form="10-K").latest(1).obj()
    financials = Financials(filing.xbrl())
    balance_sheet_df = financials.get_balance_sheet().get_dataframe().reset_index()
    income_statement_df = financials.get_income_statement().get_dataframe().reset_index()
    cash_flow_df = financials.get_cash_flow_statement().get_dataframe().reset_index()
    return balance_sheet_df, income_statement_df, cash_flow_df


# sample use: filing = edgarTool_get_filing(company_cik, "10-K", 1)
def edgarTool_get_filing(ticker, form_type="10-K", num_filings=1):
    # Get the latest 10-K filing for Apple
    filing = Company(ticker).get_filings(form=form_type).latest(num_filings)
    return filing



def main():
    parser = argparse.ArgumentParser(description="Fetch and save company data by CIK")
    parser.add_argument('cik', type=str, help="The CIK of the company to fetch data for")
    # parser.add_argument('-o', '--output', type=str, help="Output file path")
    parser.add_argument('-f', '--format', type=str, choices=['csv', 'markdown'], default='markdown',
                        help="Output format: 'csv' or 'markdown' (default: markdown txt).")
    
    

    
    args = parser.parse_args()
    cik = args.cik
    format = args.format
    # output = args.output

    print(f"Fetching data for CIK: {cik}")

    # Set the identity for the edgartool
    set_identity("lingruiz@andrew.cmu.edu")

    filing = edgarTool_get_filing(cik)
    sheets = fetch_company_sheets(filing)
    
    if sheets:
        # Write data to the selected format
        if format == 'csv':
            write_to_csv(sheets, cik)
        elif format == 'markdown':
            write_to_markdown(sheets, cik)
    else:
        print(f"No data found for CIK: {cik}")

    print(f"Data saved in {format} format for CIK: {cik}")

if __name__ == '__main__':
    main()