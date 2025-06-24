# utils.py
# Shared utility functions like file reading and cost estimation.

def estimate_cost(num_tokens: int, model: str) -> float:
    """
    Estimate the cost based on the number of tokens and model selected.
    """
    if model.startswith("gpt-3.5"):
        price_per_1k = 0.001  # USD per 1K tokens (input only)
    elif model.startswith("gpt-4o"):
        price_per_1k = 0.005  # USD per 1K tokens (input only)
    else:
        price_per_1k = 0.01  # fallback/default

    return round((num_tokens / 1000) * price_per_1k, 4)

def extract_file_metadata(uploaded_file, content_bytes):
    """
    Extracts filename, content string, and extension from the uploaded file.
    """
    filename = uploaded_file.name
    file_extension = filename.split(".")[-1].lower()
    try:
        content_str = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        content_str = content_bytes.decode("latin1")  # fallback for non-UTF-8
    return filename, content_str, file_extension

def extract_file_content(uploaded_file):
    content_bytes = uploaded_file.read()
    content_str = content_bytes.decode("utf-8")  # or with fallback
    return content_bytes, content_str

def detect_file_type(file_name: str) -> str:
    if file_name.endswith(".json"):
        return "json"
    elif file_name.endswith(".csv"):
        return "csv"
    else:
        return "unknown"