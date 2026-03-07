# =============================================================================
# Clinical Data Validation & Reconciliation — CDM Simulation Project
# Author: Jaishree
# Description: Simulates entry-level Clinical Data Associate tasks including
#              data inspection, validation, logic checks, and query generation
#              based on ICH-E6(R2) GCP guidelines.
# Tools: Python 3, Pandas
# =============================================================================

import pandas as pd
import os

# =============================================================================
# SECTION 1: DATA LOADING & INITIAL INSPECTION
# =============================================================================

# Load the raw clinical dataset (place file in same folder as this script)
file_path = "Clinical_Data_Raw_100_Patients.xlsx"

if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"Dataset not found: '{file_path}'. "
        "Please ensure the Excel file is in the same directory as this script."
    )

df = pd.read_excel(file_path)

print("=" * 60)
print("STEP 1: INITIAL DATA INSPECTION")
print("=" * 60)
print(f"\nDataset Shape: {df.shape[0]} subjects, {df.shape[1]} columns")
print(f"\nColumn Names & Data Types:\n{df.dtypes}")
print(f"\nFirst 5 Records:\n{df.head()}")
print(f"\nDescriptive Statistics:\n{df.describe(include='all')}")


# =============================================================================
# SECTION 2: DATA STANDARDISATION
# Replacing common null representations with proper NaN values
# This ensures consistent missing data handling across the dataset
# per data cleaning standards in clinical data management
# =============================================================================

print("\n" + "=" * 60)
print("STEP 2: DATA STANDARDISATION (NULL HANDLING)")
print("=" * 60)

# Standardise all known null-like values to NaN
null_representations = ['', ' ', 'None', 'none', 'nan', 'NaN', 'Null',
                        'NULL', 'NONE', 'N/A', 'n/a', 'NA', pd.NA]
df.replace(null_representations, pd.NA, inplace=True)

# Parse date columns to datetime for accurate logic checks
# Required for DOB vs VISIT_DATE consistency validation
for col in ['DOB', 'VISIT_DATE']:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')

print("Null standardisation complete. Date columns parsed.")


# =============================================================================
# SECTION 3: MISSING DATA ASSESSMENT
# Identifying completeness issues across all fields
# =============================================================================

print("\n" + "=" * 60)
print("STEP 3: MISSING DATA ASSESSMENT")
print("=" * 60)

missing_summary = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_report = pd.DataFrame({
    'Missing Count': missing_summary,
    'Missing %': missing_pct
})
missing_report = missing_report[missing_report['Missing Count'] > 0]

if missing_report.empty:
    print("No missing values detected.")
else:
    print(f"\nMissing Data Summary:\n{missing_report}")


# =============================================================================
# SECTION 4: DUPLICATE SUBJECT CHECK
# Each Subject ID must be unique — duplicates indicate data entry errors
# or accidental double enrollment, both critical GCP violations
# =============================================================================

print("\n" + "=" * 60)
print("STEP 4: DUPLICATE SUBJECT ID CHECK")
print("=" * 60)

duplicate_count = df['SUBJECT_ID'].duplicated().sum()
print(f"Duplicate Subject IDs found: {duplicate_count}")

if duplicate_count > 0:
    print(df[df['SUBJECT_ID'].duplicated(keep=False)][['SUBJECT_ID']])


# =============================================================================
# SECTION 5: VALIDATION RULES & DISCREPANCY DETECTION
# Applying study-specific validation rules based on protocol requirements
# Each rule corresponds to a real-world CDM data validation check
# =============================================================================

print("\n" + "=" * 60)
print("STEP 5: DATA VALIDATION CHECKS")
print("=" * 60)

query_log = []

# ── Rule 1: Missing SEX ──────────────────────────────────────────────────────
# SEX is a required demographic field; missing values require data clarification
if 'SEX' in df.columns:
    missing_sex = df[df['SEX'].isnull()]
    for _, row in missing_sex.iterrows():
        query_log.append({
            'SUBJECT_ID': row['SUBJECT_ID'],
            'Field': 'SEX',
            'Issue': 'Missing Value',
            'Details': 'SEX field is blank — mandatory demographic variable',
            'Severity': 'Major'
        })
    print(f"Rule 1 — Missing SEX: {len(missing_sex)} issue(s) found")

# ── Rule 2: Invalid AGE Range ────────────────────────────────────────────────
# Per ICH-E6 and study protocol, eligible subjects must be aged 18–100
# Values outside this range indicate entry errors or protocol deviations
if 'AGE' in df.columns:
    invalid_age = df[
        df['AGE'].notna() & ((df['AGE'] < 18) | (df['AGE'] > 100))
    ]
    for _, row in invalid_age.iterrows():
        query_log.append({
            'SUBJECT_ID': row['SUBJECT_ID'],
            'Field': 'AGE',
            'Issue': 'Out-of-Range Value',
            'Details': f"AGE = {row['AGE']} — expected range: 18 to 100 years",
            'Severity': 'Critical'
        })
    print(f"Rule 2 — Invalid AGE: {len(invalid_age)} issue(s) found")

# ── Rule 3: VISIT_DATE before DOB ────────────────────────────────────────────
# Logically impossible: a subject cannot attend a visit before being born
# This typically indicates a date entry or format error
if 'DOB' in df.columns and 'VISIT_DATE' in df.columns:
    date_inconsistency = df[
        df['DOB'].notna() & df['VISIT_DATE'].notna() &
        (df['VISIT_DATE'] < df['DOB'])
    ]
    for _, row in date_inconsistency.iterrows():
        query_log.append({
            'SUBJECT_ID': row['SUBJECT_ID'],
            'Field': 'VISIT_DATE / DOB',
            'Issue': 'Logical Inconsistency',
            'Details': f"VISIT_DATE ({row['VISIT_DATE'].date()}) is before DOB ({row['DOB'].date()})",
            'Severity': 'Critical'
        })
    print(f"Rule 3 — VISIT_DATE before DOB: {len(date_inconsistency)} issue(s) found")

# ── Rule 4: Future VISIT_DATE ────────────────────────────────────────────────
# Visit dates should not be recorded in the future — flags data entry errors
if 'VISIT_DATE' in df.columns:
    today = pd.Timestamp.today()
    future_dates = df[df['VISIT_DATE'].notna() & (df['VISIT_DATE'] > today)]
    for _, row in future_dates.iterrows():
        query_log.append({
            'SUBJECT_ID': row['SUBJECT_ID'],
            'Field': 'VISIT_DATE',
            'Issue': 'Future Date',
            'Details': f"VISIT_DATE ({row['VISIT_DATE'].date()}) is in the future",
            'Severity': 'Major'
        })
    print(f"Rule 4 — Future VISIT_DATE: {len(future_dates)} issue(s) found")

# ── Rule 5: Out-of-Range Haemoglobin (LAB_HB) ────────────────────────────────
# Normal haemoglobin reference range: 8–18 g/dL
# Values outside this range may indicate lab errors or critical safety signals
if 'LAB_HB' in df.columns:
    invalid_hb = df[
        df['LAB_HB'].notna() & ((df['LAB_HB'] < 8) | (df['LAB_HB'] > 18))
    ]
    for _, row in invalid_hb.iterrows():
        query_log.append({
            'SUBJECT_ID': row['SUBJECT_ID'],
            'Field': 'LAB_HB',
            'Issue': 'Out-of-Range Value',
            'Details': f"LAB_HB = {row['LAB_HB']} g/dL — expected range: 8 to 18 g/dL",
            'Severity': 'Major'
        })
    print(f"Rule 5 — Invalid LAB_HB: {len(invalid_hb)} issue(s) found")

# ── Rule 6: Missing VISIT_DATE ───────────────────────────────────────────────
if 'VISIT_DATE' in df.columns:
    missing_visit = df[df['VISIT_DATE'].isnull()]
    for _, row in missing_visit.iterrows():
        query_log.append({
            'SUBJECT_ID': row['SUBJECT_ID'],
            'Field': 'VISIT_DATE',
            'Issue': 'Missing Value',
            'Details': 'VISIT_DATE is blank — required for visit reconciliation',
            'Severity': 'Major'
        })
    print(f"Rule 6 — Missing VISIT_DATE: {len(missing_visit)} issue(s) found")


# =============================================================================
# SECTION 6: QUERY LOG GENERATION
# Exporting all identified discrepancies as a structured query listing
# This mirrors the real-world process of raising queries to site personnel
# =============================================================================

print("\n" + "=" * 60)
print("STEP 6: QUERY LOG GENERATION")
print("=" * 60)

if query_log:
    query_df = pd.DataFrame(query_log)
    query_df.index = query_df.index + 1  # Query numbers start from 1
    query_df.index.name = 'Query_No'

    output_file = "Query_List.csv"
    query_df.to_csv(output_file)

    print(f"\nTotal Queries Raised: {len(query_df)}")
    print(f"\nQuery Breakdown by Issue Type:\n{query_df['Issue'].value_counts()}")
    print(f"\nQuery Breakdown by Severity:\n{query_df['Severity'].value_counts()}")
    print(f"\nQuery log saved to: '{output_file}'")
    print(f"\nSample Queries:\n{query_df.head(10).to_string()}")
else:
    print("No discrepancies found. Dataset appears clean.")


# =============================================================================
# SECTION 7: VALIDATION SUMMARY REPORT
# =============================================================================

print("\n" + "=" * 60)
print("STEP 7: VALIDATION SUMMARY")
print("=" * 60)

total_checks = 6
total_subjects = len(df)
total_queries = len(query_log) if query_log else 0
critical = sum(1 for q in query_log if q['Severity'] == 'Critical')
major = sum(1 for q in query_log if q['Severity'] == 'Major')

print(f"""
  Total Subjects Reviewed  : {total_subjects}
  Validation Rules Applied : {total_checks}
  Total Discrepancies Found: {total_queries}
    - Critical             : {critical}
    - Major                : {major}
  Query Log Exported       : Query_List.csv

  Standards Applied: ICH-E6(R2) GCP | 21 CFR Part 11
""")
print("=" * 60)
print("Validation complete.")
print("=" * 60)
