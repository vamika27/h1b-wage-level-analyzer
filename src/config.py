"""
config.py
Central configuration: file paths and shared constants.
"""
from pathlib import Path

# --- Project root (this file lives in src/, so go up one level) ---
ROOT = Path(__file__).resolve().parent.parent

# --- Directory paths ---
DATA_RAW       = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
OUTPUTS        = ROOT / "outputs"
FIGURES        = OUTPUTS / "figures"
TABLES         = OUTPUTS / "tables"
SQL_DIR        = ROOT / "sql"

# --- Raw input filenames ---
H1B_RAW_FILE = DATA_RAW / "LCA_Disclosure_Data_FY2024_Q4.xlsx"
BLS_RAW_FILE = DATA_RAW / "national_M2024_dl.xlsx"

# --- Processed output filenames ---
H1B_CLEAN_FILE = DATA_PROCESSED / "h1b_clean.csv"
BLS_CLEAN_FILE = DATA_PROCESSED / "bls_clean.csv"
WAGE_GAP_FILE  = DATA_PROCESSED / "wage_gap_by_employer.csv"

# --- Database path ---
DB_FILE = ROOT / "h1b_analysis.duckdb"

# --- Tech SOC code prefixes (15-xxxx = Computer & Mathematical) ---
TECH_SOC_PREFIXES = ("15-",)

# --- Target companies ---
TARGET_COMPANIES = [
    "AMAZON", "GOOGLE", "MICROSOFT", "APPLE", "META", "IBM",
    "ORACLE", "INTEL", "CISCO", "DELL", "HP", "QUALCOMM",
    "JPMORGAN", "GOLDMAN SACHS", "WALMART", "DELOITTE",
    "ACCENTURE", "CAPGEMINI", "COGNIZANT", "INFOSYS",
    "TATA CONSULTANCY", "WIPRO",
]

# --- Create output dirs if missing ---
for d in (DATA_PROCESSED, FIGURES, TABLES):
    d.mkdir(parents=True, exist_ok=True)