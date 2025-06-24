import streamlit as st

def display_controls():

    # Default model
    model="gpt-4o"
    # Default number of entries evaluated from the file
    num_entries = 100


    uploaded_file = st.file_uploader(
        "📂 Upload a JSON or CSV recipe file for audit:",
        type=["json", "csv"],
        help="Click to upload a file. Only .json or .csv formats are supported."
    )

    # entry_limit = st.selectbox(
    #     "🔢 How many entries should be audited? (number of entries impacts cost of each audit run which becomes substantial for very big data sets)",
    #     options=[
    #         "100 (est. $0.01)", 
    #         "1000 (est. $0.10)", 
    #         "10000 (est. $1.00)", 
    #         "Full file (est. cost depends on the size of the file)"
    #     ],
    #     index=0,
    #     help="Choose how many entries from the uploaded file should be analyzed."
    # )

    # model_options = {
    #     "gpt-3.5-turbo": "gpt-3.5-turbo",
    #     "gpt-4o (also known as GPT-4.1, most advanced public model)": "gpt-4o"
    # }

    # model_display = st.selectbox(
    #     "🧠 Select OpenAI model:",
    #     options=list(model_options.keys()),
    #     index=1,
    #     help="GPT-4o is the latest and most capable public model from OpenAI."
    # )

    # model = model_options[model_display]

    

    # num_entries = (
    #     entry_limit.split(" ")[0] if not entry_limit.startswith("Full") else "full"
    # )

    return uploaded_file, num_entries, model