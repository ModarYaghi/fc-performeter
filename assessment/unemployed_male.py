from src.all_in_one import *
from src.analysis_functions import *
from src.basic_variables import *

os.getcwd()

men_unemployed_columns = [
    "ADMINNUM",
    "REINTAKDATE",
    "PSCNT",
    "SESDATE",
    "FUSESDATE",
    "CNTFIRSTNAME",
    "GENDER",
    "AGE",
    "YOB",
    "WORKNOW",
    "WORKAREA",
    "WORKAREACAT",
    "WORKAREAOTH",
]

adminnum_mapping = {0: "Intake", 3: "3-month", 6: "6-month", 12: "12-month"}

gender_mapping = {1: "man", 2: "woman", 3: "other"}

worknow_mapping = {
    1: "Employed (working at a job)",
    2: "Self-employed (work that could include own business, farming, etc)",
    3: "Student",
    4: "Retired or pensioner",
    5: "Military",
    6: "Unemployed and looking for work",
    7: "Cannot work due to permanent disability or illness",
    8: "Cannot work due to legal status",
    9: "None of the above (includes staying at home by choice to take care of children or household)",
}

workareacat_mapping = {
    1: "Farming",
    2: "Fishing, livestock, forestry",
    3: "Industry (manufacturing finished goods)",
    4: "Commerce (buying or selling goods and services)",
    5: "Construction",
    6: "Education",
    7: "Services (not making products but providing time, knowledge, or skills includes health sector)",
    8: "Public sector (government or politics)",
    10: "Other",
}


df = pd.read_excel(r"assessment/221024.xlsx")
df = df[men_unemployed_columns]

df["SESDATE"] = df["SESDATE"].str.replace("/", "-")
df["FUSESDATE"] = df["FUSESDATE"].str.replace("/", "-")

# df["REINTAKDATE"] = pd.to_datetime(
# df["REINTAKDATE"], format="%d-%m-%Y", errors="coerce"
# )

# df["SESDATE"] = pd.to_datetime(df["SESDATE"], format="%d-%m-%Y", errors="coerce")
# df["FUSESDATE"] = pd.to_datetime(df["FUSESDATE"], format="%d-%m-%Y", errors="coerce")

df["AGE"] = df["AGE"].astype("Int64")
df["YOB"] = df["YOB"].astype("Int64")

df["ADMINNUM"] = df["ADMINNUM"].replace(adminnum_mapping)
df["GENDER"] = df["GENDER"].replace(gender_mapping)
df["WORKNOW"] = df["WORKNOW"].replace(worknow_mapping)
df["WORKAREACAT"] = df["WORKAREACAT"].replace(workareacat_mapping)
