from flask import Flask, request, render_template, redirect, url_for
import os
import time
import pipeline.utils as utils
from pipeline.edgar_search import fetch_company_sheets, edgarTool_get_filing, set_user_identity
from pipeline.api_handler import chat_completion
import markdown

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    cik = request.form['cik']
    output = request.form['output']

    extract_prompt = utils.read_in_text("pipeline/prompts/extract_prompt.txt")
    calculate_prompt = utils.read_in_text("pipeline/prompts/calculate_prompt.txt")
    assess_prompt = utils.read_in_text("pipeline/prompts/assess_prompt.txt")
    review_prompt = utils.read_in_text("pipeline/prompts/review_prompt.txt")

    if not output:
        output = os.getcwd()

    output_dir = os.path.join(output, f"{cik}_credit_analysis")
    os.makedirs(output_dir, exist_ok=True)

    config = utils.load_config()
    openai_api_key = config["openai"]["api_key"]
    credential_email = config["edgar"]["email"]
    model = "gpt-4o-mini"

    set_user_identity(credential_email)
    filing = edgarTool_get_filing(cik)
    sheets = fetch_company_sheets(filing)

    if sheets:
        utils.write_to_csv(sheets, cik, output_dir)
        content_file = utils.write_to_markdown(sheets, cik, output_dir)
    else:
        return "No data found for CIK: {}".format(cik)

    extract_response, _ = chat_completion(extract_prompt, openai_api_key, content_file, model, True)
    utils.write_response_to_file(extract_response, 'extract', "financial_data", output_dir, "json")

    calculation_response, _ = chat_completion(calculate_prompt, openai_api_key, extract_response, model)
    utils.write_response_to_file(calculation_response, 'calculation', "calculations", output_dir)

    assessment_response, _ = chat_completion(assess_prompt, openai_api_key, calculation_response, model)
    utils.write_response_to_file(assessment_response, 'assessment', "assessment", output_dir)

    review_response, _ = chat_completion(review_prompt, openai_api_key, assessment_response, model)
    utils.write_response_to_file(review_response, 'assessment', "crosscheck_assessment", output_dir)

    # Convert Markdown to HTML
    html_content = markdown.markdown(assessment_response)
    return render_template('result.html', result=html_content)

    # return render_template('result.html', result=assessment_response)

if __name__ == '__main__':
    app.run(debug=True)