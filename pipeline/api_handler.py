from openai import OpenAI
from dotenv import load_dotenv
import os


def chat_completion(openai_key, model, system_prompt, file, json_format=False):
    client = OpenAI()
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
