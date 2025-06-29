# audit.py
# This module sends the recipe data to OpenAI's LLM and retrieves the validation response.
# It builds a prompt based on the recipe content and selected model.

import os
import json
import re
from pyexpat.errors import messages
from typing import Any

from openai import OpenAI
from dotenv import load_dotenv
import logging
import config
# logging.basicConfig(level=logging.INFO)

load_dotenv()

client = OpenAI(api_key=config.OPENAI_API_KEY)

def analyze_recipe(recipe_entries, model="gpt-4o", system_prompt="", user_prompt=""):
    # logging.info(f"Prompt: {system_prompt}")
    # logging.info(f"Prompt: {user_prompt}")

    MAX_ENTRIES = 1000

    if len(recipe_entries) > MAX_ENTRIES:
        truncated = recipe_entries[:MAX_ENTRIES]
        logging.warning(f"Truncated to first {MAX_ENTRIES} entries to stay within context limits.")
    else:
        truncated = recipe_entries

    # ✅ Canonicalize JSON input: always same ordering of keys
    full_prompt = (
        f"{user_prompt}\n\n"
        "Recipe data:\n"
        f"{json.dumps(truncated, indent=2, sort_keys=True)}"
    )

    messages: list[dict[str, Any]] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": full_prompt}
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages, # type: ignore[arg-type]
        temperature=0,
        top_p=1
    )

    content = response.choices[0].message.content.strip()

    # First try direct JSON parsing
    try:
        parsed = json.loads(content)
        logging.info("Successfully parsed model response JSON.")
        if "summary_text" not in parsed:
            parsed["summary_text"] = ""
        return parsed
    except json.JSONDecodeError:
        logging.warning("Direct JSON parsing failed. Attempting to extract JSON substring.")

        # Try to extract JSON between the first and last curly braces
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                parsed = json.loads(json_str)
                logging.info("Successfully parsed JSON extracted from text.")
                if "summary_text" not in parsed:
                    parsed["summary_text"] = ""
                if "data_quality_score" not in parsed:
                    parsed["data_quality_score"] = 5  # default if missing
                return parsed
            except json.JSONDecodeError as e2:
                logging.error(f"JSON decode error after extraction: {e2}")
        
        # If all fails
        logging.error(f"Failed to parse JSON output from the model. Raw content:\n{content}")
        raise ValueError(
            "Failed to parse JSON output from the model. "
            "See logs for raw content."
        )