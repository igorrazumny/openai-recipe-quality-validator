# app.py
# This is the main entry point for the Streamlit application that runs the Healthcare Recipe Quality Validator.

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import logging
import hashlib

logging.basicConfig(level=logging.INFO)

import config
import streamlit as st
from src.controls import display_controls
from src.audit_runner import run_audit
from src.layout import render_layout
from src.utils import detect_file_type
from datetime import datetime

# Set Streamlit page config
st.set_page_config(
    page_title="Healthcare Recipe Quality Validator",
    layout="wide",
    page_icon="🧪",
)

# Display app layout (header, file upload, etc.)
render_layout()

# Show controls and get user input
uploaded_file, num_entries, model, system_prompt, user_prompt = display_controls()

# Initialize session state variables
if "audit_done" not in st.session_state:
    st.session_state.audit_done = False
    st.session_state.audit_result = None
if "audit_running" not in st.session_state:
    st.session_state.audit_running = False
if "last_uploaded_file_hash" not in st.session_state:
    st.session_state.last_uploaded_file_hash = None

# 🟢 Clear results if a new file was selected or re-selected
if uploaded_file:
    file_bytes = uploaded_file.read()
    uploaded_file.seek(0)
    file_hash = hashlib.md5(file_bytes).hexdigest()

    if st.session_state.last_uploaded_file_hash != file_hash:
        # New file or re-upload detected
        st.session_state.audit_done = False
        st.session_state.audit_result = None
        st.session_state.audit_running = False
        st.session_state.last_uploaded_file_hash = file_hash

# Display Run Audit button if file is uploaded
if uploaded_file:
    if st.button("Run Audit"):
        # 🟢 Clear previous results and set running flag
        st.session_state.audit_done = False
        st.session_state.audit_result = None
        st.session_state.audit_running = True

        try:
            # Detect file type
            file_type = detect_file_type(uploaded_file.name)
            logging.info(f"File type: {file_type}")

            # Re-read bytes to get content
            file_bytes = uploaded_file.read()
            uploaded_file.seek(0)

            if b'\x00' in file_bytes:
                st.session_state.audit_running = False
                st.error("❌ The uploaded file contains binary data or embedded null bytes. Please upload a clean UTF-8 text file.")
                st.stop()

            try:
                content_str = file_bytes.decode("utf-8")
            except UnicodeDecodeError as e:
                st.session_state.audit_running = False
                logging.error(f"Unicode decode error: {e}")
                st.error("❌ The uploaded file is not valid UTF-8 text. Please re-save it as UTF-8 encoding and try again.")
                st.stop()

            # Run audit
            result = run_audit(
                content_str=content_str,
                file_type=file_type,
                entry_limit=num_entries,
                model=model,
                file_name=uploaded_file.name,
                system_prompt=system_prompt,
                user_prompt=user_prompt
            )

            # Save results
            st.session_state.audit_result = result
            st.session_state.audit_done = True
            st.session_state.audit_running = False

        except Exception as e:
            st.session_state.audit_running = False
            st.error(f"An error occurred while processing the file: {e}")

# 🟢 Show spinner while running
if st.session_state.audit_running:
    st.info("🔄 Running audit with OpenAI... Please wait...")

# 🟢 Show results when done
elif st.session_state.audit_done and st.session_state.audit_result:
    st.success("✅ Audit complete!")

    st.download_button(
        label="📄 Download Audit Report (PDF)",
        data=st.session_state.audit_result["pdf_content"],
        file_name=st.session_state.audit_result["custom_filename"],
        mime="application/pdf"
    )

    stats = st.session_state.audit_result["summary_stats"]
    st.write("**Compliance Rate:**", stats["compliance_rate"])
    st.write("**Critical Deviations:**", stats["critical"])
    st.write("**Moderate Deviations:**", stats["moderate"])
    st.write("**Minor Deviations:**", stats["minor"])