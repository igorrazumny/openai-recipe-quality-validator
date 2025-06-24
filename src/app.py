# app.py
# This is the main entry point for the Streamlit application that runs the Healthcare Recipe Quality Validator.
# It handles file uploads, user selections, and triggers the audit process.

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
logging.basicConfig(level=logging.INFO)

import streamlit as st
import json
import pandas as pd
from src.controls import display_controls
from src.audit_runner import run_audit
from src.layout import render_layout
from src.utils import extract_file_content, detect_file_type
from datetime import datetime

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s — %(levelname)s — %(message)s",
#     datefmt="%Y-%m-%d %H:%M:%S"
# )

logging.info("\n" * 100)
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.info(f"{now} New audit execution started")


# Set Streamlit page config
st.set_page_config(
    page_title="Healthcare Recipe Quality Validator",
    layout="centered",
    page_icon="🧪",
)

# Display app layout (header, file upload, links, etc.)
render_layout()

# Show controls and get user input
uploaded_file, num_entries, model = display_controls()

logging.info(f"Number of entries: {num_entries}, Model: {model}")

# If everything is provided, start processing
if uploaded_file and num_entries and model:
    try:
        # Determine the file type
        file_type = detect_file_type(uploaded_file.name)

        logging.info(f"File type: {file_type}")

        # Read uploaded file as string
        content_bytes = uploaded_file.read()
        logging.info(f"File type: {uploaded_file.name}")

        content_str = content_bytes.decode("utf-8")

        # Run audit
        run_audit(
            content_str=content_str,
            file_type=file_type,
            entry_limit=num_entries,
            model=model,
            file_name=uploaded_file.name
        )

    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")