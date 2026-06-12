"""
visualize.py
Generates 6 figures from SQL output CSVs and saves them
to outputs/figures/. Run after src/run_sql.py completes.
"""

import sys
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import config

# -------------------------------------------------------
# Global style settings
# -------------------------------------------------------
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)
plt.rcParams.update({
    "figure.dpi":       150,
    "savefig.dpi":      150,
    "savefig.bbox":     "tight",
    "figure.facecolor": "white",
    "axes.facecolor":   "white",
    "axes.spines.top":  False,
    "axes.spines.right":False,
})

FIGURES = config.FIGURES
FIGURES.mkdir(parents=True, exist_ok=True)

def load(filename):
    """Load a CSV from outputs/tables/ with error handling."""
    path = config.TABLES / filename
    if not path.exists():
        print(f"  WARNING: {filename} not found — skipping this chart.")
        return None
    df = pd.read_csv(path)
    if df.empty:
        print(f"  WARNING: {filename} is empty — skipping this chart.")
        return None
    return df

print("Generating figures...")

# ============================================================
# FIGURE 1: Top 15 companies by H-1B tech filings
# ============================================================
def fig1_top_companies():
    df = load("q1_top_companies.csv")
    if df is None: return
    df = df.sort_values("total_filings", ascending=True).tail(15)

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.barh(df["COMPANY"], df["total_filings"],
                   color=sns.color_palette("Blues_d", len(df)))
    ax.set_xlabel("Total H-1B Tech Filings", labelpad=10)
    ax.set_title("Top 15 Companies by H-1B Technology Filings\n(FY2024, SOC 15-xxxx)",
                 fontsize=13, fontweight="bold", pad=15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, _: f"{int(x):,}"))
    for bar in bars:
        w = bar.get_width()
        ax.text(w + max(df["total_filings"]) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{int(w):,}", va="center", fontsize=9)
    plt.tight_layout()
    out = FIGURES / "fig1_top_companies.png"
    fig.savefig(out)
    plt.close()
    print(f"  Saved: {out.name}")

# ============================================================
# FIGURE 2: Wage level distribution by company (stacked bar)
# ============================================================
def fig2_wage_level_dist():
    df = load("q2_wage_level_dist.csv")
    if df is None: return
    top_cos = load("q1_top_companies.csv")
    if top_cos is None: return

    # Limit to top 12 companies by filing volume
    top12 = top_cos.head(12)["COMPANY"].tolist()
    df = df[df["COMPANY"].isin(top12)]

    pivot = df.pivot_table(
        index="COMPANY", columns="PW_WAGE_LEVEL",
        values="pct_of_company", aggfunc="sum"
    ).fillna(0)


    ordered = [c for c in ["I", "II", "III", "IV"] if c in pivot.columns]
    pivot = pivot[ordered]

    colors = ["#d73027", "#fc8d59", "#91bfdb", "#4575b4"][:len(ordered)]

    fig, ax = plt.subplots(figsize=(12, 7))
    pivot.plot(kind="bar", stacked=True, ax=ax, color=colors,
               edgecolor="white", linewidth=0.5)
    ax.set_xlabel("")
    ax.set_ylabel("Percentage of Filings (%)", labelpad=10)
    ax.set_title("Prevailing Wage Level Distribution by Company\n(% of each company's H-1B tech filings)",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha="right", fontsize=9)
    ax.legend(title="Wage Level", bbox_to_anchor=(1.01, 1), loc="upper left")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    plt.tight_layout()
    out = FIGURES / "fig2_wage_level_dist.png"
    fig.savefig(out)
    plt.close()
    print(f"  Saved: {out.name}")

# ============================================================
# FIGURE 3: Companies ranked by % Level I filings (bar chart)
# ============================================================
def fig3_level1_share():
    df = load("q3_level1_share.csv")
    if df is None: return
    df = df.sort_values("pct_level1_or_2", ascending=True).tail(15)

    fig, ax = plt.subplots(figsize=(10, 7))
    palette = ["#d73027" if v >= 50 else "#fc8d59" if v >= 25
               else "#91bfdb" for v in df["pct_level1_or_2"]]
    ax.barh(df["COMPANY"], df["pct_level1_or_2"], color=palette)
    ax.axvline(x=50, color="black", linestyle="--", linewidth=0.8,
               label="50% threshold")
    ax.set_xlabel("% of Filings at Level I or II", labelpad=10)
    ax.set_title("Companies by Share of Level I & II Wage Filings\n(Higher = more entry-level wage classifications)",
                 fontsize=13, fontweight="bold", pad=15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:.0f}%"))
    ax.legend(fontsize=9)
    plt.tight_layout()
    out = FIGURES / "fig3_level1_share.png"
    fig.savefig(out)
    plt.close()
    print(f"  Saved: {out.name}")

# ============================================================
# FIGURE 4: Average wage gap by company (horizontal bar)
# ============================================================
def fig4_wage_gap_by_company():
    df = load("q4_wage_gap.csv")
    if df is None: return
    df = df.sort_values("avg_wage_gap_pct", ascending=True).head(15)

    colors = ["#d73027" if v < 0 else "#4575b4"
              for v in df["avg_wage_gap_pct"]]

    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(df["COMPANY"], df["avg_wage_gap_pct"], color=colors)
    ax.axvline(x=0, color="black", linewidth=0.8)
    ax.set_xlabel("Avg Wage Gap vs BLS Median (%)", labelpad=10)
    ax.set_title("Average Wage Gap vs BLS Occupational Median\nby Company (FY2024 H-1B Tech Filings)",
                 fontsize=13, fontweight="bold", pad=15)
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:+.1f}%"))
    for i, (val, company) in enumerate(zip(df["avg_wage_gap_pct"], df["COMPANY"])):
        ax.text(val - 0.5 if val < 0 else val + 0.5, i,
                f"{val:+.1f}%", va="center",
                ha="right" if val < 0 else "left", fontsize=9)
    plt.tight_layout()
    out = FIGURES / "fig4_wage_gap_company.png"
    fig.savefig(out)
    plt.close()
    print(f"  Saved: {out.name}")

# ============================================================
# FIGURE 5: Offered wage vs BLS median scatterplot
# ============================================================
def fig5_scatter_offered_vs_bls():
    df = load("q4_wage_gap.csv")
    if df is None: return

    fig, ax = plt.subplots(figsize=(9, 7))
    colors = ["#d73027" if v < 0 else "#4575b4"
              for v in df["avg_wage_gap_pct"]]
    scatter = ax.scatter(
        df["avg_bls_median"], df["avg_offered_wage"],
        c=colors, s=80, alpha=0.8, edgecolors="white", linewidths=0.5
    )
    # Add 45-degree parity line
    lim_min = min(df["avg_bls_median"].min(), df["avg_offered_wage"].min()) * 0.9
    lim_max = max(df["avg_bls_median"].max(), df["avg_offered_wage"].max()) * 1.1
    ax.plot([lim_min, lim_max], [lim_min, lim_max],
            "k--", linewidth=0.9, label="Parity (offered = BLS median)")
    ax.set_xlabel("BLS Occupational Median Wage ($)", labelpad=10)
    ax.set_ylabel("Average Offered Wage ($)", labelpad=10)
    ax.set_title("Offered Wage vs BLS Median by Company\n(Points below dashed line = below BLS median)",
                 fontsize=13, fontweight="bold", pad=15)
    # Label each point with company name
    for _, row in df.iterrows():
        ax.annotate(row["COMPANY"],
                    (row["avg_bls_median"], row["avg_offered_wage"]),
                    textcoords="offset points", xytext=(5, 3), fontsize=7)
    fmt = mticker.FuncFormatter(lambda x, _: f"${int(x):,}")
    ax.xaxis.set_major_formatter(fmt)
    ax.yaxis.set_major_formatter(fmt)
    ax.legend(fontsize=9)
    plt.tight_layout()
    out = FIGURES / "fig5_scatter_offered_vs_bls.png"
    fig.savefig(out)
    plt.close()
    print(f"  Saved: {out.name}")

# ============================================================
# FIGURE 6: Wage gap heatmap by occupation and company
# ============================================================
def fig6_heatmap_gap_by_soc():
    df_soc  = load("q5_gap_by_soc.csv")
    df_gap  = load("q4_wage_gap.csv")
    h1b_raw = load("q1_top_companies.csv")
    if any(x is None for x in [df_soc, df_gap, h1b_raw]):
        return

    # Re-derive from the raw h1b_clean and bls_clean files.
    try:
        h1b = pd.read_csv(config.H1B_CLEAN_FILE)
        bls = pd.read_csv(config.BLS_CLEAN_FILE)
    except Exception as e:
        print(f"  Skipping fig6 — could not load processed CSVs: {e}")
        return

    merged = h1b.merge(
        bls[["SOC_CODE_CLEAN", "A_MEDIAN"]],
        left_on="SOC_CODE", right_on="SOC_CODE_CLEAN", how="inner"
    )
    merged = merged[merged["A_MEDIAN"].notna() & merged["OFFERED_WAGE_ANNUAL"].notna()]
    merged["wage_gap_pct"] = (
        (merged["OFFERED_WAGE_ANNUAL"] - merged["A_MEDIAN"]) / merged["A_MEDIAN"] * 100
    )

    # Top 10 companies and top 8 SOC titles
    top_cos  = h1b_raw.head(10)["COMPANY"].tolist()
    top_socs = (merged.groupby("SOC_TITLE")["wage_gap_pct"]
                .count().nlargest(8).index.tolist())

    heat_df = (merged[merged["COMPANY"].isin(top_cos) &
                      merged["SOC_TITLE"].isin(top_socs)]
               .groupby(["COMPANY", "SOC_TITLE"])["wage_gap_pct"]
               .mean()
               .unstack(fill_value=0))

    if heat_df.empty:
        print("  Skipping fig6 — insufficient data for heatmap.")
        return

    # Shorten SOC titles for readability
    heat_df.columns = [c[:30] for c in heat_df.columns]

    fig, ax = plt.subplots(figsize=(14, 7))
    sns.heatmap(
        heat_df, annot=True, fmt=".1f", center=0,
        cmap="RdYlBu", linewidths=0.4, linecolor="white",
        cbar_kws={"label": "Avg Wage Gap vs BLS Median (%)"},
        ax=ax
    )
    ax.set_title("Average Wage Gap (%) by Company and Occupation\n(Negative = below BLS median; Positive = above)",
                 fontsize=13, fontweight="bold", pad=15)
    ax.set_xlabel("Occupation (SOC Title)", labelpad=10)
    ax.set_ylabel("Company", labelpad=10)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=35, ha="right", fontsize=8)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=9)
    plt.tight_layout()
    out = FIGURES / "fig6_heatmap_gap_by_soc.png"
    fig.savefig(out)
    plt.close()
    print(f"  Saved: {out.name}")




# Run all figures

if __name__ == "__main__":
    fig1_top_companies()
    fig2_wage_level_dist()
    fig3_level1_share()
    fig4_wage_gap_by_company()
    fig5_scatter_offered_vs_bls()
    fig6_heatmap_gap_by_soc()
    print(f"\nAll done. Figures saved to: {FIGURES}")