from openai import OpenAI
from dotenv import load_dotenv
import os
from utils import read_in_text, write_response_to_file
import time

def chat_completion(openai_key, model, system_prompt, file, json_format=False):
    client = OpenAI(openai_key)
    if json_format:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": file
                }
            ],
            response_format={"type": "json_object"}
        )
    else:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": file
                }
            ]
        )
    response = completion.choices[0].message
    return response

def chat_with_model(system_prompt, openai_key, model = "gpt-4o-mini"):

    system_prompt = read_in_text('prompts/{system_prompt}_prompt.txt')
    content_file = read_in_text("markdown_data/NWBI_sheet.txt")

    start_time = time.time()
    print("Analyzing...")
    response = chat_completion(openai_key, model, system_prompt, content_file, True)
    end_time = time.time()
    # Calculate the elapsed time in milliseconds
    elapsed_time_ms = (end_time - start_time) * 1000
    
    # Log the elapsed time
    print(f"Time taken for chat_completion: {elapsed_time_ms:.2f} ms")

    write_response_to_file(response, 'extract', "financial_data.txt")
