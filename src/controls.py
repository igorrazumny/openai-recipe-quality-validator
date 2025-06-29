import streamlit as st
import textwrap

def display_controls():

    # Default model
    model = "gpt-4o"
    # Default number of entries evaluated from the file
    num_entries = 10000

    num_entries = st.slider(
      "🔢 Number of records to process from file:",
      min_value=10,
      max_value=10000,
      value=100,
      step=10,
      help="Controls how many records to evaluate in this run."
    )

    # Default system prompt
    default_system_prompt = textwrap.dedent("""\
    You are a healthcare recipe quality validation assistant.
    """)

    # Default user prompt
    default_user_prompt = textwrap.dedent("""\
    You are an expert Quality Assurance auditor specializing in pharmaceutical manufacturing processes.
    You will receive a list of structured JSON records describing recipe execution steps, including process parameters,
    operator information, timestamps, and status codes.

    For each record, please perform a thorough validation and deviation analysis as follows:

    1. **Completeness Check**
       - Identify any missing, null, or inconsistent fields (e.g., missing quantity_kg, incomplete operator name).

    2. **Format and Consistency Check**
       - Verify that timestamps follow ISO 8601 format and that start_time is earlier than end_time.
       - Confirm that status values conform to the allowed set: "in progress", "completed".

    3. **Logical Plausibility Check**
       - Validate that quantities are within realistic operational ranges (e.g., 0.01–1000 kg).
       - Identify any conflicting process steps or status codes.

    4. **Deviation Classification**
       - For each detected issue, assign:
         - a **Deviation Type** (e.g., Missing Data, Format Error, Value Out of Range, Status Conflict, Timestamp Error, Data Conflict, Invalid Status, Incomplete Record)
         - a **Severity Level** according to the definitions below (**Critical**, **Moderate**, or **Minor**)

       **Severity Definitions**

       - **Critical:**  
         Issues that pose a serious risk to patient safety, regulatory compliance, or process integrity.  
         Examples include:  
           - Missing required process steps (e.g., no sterilization step recorded)  
           - Grossly incorrect quantities (e.g., 5000 kg where the process allows max 1000 kg)  
           - Conflicting or invalid status codes (e.g., “completed” with no start time)  
           - Data that could indicate potential fraud or falsification  
           - Steps that contradict the approved recipe version  
           - Negative quantities in required positive fields  

       - **Moderate:**  
         Issues that could impact product quality, data integrity, or operational efficiency but do not immediately endanger safety or compliance.  
         Examples include:  
           - Quantities slightly outside expected ranges (e.g., 1001 kg where the limit is 1000)  
           - Incomplete operator names (e.g., “J.”)  
           - Non-standard or inconsistent timestamps (e.g., using DD/MM/YYYY when ISO format is required)  
           - Inconsistent sequencing of steps  
           - Duplicate records for the same step  
           - Use of deprecated process codes  
           - Missing optional but recommended fields  

       - **Minor:**  
         Issues that are unlikely to materially affect the process or outcomes but should still be corrected.  
         Examples include:  
           - Minor formatting errors (e.g., extra spaces, inconsistent casing)  
           - Non-critical typos in descriptive fields  
           - Timestamps missing seconds if not strictly required  
           - Slight deviations from naming conventions  
           - Use of alternative terminology that is still understandable

    5. **Summary Text**
       - After evaluating all records, produce a **verbal executive summary** describing the overall data quality, key trends, and any significant risks.
       - Your summary should **generally be short (5–6 sentences)** if the data are mostly compliant or have simple issues.
       - If the data contain numerous or severe deviations, expand the summary as needed to clearly communicate important details. You may use **up to 15 sentences** if necessary.
       - The goal is to ensure the recipient understands the criticality and context of the findings without reviewing all individual deviations.

    6. **Deviation Type Severity Mapping**
       - For known deviation types, **always assign the following severity**, overriding other definitions if there is any conflict:
           - Missing Required Step: Critical
           - Grossly Incorrect Quantity: Critical
           - Conflicting Status Code: Critical
           - Negative Quantity: Critical
           - Slightly Out of Range Quantity: Moderate
           - Incomplete Operator Name: Moderate
           - Non-Standard Timestamp: Moderate
           - Duplicate Record: Moderate
           - Minor Formatting Error: Minor
           - Non-Critical Typo: Minor
       - If a deviation does not fit these mappings, classify it using your best judgment.

    7. **Structured Output Format**
       - Return a single valid JSON object with the following schema:

    {
        "summary_text": "<short verbal summary here>",
        "data_quality_score": <integer from 1 to 10>,
        "records": [
            {
                "id": "<record id>",
                "deviations": [
                    {
                        "type": "<Deviation Type>",
                        "severity": "<Severity Level>",
                        "description": "<Detailed explanation>"
                    }
                    ...
                ]
            },
            ...
        ]
    }

    - If no deviations are found for a record, include the record in the array with an empty deviations list.
    - Do not include any additional commentary or explanation outside this JSON.
    """)

    # Expander for System Prompt
    with st.expander("🛠️ Advanced Settings – System Prompt"):
        system_prompt = st.text_area(
            "System Prompt:",
            value=default_system_prompt,
            height=68
        )

    # Expander for User Prompt
    with st.expander("📝 Advanced Settings – User Prompt"):
        user_prompt = st.text_area(
            "User Prompt:",
            value=default_user_prompt,
            height=700
        )

    uploaded_file = st.file_uploader(
        "📂 Upload a JSON or CSV recipe file for audit:",
        type=["json", "csv"],
        help="Click to upload a file. Only .json or .csv formats are supported."
    )

    return uploaded_file, num_entries, model, system_prompt, user_prompt