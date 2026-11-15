import pandas as pd
from pathlib import Path

ADDRESS_COLUMNS = ["address", "memory_address", "access_address"]

def parse_address(value):
    if pd.isna(value):
        raise ValueError("Address column contains a blank value.")
    text = str(value).strip().replace("_", "")
    if not text:
        raise ValueError("Address column contains a blank value.")
    try:
        return int(text, 16) if text.lower().startswith("0x") else int(text, 10)
    except ValueError:
        raise ValueError(f"Invalid address '{text}'. Use decimal numbers or hexadecimal values such as 0x1A.")

def load_trace(source):
    try:
        frame = pd.read_csv(source)
    except Exception as exc:
        raise ValueError(f"Could not read CSV: {exc}")
    normalized = {str(c).strip().lower(): c for c in frame.columns}
    column = next((normalized[name] for name in ADDRESS_COLUMNS if name in normalized), None)
    if column is None:
        raise ValueError("Unsupported CSV format. Include one address column named: address, memory_address, or access_address.")
    if frame.empty:
        raise ValueError("CSV contains no memory accesses.")
    addresses = [parse_address(v) for v in frame[column].tolist()]
    if any(v < 0 for v in addresses):
        raise ValueError("Memory addresses must be non-negative.")
    return addresses, frame
