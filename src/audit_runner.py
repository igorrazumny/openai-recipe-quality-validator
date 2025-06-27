# audit_runner.py
# This file orchestrates the process of running the audit pipeline.
# It handles entry slicing, model-based analysis, PDF generation, and output delivery.

from datetime import datetime
import json
import streamlit as st
from src.audit import analyze_recipe
from src.pdf_generator import generate_audit_report
from src.utils import estimate_cost
import pandas as pd
import io
import pytz
from collections import Counter

import logging
logging.basicConfig(level=logging.INFO)

severity_mapping = {
    # Critical issues
    "Missing Required Step": "Critical",
    "Grossly Incorrect Quantity": "Critical",
    "Conflicting Status Code": "Critical",
    "Negative Quantity": "Critical",
    "Data Conflict": "Critical",
    "Invalid Status": "Critical",
    "Step Contradicts Approved Recipe": "Critical",
    "Potential Falsification": "Critical",
    "Timestamp Sequence Error": "Critical",
    "Missing Mandatory Field": "Critical",
    # Moderate issues
    "Slightly Out of Range Quantity": "Moderate",
    "Incomplete Operator Name": "Moderate",
    "Non-Standard Timestamp": "Moderate",
    "Duplicate Record": "Moderate",
    "Use of Deprecated Process Code": "Moderate",
    "Inconsistent Sequencing": "Moderate",
    "Missing Recommended Field": "Moderate",
    "Format Error": "Moderate",
    "Value Out of Range": "Moderate",
    "Invalid Date Format": "Moderate",
    "Partial Data Entry": "Moderate",
    "Data Inconsistency": "Moderate",
    # Minor issues
    "Minor Formatting Error": "Minor",
    "Non-Critical Typo": "Minor",
    "Slight Naming Deviation": "Minor",
    "Extra Spaces": "Minor",
    "Alternative Terminology": "Minor",
    "Timestamps Missing Seconds": "Minor",
    "Inconsistent Casing": "Minor"
}


def run_audit(content_str, file_type, entry_limit, model, file_name, system_prompt, user_prompt):
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
            result_json = analyze_recipe(data, model, system_prompt, user_prompt)
            records = result_json.get("records", [])

        # Re-apply severity mapping for consistency
        for rec in records:
            deviations = rec.get("deviations", [])
            for dev in deviations:
                dev_type = dev.get("type", "").strip()
                if dev_type in severity_mapping:
                    dev["severity"] = severity_mapping[dev_type]

        # Compute compliance summary
        total_records = len(records)
        critical = 0
        moderate = 0
        minor = 0

        critical_types = Counter()
        moderate_types = Counter()

        records_with_deviations = 0
        records_with_multiple_deviations = 0

        for rec in records:
            deviations = rec.get("deviations", [])
            if deviations:
                records_with_deviations += 1
                if len(deviations) > 1:
                    records_with_multiple_deviations += 1
                for dev in deviations:
                    severity = dev.get("severity", "").lower()
                    dev_type = dev.get("type", "Unknown")
                    if severity == "critical":
                        critical += 1
                        critical_types[dev_type] += 1
                    elif severity == "moderate":
                        moderate += 1
                        moderate_types[dev_type] += 1
                    elif severity == "minor":
                        minor += 1

        records_fully_compliant = total_records - records_with_deviations
        compliance_rate = round((records_fully_compliant / total_records) * 100, 1)

        summary_stats = {
            "data_quality_score": result_json.get("data_quality_score", 5),
            "total_records": total_records,
            "total_entries_in_file": total_entries,
            "records_with_deviations": records_with_deviations,
            "records_with_multiple_deviations": records_with_multiple_deviations,
            "records_fully_compliant": records_fully_compliant,
            "compliance_rate": compliance_rate,
            "critical": critical,
            "moderate": moderate,
            "minor": minor,
            "critical_types": dict(critical_types),
            "moderate_types": dict(moderate_types)
        }

        # Step 4: Generate audit report PDF
        pdf_content = generate_audit_report(
            audit_results=result_json,  # ✅ Pass the full JSON including summary_text
            original_filename=file_name,
            file_contents=data,
            summary_stats=summary_stats
        )

        # Create a custom filename for the PDF
        timestamp = datetime.now(pytz.timezone("Europe/Zurich")).strftime("%Y-%m-%d %H:%M:%S %Z")
        safe_file_name = file_name.replace(" ", "_").replace(".json", "").replace(".csv", "")
        custom_filename = f"{timestamp}_{safe_file_name}_audit_report.pdf"

        # Step 5: Provide download link
        st.success("✅ Audit complete!")

        st.download_button(
            label="📄 Download Audit Report (PDF)",
            data=pdf_content,
            file_name=custom_filename,
            mime="application/pdf"
        )

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")