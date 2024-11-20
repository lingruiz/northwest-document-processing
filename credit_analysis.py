import os
from edgar import *
import argparse
import requests
from edgar.financials import Financials
import pandas as pd
import warnings
import pipeline.utils as utils
from pipeline.edgar_search import fetch_company_sheets, edgarTool_get_filing, set_identity
from pipeline.api_handler import chat_completion, chat_with_model
warnings.filterwarnings("ignore", category=FutureWarning)




def main():
    parser = argparse.ArgumentParser(description="Fetch and save company data by CIK")
    parser.add_argument('cik', type=str, help="The CIK of the company to fetch data for")
    parser.add_argument('-o', '--output', type=str, help="Output file path")
    parser.add_argument('-f', '--format', type=str, choices=['csv', 'markdown'], default='markdown',
                        help="Output format: 'csv' or 'markdown' (default: markdown txt).")
    
    

    
    args = parser.parse_args()
    cik = args.cik
    output = args.output
    extract_prompt = utils.read_in_text("prompts/extract_prompt.txt")
    calculate_prompt = utils.ead_in_text("prompts/calculate_prompt.txt")
    assess_prompt = utils.read_in_text("prompts/assess_prompt.txt")


    os.chdir(output)

    

    print(f"Fetching data for CIK: {cik}")

    config = utils.load_config() 
    openai_api_key = config["openai"]["api_key"]
    credential_email = config["edgar"]["email"]
    model = "gpt-4o-mini"

    # Set the identity for the edgartool
    set_identity(credential_email)

    filing = edgarTool_get_filing(cik)
    sheets = fetch_company_sheets(filing)
    
    if sheets:
        # Write data to the selected format
        utils.write_to_csv(sheets, cik)
        utils.write_to_markdown(sheets, cik)
    else:
        print(f"No data found for CIK: {cik}")
        exit()
    



    print(f"Data saved in {format} format for CIK: {cik}")

    # Chat with the model
    chat_with_model(extract_prompt, openai_api_key, model)
    



if __name__ == '__main__':
    main()