"""
clean_h1b.py
Loads the raw DOL LCA disclosure Excel file, cleans and filters it,
and saves a processed CSV to data/processed/h1b_clean.csv
"""

import sys
import re
from pathlib import Path

import pandas as pd

# --- Make sure src/ is on the path so we can import config ---
sys.path.insert(0, str(Path(__file__).parent))
import config

# -------------------------------------------------------
# STEP 1: Load the raw Excel file
# -------------------------------------------------------
print(f"Loading: {config.H1B_RAW_FILE}")
print("This may take 1-3 minutes for large files...")

df = pd.read_excel(config.H1B_RAW_FILE, dtype=str)

print(f"Loaded {len(df):,} rows and {len(df.columns)} columns")
print("Columns found:", list(df.columns))

# -------------------------------------------------------
# STEP 2: Standardize column names
# Strip whitespace and convert to uppercase
# -------------------------------------------------------
df.columns = df.columns.str.strip().str.upper()

# -------------------------------------------------------
# STEP 3: Keep only the columns we need
# These are the standard FY2020+ FLAG system column names.
# If your file has slightly different names, check the
# print output above and adjust this list.
# -------------------------------------------------------
COLS_NEEDED = [
    "CASE_NUMBER",
    "CASE_STATUS",
    "EMPLOYER_NAME",
    "JOB_TITLE",
    "SOC_CODE",
    "SOC_TITLE",
    "WAGE_RATE_OF_PAY_FROM",
    "WAGE_UNIT_OF_PAY",
    "PREVAILING_WAGE",
    "PW_UNIT_OF_PAY",
    "PW_WAGE_LEVEL",
    "TOTAL_WORKER_POSITIONS",
]

# Only keep columns that actually exist in the file
cols_present = [c for c in COLS_NEEDED if c in df.columns]
cols_missing = [c for c in COLS_NEEDED if c not in df.columns]

if cols_missing:
    print(f"Warning: these columns were not found and will be skipped: {cols_missing}")

df = df[cols_present].copy()

# -------------------------------------------------------
# STEP 4: Keep only certified H-1B applications
# -------------------------------------------------------
if "CASE_STATUS" in df.columns:
    df = df[df["CASE_STATUS"].str.upper().str.contains("CERTIFIED", na=False)]
    print(f"After filtering for certified cases: {len(df):,} rows")

# -------------------------------------------------------
# STEP 5: Clean and standardize employer names
# Convert to uppercase, strip extra spaces, remove punctuation
# -------------------------------------------------------
if "EMPLOYER_NAME" in df.columns:
    df["EMPLOYER_NAME"] = (
        df["EMPLOYER_NAME"]
        .str.upper()
        .str.strip()
        .str.replace(r"[^\w\s]", "", regex=True)  # remove punctuation
        .str.replace(r"\s+", " ", regex=True)      # collapse multiple spaces
    )

# -------------------------------------------------------
# STEP 6: Clean SOC codes
# Standard format is XX-XXXX (e.g. 15-1132)
# -------------------------------------------------------
if "SOC_CODE" in df.columns:
    df["SOC_CODE"] = (
        df["SOC_CODE"]
        .str.strip()
        .str.replace(r"\.\d+$", "", regex=True)  # remove .0, .00, .01 etc
    )

# -------------------------------------------------------
# STEP 7: Filter for technology-related SOC codes
# SOC major group 15 = Computer and Mathematical occupations
# -------------------------------------------------------
if "SOC_CODE" in df.columns:
    tech_mask = df["SOC_CODE"].str.startswith(
        tuple(config.TECH_SOC_PREFIXES), na=False
    )
    df = df[tech_mask]
    print(f"After filtering for tech SOC codes (15-xxxx): {len(df):,} rows")

# -------------------------------------------------------
# STEP 8: Convert wage columns to numeric (annual dollars)
# Wages may be hourly, weekly, monthly, or annual
# -------------------------------------------------------
def to_annual(wage_str, unit_str):
    """Convert wage to annual based on pay unit."""
    multipliers = {
        "HOUR":       2080,   # 40 hrs/wk * 52 wks
        "WEEK":       52,
        "BI-WEEKLY":  26,
        "MONTH":      12,
        "YEAR":       1,
        "ANNUAL":     1,
    }
    try:
        wage = float(str(wage_str).replace(",", "").strip())
        unit = str(unit_str).upper().strip()
        mult = multipliers.get(unit, 1)
        return wage * mult
    except (ValueError, TypeError):
        return None

if "WAGE_RATE_OF_PAY_FROM" in df.columns and "WAGE_UNIT_OF_PAY" in df.columns:
    df["OFFERED_WAGE_ANNUAL"] = df.apply(
        lambda r: to_annual(r["WAGE_RATE_OF_PAY_FROM"], r["WAGE_UNIT_OF_PAY"]),
        axis=1
    )

if "PREVAILING_WAGE" in df.columns and "PW_UNIT_OF_PAY" in df.columns:
    df["PREVAILING_WAGE_ANNUAL"] = df.apply(
        lambda r: to_annual(r["PREVAILING_WAGE"], r["PW_UNIT_OF_PAY"]),
        axis=1
    )

# -------------------------------------------------------
# STEP 9: Filter for realistic annual wages
# Drop rows where offered wage is below $20k or above $1M
# (likely data entry errors or unit mismatches)
# -------------------------------------------------------
if "OFFERED_WAGE_ANNUAL" in df.columns:
    before = len(df)
    df = df[
        df["OFFERED_WAGE_ANNUAL"].between(20_000, 1_000_000, inclusive="both")
    ]
    print(f"After wage sanity filter: {len(df):,} rows (dropped {before - len(df):,})")

# -------------------------------------------------------
# STEP 10: Filter for target companies (Fortune 500 proxy)
# Keep rows where the employer name contains any target keyword
# -------------------------------------------------------
if "EMPLOYER_NAME" in df.columns:
    pattern = "|".join(config.TARGET_COMPANIES)
    target_mask = df["EMPLOYER_NAME"].str.contains(pattern, na=False)
    df_target = df[target_mask].copy()
    print(f"Rows matching target companies: {len(df_target):,}")
else:
    df_target = df.copy()

# -------------------------------------------------------
# STEP 11: Add a simplified company label column
# Maps messy employer names to clean short names
# -------------------------------------------------------
def map_company(name):
    """Return a clean short company name for known employers."""
    name = str(name).upper()
    mapping = {
        "AMAZON":      "Amazon",
        "GOOGLE":      "Google",
        "MICROSOFT":   "Microsoft",
        "APPLE":       "Apple",
        "META":        "Meta",
        "IBM":         "IBM",
        "ORACLE":      "Oracle",
        "INTEL":       "Intel",
        "CISCO":       "Cisco",
        "QUALCOMM":    "Qualcomm",
        "JPMORGAN":    "JPMorgan",
        "GOLDMAN":     "Goldman Sachs",
        "WALMART":     "Walmart",
        "DELOITTE":    "Deloitte",
        "ACCENTURE":   "Accenture",
        "CAPGEMINI":   "Capgemini",
        "COGNIZANT":   "Cognizant",
        "INFOSYS":     "Infosys",
        "TATA":        "Tata Consultancy",
        "WIPRO":       "Wipro",
    }
    for keyword, label in mapping.items():
        if keyword in name:
            return label
    return name  # fallback: return as-is

if "EMPLOYER_NAME" in df_target.columns:
    df_target["COMPANY"] = df_target["EMPLOYER_NAME"].apply(map_company)

# -------------------------------------------------------
# STEP 12: Save both full tech file and target company file
# -------------------------------------------------------
config.DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# Full tech dataset (all companies, tech SOC codes only)
full_out = config.DATA_PROCESSED / "h1b_tech_all.csv"
df.to_csv(full_out, index=False)
print(f"Saved full tech dataset: {full_out} ({len(df):,} rows)")

# Target companies only
target_out = config.H1B_CLEAN_FILE
df_target.to_csv(target_out, index=False)
print(f"Saved target company dataset: {target_out} ({len(df_target):,} rows)")

print("\nDone! Check data/processed/ for your cleaned files.")