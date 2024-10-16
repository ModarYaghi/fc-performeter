from src.all_in_one import *
from src.rebuild_dataframe import *

# UNIQUE SCREENING BENEFICIARIES RECORDS

scr_file = path_manager.get_data_file(Category.PS, PSFile.SCR)
scr = get_df(scr_file.path, scr_file.sheet, config_file)
scr = scr.sort_values(by=['sc_s1'])
# unique_scr = scr.drop_duplicates(subset='rid')
rebuilt_scr = rebuild_dataframe(scr, 'rid')

# UNIQUE INTAKE BENEFICIARIES RECORD
intake_s2 = ["rid", "fcid", "service","nt_s2", "family_of_missing", "survivor_of_detention", "primary_torture", "secondary_torture", "sexual_violation_a", "sexual_violation_p", "hrd", "journalist", "wov", "stgbv", "lgbti", "other"]
intake_s3 = ["rid", "fcid", "service","nt_s3", "family_of_missing", "survivor_of_detention", "primary_torture", "secondary_torture", "sexual_violation_a", "sexual_violation_p", "hrd", "journalist", "wov", "stgbv", "lgbti", "other"]
intake_re = ["rid", "fcid", "service","nt_re", "family_of_missing", "survivor_of_detention", "primary_torture", "secondary_torture", "sexual_violation_a", "sexual_violation_p", "hrd", "journalist", "wov", "stgbv", "lgbti", "other"]
int_criteria = ["rid", "family_of_missing", "survivor_of_detention", "primary_torture", "secondary_torture", "sexual_violation_a", "sexual_violation_p", "hrd", "journalist", "wov", "stgbv", "lgbti", "other"]
int_criteria0 = ["family_of_missing", "survivor_of_detention", "primary_torture", "secondary_torture", "sexual_violation_a", "sexual_violation_p", "hrd", "journalist", "wov", "stgbv", "lgbti", "other"]
int_criteria1 = ["fcid", "family_of_missing", "survivor_of_detention", "primary_torture", "secondary_torture", "sexual_violation_a", "sexual_violation_p", "hrd", "journalist", "wov", "stgbv", "lgbti", "other"]

int_file = path_manager.get_data_file(Category.PS, PSFile.PSNT)
intake = get_df(int_file.path, int_file.sheet, config_file)
intake.insert(4, "service", None)
intake = intake.sort_values(by=['nt_s1', 'nt_s2', 'nt_s3', 'nt_re'], ascending=True)
# unique_intake = intake.drop_duplicates(subset='rid', keep='last')
rebuilt_intake = rebuild_dataframe(intake, 'fcid')