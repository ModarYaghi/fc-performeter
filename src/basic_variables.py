from src.all_in_one import *
from src.rebuild_dataframe import *

# UNIQUE SCREENING BENEFICIARIES RECORDS

# scr_file = path_manager.get_data_file(Category.PS, PSFile.SCR)
# scr = get_df(scr_file.path, scr_file.sheet, config_file)
# scr = scr.sort_values(by=["sc_s1"])
# unique_scr = scr.drop_duplicates(subset='rid')
# rebuilt_scr = rebuild_dataframe(scr, "rid")
#
# int_file = path_manager.get_data_file(Category.PS, PSFile.PSNT)
# intake = get_df(int_file.path, int_file.sheet, config_file)
# intake.insert(4, "service", None)
# intake = intake.sort_values(by=["nt_s1", "nt_s2", "nt_s3", "nt_re"], ascending=True)
# unique_intake = intake.drop_duplicates(subset='rid', keep='last')
# rebuilt_intake = rebuild_dataframe(intake, "fcid")
# rebuilt_intake["fcid"] = rebuilt_intake["fcid"].astype("Int64")


# UNIQUE INTAKE BENEFICIARIES RECORD
intake_s2 = [
    "rid",
    "fcid",
    "service",
    "nt_s2",
    "family_of_missing",
    "survivor_of_detention",
    "primary_torture",
    "secondary_torture",
    "sexual_violation_a",
    "sexual_violation_p",
    "hrd",
    "journalist",
    "wov",
    "stgbv",
    "lgbti",
    "other",
]
intake_s3 = [
    "rid",
    "fcid",
    "service",
    "nt_s3",
    "family_of_missing",
    "survivor_of_detention",
    "primary_torture",
    "secondary_torture",
    "sexual_violation_a",
    "sexual_violation_p",
    "hrd",
    "journalist",
    "wov",
    "stgbv",
    "lgbti",
    "other",
]
intake_re = [
    "rid",
    "fcid",
    "service",
    "nt_re",
    "family_of_missing",
    "survivor_of_detention",
    "primary_torture",
    "secondary_torture",
    "sexual_violation_a",
    "sexual_violation_p",
    "hrd",
    "journalist",
    "wov",
    "stgbv",
    "lgbti",
    "other",
]
int_criteria = [
    "rid",
    "family_of_missing",
    "survivor_of_detention",
    "primary_torture",
    "secondary_torture",
    "sexual_violation_a",
    "sexual_violation_p",
    "hrd",
    "journalist",
    "wov",
    "stgbv",
    "lgbti",
    "other",
]
int_criteria0 = [
    "family_of_missing",
    "survivor_of_detention",
    "primary_torture",
    "secondary_torture",
    "sexual_violation_a",
    "sexual_violation_p",
    "hrd",
    "journalist",
    "wov",
    "stgbv",
    "lgbti",
    "other",
]
int_criteria1 = [
    "fcid",
    "family_of_missing",
    "survivor_of_detention",
    "primary_torture",
    "secondary_torture",
    "sexual_violation_a",
    "sexual_violation_p",
    "hrd",
    "journalist",
    "wov",
    "stgbv",
    "lgbti",
    "other",
]

pss_sheet_path = {
    "screening": (ps_files.SCR.sheet, ps_files.SCR.path),
    "intake": (ps_files.PSNT.sheet, ps_files.PSNT.path),
    "group_counseling": (ps_files.PSG.sheet, ps_files.PSG.path),
    "individual_counseling": (ps_files.PSI.sheet, ps_files.PSI.path),
    "follow_up_assessment": (ps_files.PSFU.sheet, ps_files.PSFU.path),
    "post_earthquake_intervention": (ps_files.PEI.sheet, ps_files.PEI.path),
    "trw": (ps_files.TRW.sheet, ps_files.TRW.path),
    "therapeutic_documentation": (ps_files.TD.sheet, ps_files.TD.path),
    "creative_workshop": (ps_files.CWS.sheet, ps_files.CWS.path),
    "awareness_workshop": (ps_files.AWW.sheet, ps_files.AWW.path),
}

pt_sheet_path = {
    "psfs": (pt_files.PSFS.sheet, pt_files.PSFS.path),
    "pt_intake": (pt_files.PTNT.sheet, pt_files.PTNT.path),
    "pt_group": (pt_files.PTG.sheet, pt_files.PTG.path),
    "pt_individual": (pt_files.PTI.sheet, pt_files.PTI.path),
    "pt_fua": (pt_files.PTFU.sheet, pt_files.PTFU.path),
}

# --------------------------Working Period------------------------------------
START = "2025-01-01"
END = "2025-01-31"
# ----------------------------------------------------------------------------
