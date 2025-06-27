# audit_runner.py
# This file orchestrates the process of running the audit pipeline.
# It handles entry slicing, model-based analysis, PDF generation, and output delivery.

from datetime import datetime
import json
import streamlit as st
from src.audit import analyze_recipe
from src.pdf_generator import generate_audit_report
from src.utils import estimate_cost, extract_file_metadata
import pandas as pd
import io
import pytz

import logging
logging.basicConfig(level=logging.INFO)

def run_audit(content_str, file_type, entry_limit, model, file_name, prompt):
    try:
        # Step 1: Parse file content into a list of records
        if file_type == "json":
            data = json.loads(content_str)
        else:
            df = pd.read_csv(io.StringIO(content_str))
            data = df.to_dict(orient="records")

        total_entries = len(data)

        # Step 2: Estimate cost and confirm for full file
        if entry_limit == "full":
            estimated_cost = estimate_cost(total_entries)
            user_confirmed = st.radio(
                f"Estimated cost: ${estimated_cost:.2f} USD. Please use discretion when running large audits or testing at scale. Though no costs will be charged to you, the cost of this run will be covered from the personal funds of the developer: [GitHub](https://github.com/igorrazumny). Proceed?",
                ["Yes", "No"],
                index=1
            )
            if user_confirmed != "Yes":
                st.warning("Audit canceled.")
                return
        else:
            entry_count = int(str(entry_limit).split(" ")[0])
            data = data[:entry_count]

        # Step 3: Perform analysis
        with st.spinner("Running audit with OpenAI..."):
            report_text = analyze_recipe(data, model, prompt)

    

        # Step 4: Generate audit report PDF
        pdf_content = generate_audit_report(
            report_text,
            file_name,
            data
        )

        # Create a custom filename for the PDF
        timestamp = datetime.now(pytz.timezone("Europe/Zurich")).strftime("%Y-%m-%d %H:%M:%S %Z")
        safe_file_name = file_name.replace(" ", "_").replace(".json", "").replace(".csv", "")
        custom_filename = f"{timestamp}_{safe_file_name}_audit_report.pdf"

        # Step 5: Provide download link
        st.success("✅ Audit complete!")
        
        # logging.info(f"pdf_content = {pdf_content} (type: {type(pdf_content)})")
        
        # with open(pdf_content, "rb") as f:
        #     pdf_bytes = f.read()

        # Debugging
        logging.info("\n" * 10)
        logging.info("Here")
            
        st.download_button(
            label="📄 Download Audit Report (PDF)",
            data=pdf_content,
            file_name=custom_filename,
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")