import os
from edgar import *
import argparse
import requests
import time
from edgar.financials import Financials
import pandas as pd
import warnings
import pipeline.utils as utils
from pipeline.edgar_search import fetch_company_sheets, edgarTool_get_filing, set_user_identity
from pipeline.api_handler import chat_completion
warnings.filterwarnings("ignore", category=FutureWarning)




def main():
    start_time = time.time()
    parser = argparse.ArgumentParser(description="Fetch and save company data by CIK")
    parser.add_argument('cik', type=str, help="The CIK of the company to fetch data for")
    parser.add_argument('-o', '--output', type=str, help="Output file path")
    

    
    args = parser.parse_args()
    cik = args.cik
    output = args.output

    extract_prompt = utils.read_in_text("pipeline/prompts/extract_prompt.txt")
    calculate_prompt = utils.read_in_text("pipeline/prompts/calculate_prompt.txt")
    assess_prompt = utils.read_in_text("pipeline/prompts/assess_prompt.txt")
    review_prompt = utils.read_in_text("pipeline/prompts/review_prompt.txt")

    if not output:
        output = os.getcwd()
    

    # os.chdir(output)
    output_dir = os.path.join(output, f"{cik}_credit_analysis")

    os.makedirs(output_dir, exist_ok=True)

    print(f"Fetching data for CIK: {cik}")

    config = utils.load_config() 
    openai_api_key = config["openai"]["api_key"]
    credential_email = config["edgar"]["email"]
    model = "gpt-4o-mini"

    # Set the identity for the edgartool
    set_user_identity(credential_email)

    filing = edgarTool_get_filing(cik)
    sheets = fetch_company_sheets(filing)
    
    if sheets:
        # Write data to the selected format
        utils.write_to_csv(sheets, cik, output_dir)
        content_file = utils.write_to_markdown(sheets, cik, output_dir)
    else:
        print(f"No data found for CIK: {cik}")
        exit()
    



    print(f"Data saved for CIK: {cik}")

    # Chat with the model
    print("Performing Extraction Step")
    extract_response, _ = chat_completion(extract_prompt, openai_api_key, content_file, model, True)
    utils.write_response_to_file(extract_response, 'extract', "financial_data", output_dir, "json")

    print("Performing Calculation Step")
    calculation_response, _ = chat_completion(calculate_prompt, openai_api_key, extract_response, model)
    utils.write_response_to_file(calculation_response, 'calculation', "calculations", output_dir)

    print("Performing Assessment Step")
    assessment_response, _ = chat_completion(assess_prompt, openai_api_key, calculation_response, model)
    utils.write_response_to_file(assessment_response, 'assessment', "assessment", output_dir)

    print("Performing Review Step")
    review_response, _ = chat_completion(review_prompt, openai_api_key, assessment_response, model)
    utils.write_response_to_file(review_response, 'assessment', "final_assessment", output_dir)
    print(review_response)

    end_time = time.time()
    full_time_taken = (end_time - start_time)

    print(f"Time taken for the analysis: {full_time_taken:.2f} seconds")

    



if __name__ == '__main__':
    main()