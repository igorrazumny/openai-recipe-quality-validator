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
import logging

logging.basicConfig(level=logging.INFO)

def run_audit(content_str, file_type, entry_limit, model, file_name):
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
            data = data[:int(entry_limit)]

        # Step 3: Perform analysis
        with st.spinner("Running audit with OpenAI..."):
            report_text = analyze_recipe(data, model)

        # Debugging
        logging.info("\n" * 10)
        lines = report_text.splitlines()
        preview = "\n".join(lines[:5])
        logging.info(f"Report text preview in audit_runner.py:\n{preview}")


        # Step 4: Generate audit report PDF
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        pdf_file_path = generate_audit_report(
            report_text,
            file_name,
            data
        )


        # Step 5: Provide download link
        st.success("✅ Audit complete!")
        st.download_button(
            label="📄 Download Audit Report (PDF)",
            data=pdf_file_path,
            file_name=f"{datetime.now().strftime("%Y-%m-%d")}_recipe_audit_report.pdf",
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")