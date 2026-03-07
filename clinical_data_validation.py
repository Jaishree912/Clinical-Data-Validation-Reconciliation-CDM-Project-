import pandas as pd
df = pd.read_excel("\\Users\\realme\\Downloads\\Clinical_Data_Raw_100_Patients.xlsx")
head = df.head()
tail = df.tail() # head & tail to get 1st and last 5 reading
shape = df.shape # shows no.of patients and columns
print(df.columns) # for column's names and type of data
print(df[df.SUBJECT_ID == "SUBJ_001"]) # to print out specific row

df.info() 
sex = df['SEX'].unique() 
df.replace(['', 'None', 'nan', 'Null', 'NONE'], pd.NA)
invalid_age = df[(df['AGE'] < 18) | (df['AGE'] > 100)] 
print(invalid_age) 
date_issue = df[df["DOB"] > df["VISIT_DATE"]] 
duplicate_data = df.SUBJECT_ID.duplicated().sum()
lab = df[(df['LAB_HB'] < 8) | (df['LAB_HB'] > 18)]

query_log = []
for index, row in df.iterrows():
    if pd.isnull(row['SEX']):
        query_log.append([row['SUBJECT_ID'], "SEX missing"])
    if row['AGE'] is not None and (row['AGE'] < 18 or row['AGE'] > 120):
        query_log.append([row['SUBJECT_ID'], "Invalid AGE"])
    if row['DOB'] > row['VISIT_DATE']:
        query_log.append([row['SUBJECT_ID'], "VISIT_DATE before DOB"])

query_df = pd.DataFrame(query_log)
query_df.to_csv("Query list.csv") 
