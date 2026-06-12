"""
run_sql.py
Loads cleaned CSVs into DuckDB, creates tables, runs analysis
queries, and saves results as CSVs to outputs/tables/.
"""

import sys
import re
from pathlib import Path

import duckdb
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import config

# -------------------------------------------------------
# STEP 1: Connect to DuckDB (creates file if not exists)
# -------------------------------------------------------
print(f"Connecting to DuckDB at: {config.DB_FILE}")
con = duckdb.connect(str(config.DB_FILE))

# -------------------------------------------------------
# STEP 2: Run schema.sql to create tables
# -------------------------------------------------------
schema_sql = (config.SQL_DIR / "schema.sql").read_text()
con.execute(schema_sql)
print("Tables created.")

# -------------------------------------------------------
# STEP 3: Load cleaned CSVs into DuckDB tables
# -------------------------------------------------------
print(f"Loading H-1B data from: {config.H1B_CLEAN_FILE}")
con.execute(f"""
    COPY h1b FROM '{config.H1B_CLEAN_FILE}'
    (FORMAT CSV, HEADER TRUE, NULL '')
""")
h1b_count = con.execute("SELECT COUNT(*) FROM h1b").fetchone()[0]
print(f"  Loaded {h1b_count:,} rows into h1b table")

print(f"Loading BLS data from: {config.BLS_CLEAN_FILE}")
con.execute(f"""
    COPY bls_wages FROM '{config.BLS_CLEAN_FILE}'
    (FORMAT CSV, HEADER TRUE, NULL '')
""")
bls_count = con.execute("SELECT COUNT(*) FROM bls_wages").fetchone()[0]
print(f"  Loaded {bls_count:,} rows into bls_wages table")

# -------------------------------------------------------
# STEP 4: Run analysis queries and save results
# -------------------------------------------------------
analysis_sql = (config.SQL_DIR / "analysis.sql").read_text()

# Split on comment markers like -- Q1_TOP_COMPANIES
query_blocks = re.split(r'--\s*(Q\d+_\w+)\s*\n', analysis_sql)

# query_blocks alternates: [preamble, name1, sql1, name2, sql2, ...]
queries = {}
i = 1
while i < len(query_blocks) - 1:
    name = query_blocks[i].strip()
    sql  = query_blocks[i + 1].strip()
    queries[name] = sql
    i += 2

config.TABLES.mkdir(parents=True, exist_ok=True)

print("\nRunning queries:")
for name, sql in queries.items():
    try:
        df = con.execute(sql).df()
        out_path = config.TABLES / f"{name.lower()}.csv"
        df.to_csv(out_path, index=False)
        print(f"  {name}: {len(df)} rows → {out_path.name}")
    except Exception as e:
        print(f"  {name}: ERROR — {e}")

# -------------------------------------------------------
# STEP 5: Print a preview of key results
# -------------------------------------------------------
print("\n--- PREVIEW: Top companies by filings ---")
try:
    df = pd.read_csv(config.TABLES / "q1_top_companies.csv")
    print(df[["COMPANY", "total_filings", "avg_offered_wage"]].to_string(index=False))
except Exception:
    pass

print("\n--- PREVIEW: Companies by Level I share ---")
try:
    df = pd.read_csv(config.TABLES / "q3_level1_share.csv")
    print(df[["COMPANY", "total_filings", "pct_level1", "pct_level1_or_2"]]
          .head(10).to_string(index=False))
except Exception:
    pass

print("\n--- PREVIEW: Wage gap by company ---")
try:
    df = pd.read_csv(config.TABLES / "q4_wage_gap.csv")
    print(df[["COMPANY", "avg_offered_wage", "avg_bls_median", "avg_wage_gap_pct"]]
          .head(10).to_string(index=False))
except Exception:
    pass

con.close()
print("\nDone! Results saved to outputs/tables/")