import yaml
import os
import pandas as pd

def load_config(config_path="pipeline/config.yml"):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config

def dataframe_to_markdown(df: pd.DataFrame) -> str:
    # Create the header row
    header = "| " + " | ".join(df.columns) + " |\n"
    separator = "| " + " | ".join(["---"] * len(df.columns)) + " |\n"
    
    # Create the data rows
    rows = ""
    for _, row in df.iterrows():
        row_text = "| " + " | ".join(map(str, row)) + " |\n"
        rows += row_text
    
    return header + separator + rows

def write_to_markdown(data, company_cik, output_dir):
    path = os.path.join(output_dir, "markdown_data")
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path,f'{company_cik}_sheet.txt'), 'w') as file:
        file.write("\n balance sheet \n")
        file.write(dataframe_to_markdown(data[0]))
        file.write("\n income statement \n")
        file.write(dataframe_to_markdown(data[1]))
        file.write("\n cash flow statment \n")
        file.write(dataframe_to_markdown(data[2]))
        file.close()
    with open(os.path.join(path,f'{company_cik}_sheet.txt'), 'r') as file:
        content = file.read()
        file.close()
    return content

def write_to_csv(data, company_cik, output_dir):
    path = os.path.join(output_dir, "csv_data")
    os.makedirs(path, exist_ok=True)
    data[0].to_csv(os.path.join(path, f'{company_cik}_balance_sheet.csv'), index=False)
    data[1].to_csv(os.path.join(path, f'{company_cik}_income_statement.csv'), index=False)
    data[2].to_csv(os.path.join(path, f'{company_cik}_cash_flow.csv'), index=False)


def read_in_text(filename):
    with open(filename, 'r') as file:
        text = file.read()
        file.close()
    return text


def write_response_to_file(response, system_prompt, filename, output_dir, filetype="txt"):
    path = os.path.join(output_dir, system_prompt)
    os.makedirs(path, exist_ok=True)
    with open(f'{path}/{filename}.{filetype}', 'w') as f:
        f.write(response)
        f.close()
    print(f"Response saved to {filename}.{filetype}")