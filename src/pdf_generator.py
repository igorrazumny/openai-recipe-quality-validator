# pdf_generator.py
# Generates the final audit report as a downloadable PDF with appendix.

from fpdf import FPDF
from datetime import datetime
import pytz
import json

import logging
logging.basicConfig(level=logging.INFO)

def generate_audit_report(audit_results: str, original_filename: str, file_contents: str) -> bytes:
    """
    Generates a PDF report from the audit results, timestamp, and original file content.
    """
    timestamp = datetime.now(pytz.timezone("Europe/Zurich")).strftime("%Y-%m-%d %H:%M:%S %Z")

    # Debugging
    logging.info("\n" * 10)
    logging.info(f"Timestamp {timestamp}")
   

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Healthcare Recipe Data Audit Report", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Audited File: {original_filename}")
    pdf.multi_cell(0, 10, f"Audit performed: {timestamp}")
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Audit Summary", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, audit_results)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Appendix: Full File Content", ln=True)

    pdf.set_font("Arial", "", 9)
    pdf.multi_cell(0, 5, json.dumps(file_contents, indent=2))


    return pdf.output(dest="S").encode("latin1")