# audit.py
# This module sends the recipe data to OpenAI's LLM and retrieves the validation response.
# It builds a prompt based on the recipe content and selected model.

import os
import json
from openai import OpenAI 
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_recipe(recipe_entries, model="gpt-4o", prompt=""):
    # prompt = (
    #     "You are an expert in healthcare manufacturing data quality control."
    #     " Analyze the following recipe data for potential issues such as missing values,"
    #     " inconsistent entries, or non-standardized formatting."
    #     " Provide a clear, structured report with explanations."
    #     "\n\n"
    #     f"Recipe data:\n{json.dumps(recipe_entries, indent=2)}"
    # )

    MAX_ENTRIES = 1000

    if len(recipe_entries) > MAX_ENTRIES:
        truncated = recipe_entries[:MAX_ENTRIES]
        logging.warning(f"Truncated to first {MAX_ENTRIES} entries to stay within context limits.")
    else:
        truncated = recipe_entries

    full_prompt = (
        f"{prompt}\n\n"
        "Recipe data:\n"
        f"{json.dumps(truncated, indent=2)}"
    )


    response = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are a healthcare recipe quality validation assistant."},
        {"role": "user", "content": full_prompt}
    ],
    temperature=0.2
)


    return response.choices[0].message.content