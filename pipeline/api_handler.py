from openai import OpenAI
from dotenv import load_dotenv
import os
from pipeline.utils import read_in_text, write_response_to_file
import time

def chat_completion(system_prompt, openai_key, file, model = "gpt-4o-mini", json_format = False):
    start_time = time.time()
    print("Chatting with model...")
    client = OpenAI(api_key=openai_key)
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
    end_time = time.time()
    elapsed_time_ms = (end_time - start_time) * 1000
    return response.content, elapsed_time_ms