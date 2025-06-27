from fpdf import FPDF
from datetime import datetime
import pytz
import json

def clean_nested_text(obj):
    """
    Recursively clean all string values in nested dicts and lists.
    """
    if isinstance(obj, dict):
        return {k: clean_nested_text(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nested_text(item) for item in obj]
    elif isinstance(obj, str):
        return obj.encode("latin-1", "ignore").decode("latin-1")
    else:
        return obj

def generate_audit_report(audit_results, original_filename, file_contents, summary_stats):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    audit_results = clean_nested_text(audit_results)
    file_contents = clean_nested_text(file_contents)

    # Title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Healthcare Recipe Data Audit Report", ln=True)

    # File info
    pdf.set_font("Arial", "", 12)
    pdf.ln(5)
    pdf.multi_cell(0, 8, f"Audited File: {original_filename}")
    timestamp = datetime.now(pytz.timezone("Europe/Zurich")).strftime("%Y-%m-%d %H:%M:%S %Z")
    pdf.multi_cell(0, 8, f"Audit performed: {timestamp}")

    pdf.ln(5)

    # Executive Summary
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Executive Summary", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.ln(2)

    if "summary_text" in audit_results:
        pdf.multi_cell(0, 8, audit_results["summary_text"])
        pdf.ln(4)

    lines = [
        f"- Overall Data Quality Score (1-10): {summary_stats['data_quality_score']}",
        f"- Total entries in file: {summary_stats['total_entries_in_file']}",
        f"- Total records audited: {summary_stats['total_records']}",
        f"- Records with deviations: {summary_stats['records_with_deviations']} "
        f"(of which {summary_stats['records_with_multiple_deviations']} had multiple deviations)",
        f"- Records fully compliant: {summary_stats['records_fully_compliant']}",
        f"- Compliance rate: {summary_stats['compliance_rate']}%",
        f"- Number of critical deviations: {summary_stats['critical']}",
        f"- Number of moderate deviations: {summary_stats['moderate']}",
        f"- Number of minor deviations: {summary_stats['minor']}",
    ]
    for line in lines:
        pdf.multi_cell(0, 8, line)

    pdf.ln(4)

    # Most common critical deviations
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Most common critical deviations:", ln=True)
    pdf.set_font("Arial", "", 12)
    crit_counts = summary_stats.get("critical_types", {})
    if crit_counts:
        for t, count in crit_counts.items():
            pdf.multi_cell(0, 8, f"- {t}: {count}")
    else:
        pdf.multi_cell(0, 8, "- None")

    pdf.ln(2)

    # Most common moderate deviations
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Most common moderate deviations:", ln=True)
    pdf.set_font("Arial", "", 12)
    mod_counts = summary_stats.get("moderate_types", {})
    if mod_counts:
        for t, count in mod_counts.items():
            pdf.multi_cell(0, 8, f"- {t}: {count}")
    else:
        pdf.multi_cell(0, 8, "- None")

    pdf.ln(4)

    # Note
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(
        0,
        6,
        (
            "**According to industry standards, records with critical findings should be remediated within 7 days, "
            "and records with moderate findings within 30 days.**"
        ),
    )

    pdf.ln(8)

    # Start Detailed Findings on a new page
    pdf.add_page()

    # Detailed Findings
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Detailed Findings", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.ln(2)

    severity_order = {"critical": 1, "moderate": 2, "minor": 3}

    records = audit_results.get("records", [])
    # Filter to records with deviations
    records_with_devs = [r for r in records if r.get("deviations")]
    # Sort records by most severe deviation in each record
    def record_severity(rec):
        if not rec.get("deviations"):
            return 4
        severities = [severity_order.get(d.get("severity", "").lower(), 4) for d in rec["deviations"]]
        return min(severities)

    records_with_devs.sort(key=record_severity)

    for rec in records_with_devs:
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 8, f"Record ID: {rec.get('id')}")
        pdf.set_font("Arial", "", 12)
        deviations = rec.get("deviations", [])
        for dev in deviations:
            pdf.multi_cell(0, 6, f"- Deviation Type: {dev.get('type')}")
            pdf.multi_cell(0, 6, f"  Severity: {dev.get('severity')}")
            pdf.multi_cell(0, 6, f"  Description: {dev.get('description')}")
        pdf.ln(2)

    # Appendix
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Appendix: Full File Content", ln=True)
    pdf.ln(3)

    pdf.set_font("Courier", "", 8)
    file_json = json.dumps(file_contents, indent=2, ensure_ascii=False, sort_keys=True)
    for line in file_json.splitlines():
        pdf.multi_cell(0, 4, line)

    return pdf.output(dest="S").encode("latin1")