"""
clean_bls.py
Loads the BLS OEWS national wage Excel file, extracts
Computer & Mathematical occupations (SOC 15-xxxx),
and saves a clean benchmark CSV to data/processed/bls_clean.csv
"""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import config

# -------------------------------------------------------
# STEP 1: Load the BLS Excel file
# -------------------------------------------------------
print(f"Loading: {config.BLS_RAW_FILE}")

# The BLS file has a specific sheet name — try common ones
try:
    df = pd.read_excel(config.BLS_RAW_FILE, sheet_name="national_M2024_dl", dtype=str)
except Exception:
    # If sheet name doesn't match, load first sheet
    df = pd.read_excel(config.BLS_RAW_FILE, sheet_name=0, dtype=str)

print(f"Loaded {len(df):,} rows")
print("Columns:", list(df.columns))

# -------------------------------------------------------
# STEP 2: Standardize column names
# -------------------------------------------------------
df.columns = df.columns.str.strip().str.upper()

# -------------------------------------------------------
# STEP 3: Keep only relevant columns
# BLS OEWS standard column names:
#   OCC_CODE, OCC_TITLE, TOT_EMP, H_MEAN, A_MEAN, H_MEDIAN, A_MEDIAN
# -------------------------------------------------------
BLS_COLS = [
    "OCC_CODE",
    "OCC_TITLE",
    "TOT_EMP",
    "H_MEAN",     # hourly mean wage
    "A_MEAN",     # annual mean wage
    "H_MEDIAN",   # hourly median wage
    "A_MEDIAN",   # annual median wage (this is our primary benchmark)
]

cols_present = [c for c in BLS_COLS if c in df.columns]
cols_missing  = [c for c in BLS_COLS if c not in df.columns]
if cols_missing:
    print(f"Warning: missing columns: {cols_missing}")

df = df[cols_present].copy()

# -------------------------------------------------------
# STEP 4: Filter for Computer & Mathematical occupations
# SOC major group 15 = what H-1B tech roles map to
# -------------------------------------------------------
if "OCC_CODE" in df.columns:
    df = df[df["OCC_CODE"].str.startswith("15-", na=False)]
    print(f"After filtering for SOC 15-xxxx: {len(df):,} rows")

# -------------------------------------------------------
# STEP 5: Convert wage columns to numeric
# BLS uses "*" for suppressed values and "#" for $208,000+
# Replace those with NaN before converting
# -------------------------------------------------------
WAGE_COLS = ["H_MEAN", "A_MEAN", "H_MEDIAN", "A_MEDIAN"]
for col in WAGE_COLS:
    if col in df.columns:
        df[col] = (
            df[col]
            .str.replace(",", "", regex=False)   # remove thousand separators
            .str.replace("*", "", regex=False)   # suppressed
            .str.replace("#", "", regex=False)   # capped at 208k
            .str.strip()
            .replace("", None)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

# -------------------------------------------------------
# STEP 6: Add a normalized SOC code column for joining
# Strip the last two digits to get 4-digit SOC for broader matching
# e.g. 15-1132 -> 15-1132 (keep as-is; exact match preferred)
# -------------------------------------------------------
if "OCC_CODE" in df.columns:
    df["SOC_CODE_CLEAN"] = df["OCC_CODE"].str.strip()

# -------------------------------------------------------
# STEP 7: Drop rows with no median wage
# -------------------------------------------------------
if "A_MEDIAN" in df.columns:
    before = len(df)
    df = df[df["A_MEDIAN"].notna()]
    print(f"After dropping rows with no annual median: {len(df):,} rows "
          f"(dropped {before - len(df):,})")

# -------------------------------------------------------
# STEP 8: Save clean BLS file
# -------------------------------------------------------
config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
df.to_csv(config.BLS_CLEAN_FILE, index=False)
print(f"Saved: {config.BLS_CLEAN_FILE} ({len(df):,} rows)")
print("\nDone!")