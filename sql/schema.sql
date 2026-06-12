-- schema.sql
-- Creates the two main tables for H-1B wage analysis.
-- Run via src/run_sql.py — do not run this file directly.

-- Drop tables if they already exist (safe to re-run)
DROP TABLE IF EXISTS h1b;
DROP TABLE IF EXISTS bls_wages;

-- H-1B cleaned applications table
CREATE TABLE h1b (
    CASE_NUMBER             VARCHAR,
    CASE_STATUS             VARCHAR,
    EMPLOYER_NAME           VARCHAR,
    JOB_TITLE               VARCHAR,
    SOC_CODE                VARCHAR,
    SOC_TITLE               VARCHAR,
    WAGE_RATE_OF_PAY_FROM   VARCHAR,
    WAGE_UNIT_OF_PAY        VARCHAR,
    PREVAILING_WAGE         VARCHAR,
    PW_UNIT_OF_PAY          VARCHAR,
    PW_WAGE_LEVEL           VARCHAR,
    TOTAL_WORKER_POSITIONS  VARCHAR,
    OFFERED_WAGE_ANNUAL     DOUBLE,
    PREVAILING_WAGE_ANNUAL  DOUBLE,
    COMPANY                 VARCHAR
);

-- BLS national wage benchmarks table
CREATE TABLE bls_wages (
    OCC_CODE        VARCHAR,
    OCC_TITLE       VARCHAR,
    TOT_EMP         VARCHAR,
    H_MEAN          DOUBLE,
    A_MEAN          DOUBLE,
    H_MEDIAN        DOUBLE,
    A_MEDIAN        DOUBLE,
    SOC_CODE_CLEAN  VARCHAR
);