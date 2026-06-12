-- analysis.sql
-- All analytical queries for the H-1B wage level analysis.
-- Each query is separated by a comment header.
-- Run via src/run_sql.py

-- ============================================================
-- QUERY 1: Top 15 companies by total H-1B tech filings
-- ============================================================
-- Q1_TOP_COMPANIES
SELECT
    COMPANY,
    COUNT(*)                        AS total_filings,
    ROUND(AVG(OFFERED_WAGE_ANNUAL)) AS avg_offered_wage,
    ROUND(AVG(PREVAILING_WAGE_ANNUAL)) AS avg_prevailing_wage
FROM h1b
WHERE COMPANY IS NOT NULL
GROUP BY COMPANY
ORDER BY total_filings DESC
LIMIT 15;

-- ============================================================
-- QUERY 2: Wage level distribution by company
-- (What % of each company's filings are Level 1, 2, 3, 4)
-- ============================================================
-- Q2_WAGE_LEVEL_DIST
SELECT
    COMPANY,
    PW_WAGE_LEVEL,
    COUNT(*) AS filings,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY COMPANY),
        1
    ) AS pct_of_company
FROM h1b
WHERE COMPANY IS NOT NULL
  AND PW_WAGE_LEVEL IS NOT NULL
  AND PW_WAGE_LEVEL != ''
GROUP BY COMPANY, PW_WAGE_LEVEL
ORDER BY COMPANY, PW_WAGE_LEVEL;

-- ============================================================
-- QUERY 3: Companies ranked by share of Level I filings
-- (Higher share = more entry-level wage classifications)
-- ============================================================
-- Q3_LEVEL1_SHARE
SELECT
    COMPANY,
    COUNT(*)  AS total_filings,
    SUM(CASE WHEN PW_WAGE_LEVEL = 'I'  THEN 1 ELSE 0 END) AS level1_count,
    SUM(CASE WHEN PW_WAGE_LEVEL = 'II' THEN 1 ELSE 0 END) AS level2_count,
    ROUND(
        SUM(CASE WHEN PW_WAGE_LEVEL = 'I' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        1
    ) AS pct_level1,
    ROUND(
        (SUM(CASE WHEN PW_WAGE_LEVEL = 'I'  THEN 1 ELSE 0 END) +
         SUM(CASE WHEN PW_WAGE_LEVEL = 'II' THEN 1 ELSE 0 END)) * 100.0 / COUNT(*),
        1
    ) AS pct_level1_or_2
FROM h1b
WHERE COMPANY IS NOT NULL
  AND PW_WAGE_LEVEL IS NOT NULL
  AND PW_WAGE_LEVEL != ''
GROUP BY COMPANY
HAVING COUNT(*) >= 10
ORDER BY pct_level1 DESC;

-- ============================================================
-- QUERY 4: Average wage gap vs BLS median by company
-- wage_gap = offered_wage - bls_median
-- wage_gap_pct = gap / bls_median * 100
-- ============================================================
-- Q4_WAGE_GAP
SELECT
    h.COMPANY,
    COUNT(*)                                    AS matched_filings,
    ROUND(AVG(h.OFFERED_WAGE_ANNUAL))           AS avg_offered_wage,
    ROUND(AVG(b.A_MEDIAN))                      AS avg_bls_median,
    ROUND(AVG(h.OFFERED_WAGE_ANNUAL - b.A_MEDIAN)) AS avg_wage_gap,
    ROUND(
        AVG((h.OFFERED_WAGE_ANNUAL - b.A_MEDIAN) / b.A_MEDIAN * 100),
        1
    )                                           AS avg_wage_gap_pct
FROM h1b h
JOIN bls_wages b
  ON h.SOC_CODE = b.SOC_CODE_CLEAN
WHERE h.COMPANY IS NOT NULL
  AND b.A_MEDIAN IS NOT NULL
  AND b.A_MEDIAN > 0
GROUP BY h.COMPANY
HAVING COUNT(*) >= 5
ORDER BY avg_wage_gap ASC;

-- ============================================================
-- QUERY 5: Wage gap by SOC occupation title
-- Which tech occupations show the largest gaps overall?
-- ============================================================
-- Q5_GAP_BY_SOC
SELECT
    h.SOC_CODE,
    h.SOC_TITLE,
    COUNT(*)                                    AS filings,
    ROUND(AVG(h.OFFERED_WAGE_ANNUAL))           AS avg_offered_wage,
    ROUND(AVG(b.A_MEDIAN))                      AS bls_median,
    ROUND(AVG(h.OFFERED_WAGE_ANNUAL - b.A_MEDIAN)) AS avg_gap,
    ROUND(
        AVG((h.OFFERED_WAGE_ANNUAL - b.A_MEDIAN) / b.A_MEDIAN * 100),
        1
    )                                           AS avg_gap_pct
FROM h1b h
JOIN bls_wages b
  ON h.SOC_CODE = b.SOC_CODE_CLEAN
WHERE b.A_MEDIAN IS NOT NULL
  AND b.A_MEDIAN > 0
GROUP BY h.SOC_CODE, h.SOC_TITLE
HAVING COUNT(*) >= 10
ORDER BY avg_gap ASC
LIMIT 20;

-- ============================================================
-- QUERY 6: Summary stats for the full dataset
-- ============================================================
-- Q6_SUMMARY
SELECT
    COUNT(*)                                        AS total_filings,
    COUNT(DISTINCT COMPANY)                         AS unique_companies,
    COUNT(DISTINCT SOC_CODE)                        AS unique_soc_codes,
    ROUND(AVG(OFFERED_WAGE_ANNUAL))                 AS overall_avg_wage,
    ROUND(MEDIAN(OFFERED_WAGE_ANNUAL))              AS overall_median_wage,
    MIN(OFFERED_WAGE_ANNUAL)                        AS min_wage,
    MAX(OFFERED_WAGE_ANNUAL)                        AS max_wage
FROM h1b
WHERE OFFERED_WAGE_ANNUAL IS NOT NULL;