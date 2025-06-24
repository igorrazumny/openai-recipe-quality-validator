# layout.py
# This file manages the layout and display elements of the Streamlit app
# including the project overview and file download section.

import streamlit as st
from pathlib import Path

def render_layout():
    st.title("📋 OpenAI Healthcare Recipe Quality Validator")

    st.markdown("""
    This application audits healthcare manufacturing recipes using an advanced AI model (OpenAI GPT-4o).
    After analyzing the uploaded recipe, it generates an evaluation report available for download in PDF format.
    """)

    # st.markdown("""
    # ---  
    # ### 🧪 Try it out with test data:
    # The test files below contain intentionally introduced data quality problems. You can download them and re-upload below
    # to see how the audit works. Both files contain the same data, just in different formats.
    # """)

    # # File paths
    # json_path = Path("public_assets/test_data.json")
    # csv_path = Path("public_assets/test_data.csv")
    # pdf_path = Path("public_assets/recipe_quality_validation_report.pdf")

    # # Read file contents
    # json_bytes = json_path.read_bytes()
    # csv_bytes = csv_path.read_bytes()
    # pdf_bytes = pdf_path.read_bytes()

    # st.markdown("*Clicking a button will download the file. You’ll need to upload it using the selector below to run the audit.*")

    # # Download buttons
    # st.download_button(
    #     label="📥 Download test_data.json",
    #     data=json_bytes,
    #     file_name="test_data.json",
    #     mime="application/json"
    # )

    # st.download_button(
    #     label="📥 Download test_data.csv",
    #     data=csv_bytes,
    #     file_name="test_data.csv",
    #     mime="text/csv"
    # )

    # st.download_button(
    #     label="📄 View list of intentionally introduced deviations (PDF)",
    #     data=pdf_bytes,
    #     file_name="recipe_quality_validation_report.pdf",
    #     mime="application/pdf"
    # )

    # st.markdown("---")