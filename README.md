# Clinical-Data-Validation-Reconciliation-CDM-Project-
Project Overview
This project demonstrates a real-world Clinical Data Management (CDM) workflow using Python (Pandas) to inspect, clean, and validate clinical trial–like data. 
The objective is to simulate entry-level Clinical Data Associate / Coordinator tasks such as identifying data discrepancies, performing logic checks, and generating query listings from raw datasets. The dataset contains 100 subjects with demographic and visit-level information, intentionally including missing values, out-of-range values, and logical inconsistencies to mirror real clinical data.
#Key Pandas Functions Used:
read_excel()
head(), info(), describe()
isna(), notna()
Boolean filtering with &, |, ~
to_datetime()
duplicated()

#Key CDM Concepts Demonstrated: 
Clinical data inspection & cleaning
Data validation rules
Logic and consistency checks
Query identification and discrepancy management
Handling real-world data issues from Excel sources

#Tools & Technologies:
Python 3
Pandas
Excel (source data)
