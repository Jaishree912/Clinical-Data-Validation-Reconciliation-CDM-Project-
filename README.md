# Clinical Data Validation & Reconciliation — CDM Simulation Project

A Python-based simulation of real-world **Clinical Data Management (CDM)** workflows, built to demonstrate entry-level CDA/CRC competencies including data validation, discrepancy detection, and query generation.

---

## 🎯 Project Objective

This project replicates the data validation tasks performed by a **Clinical Data Associate** during the data cleaning phase of a clinical trial. Using a simulated dataset of 100 subjects, the script applies study-specific validation rules to detect discrepancies, inconsistencies, and missing data — and outputs a structured query log mirroring real EDC query management workflows.

---

## 📋 What This Project Simulates

| CDM Task | Implementation |
|---|---|
| Raw data inspection & profiling | `df.info()`, `describe()`, shape checks |
| Null standardisation | Replacing all null variants with `pd.NA` |
| Duplicate subject detection | `duplicated()` check on SUBJECT_ID |
| Range checks (AGE, LAB_HB) | Protocol-based out-of-range flagging |
| Logic/consistency checks | VISIT_DATE before DOB detection |
| Future date detection | VISIT_DATE vs today's date check |
| Query log generation | Structured CSV output with severity levels |
| Validation summary report | Counts by issue type and severity |

---

## 🔍 Validation Rules Applied

All checks are based on **ICH-E6(R2) GCP** guidelines and standard CDM protocol conventions:

1. **Missing SEX** — Required demographic field; blank values flagged as Major
2. **Invalid AGE** — Protocol eligibility range: 18–100 years; deviations flagged as Critical
3. **VISIT_DATE before DOB** — Logically impossible; flagged as Critical date inconsistency
4. **Future VISIT_DATE** — Cannot record a visit that hasn't occurred; flagged as Major
5. **Out-of-range LAB_HB** — Normal haemoglobin reference: 8–18 g/dL; flagged as Major
6. **Missing VISIT_DATE** — Required for visit reconciliation; flagged as Major

---

## 📁 Repository Structure

```
├── clinical_data_validation.py       # Main validation script
├── Clinical_Data_Raw_100_Patients.xlsx  # Simulated raw clinical dataset (100 subjects)
├── Query_List.csv                    # Output: generated query log
└── README.md
```

---

## ▶️ How to Run

**Requirements:** Python 3.x, pandas, openpyxl

```bash
pip install pandas openpyxl
```

Place `Clinical_Data_Raw_100_Patients.xlsx` in the same directory as the script, then run:

```bash
python clinical_data_validation.py
```

The script will print a step-by-step validation report to the console and save all queries to `Query_List.csv`.

---

## 📤 Sample Output

```
============================================================
STEP 7: VALIDATION SUMMARY
============================================================

  Total Subjects Reviewed  : 100
  Validation Rules Applied : 6
  Total Discrepancies Found: 45
    - Critical             : 9
    - Major                : 36
  Query Log Exported       : Query_List.csv

  Standards Applied: ICH-E6(R2) GCP | 21 CFR Part 11
```

---

## 🛠️ Tools & Standards

- **Language:** Python 3
- **Libraries:** Pandas
- **Regulatory Standards:** ICH-E6(R2) GCP, 21 CFR Part 11
- **CDM Concepts:** Data validation, discrepancy management, query lifecycle, audit readiness
- **EDC Experience:** REDCap (separate simulation project)

---

## 👩‍🔬 About the Author

MSc Biotechnology (CGPA 8.90) | GCP Certified (NIDA CTN) | Clinical Data Management (Udemy) | Python (Pandas, NumPy)

Seeking entry-level roles in **Clinical Data Management**, **Pharmacovigilance**, or **Clinical Research** where domain knowledge and data skills can contribute to trial quality and patient safety.

📧 Connect on [LinkedIn](www.linkedin.com/in/jaishree-mishra-051498167)
