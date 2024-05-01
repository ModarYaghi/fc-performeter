import os
from src.config_reader import YAMLConfigReader


# Get the environment variable of the project - fc-performeter
root = os.getenv(
    "FcPerformeter"
)  # NOTE: set the environment variable for the project in the OFFICE


# Main directories in use
config, config_yaml = "config", "config.yaml"
data = "data"
raw = "raw"
ps = "ps"
pt = "pt"
processed = "processed"

data_dir = "0424"


# path to config.yaml
config_file = os.path.join(root, config, config_yaml)
config = YAMLConfigReader(config_file)

# path to raw data - xlsx files
ps_raw_data = os.path.join(root, data, raw, data_dir, ps)
pspw = config.get_passwords_by_directory(ps_raw_data)

pt_raw_data = os.path.join(root, data, raw, data_dir, pt)
ptpw = config.get_passwords_by_directory(pt_raw_data)

processed_data = os.path.join(root, data, processed, data_dir)
unvfvt23 = os.path.join(root, data, processed, "unvfvt23")

# --------------------------------------------------------------
scr_path, scr_sheet = (
    os.path.join(processed_data, "00_" + "ps" + "scr" + "_" + data_dir + ".csv"),
    "Scr",
)

int_path, int_sheet = (
    os.path.join(processed_data, "01_" + "ps" + "int" + "_" + data_dir + ".csv"),
    "Int",
)

gc_path, gc_sheet = (os.path.join(processed_data, "02_" + "ps" + "gc" + "_" + data_dir + ".csv"), "GC")

ic_path, ic_sheet = (os.path.join(processed_data, "03_" + "ps" + "ic" + "_" + data_dir + ".csv"), "IC")

psfua_path, psfua_sheet = (
    os.path.join(processed_data, "04_" + "psfua" + "_" + data_dir + ".csv"),
    "FUA",
)

pei_path, pei_sheet = (
    os.path.join(processed_data, "05_" + "ps" + "pei" + "_" + data_dir + ".csv"),
    "PEI",
)

trw_path, trw_sheet = (
    os.path.join(processed_data, "06_" + "ps" + "trw" + "_" + data_dir + ".csv"),
    "TRW",
)

td_path, td_sheet = (os.path.join(processed_data, "07_" + "ps" + "td" + "_" + data_dir + ".csv"), "TD")

cws_path, cws_sheet = (
    os.path.join(processed_data, "08_" + "ps" + "cws" + "_" + data_dir + ".csv"),
    "CWS",
)

aw_path, aw_sheet = (os.path.join(processed_data, "09_" + "ps" + "aw" + "_" + data_dir + ".csv"), "AW")

psfs_path, psfs_sheet = (
    os.path.join(processed_data, "10_" + "pt" + "psfs" + "_" + data_dir + ".csv"),
    "PSFS",
)

ptint_path, ptint_sheet = (
    os.path.join(processed_data, "11_" + "pt" + "ptint" + "_" + data_dir + ".csv"),
    "PT Int",
)

gpt_path, gpt_sheet = (
    os.path.join(processed_data, "12_" + "pt" + "gpt" + "_" + data_dir + ".csv"),
    "GPT",
)

ipt_path, ipt_sheet = (
    os.path.join(processed_data, "13_" + "pt" + "ipt" + "_" + data_dir + ".csv"),
    "IPT",
)

ptfua_path, ptfua_sheet = (
    os.path.join(processed_data, "14_" + "ptfua" + "_" + data_dir + ".csv"),
    "FUA",
)

data_files = {
    "scr": {"path": os.path.join(processed_data, "00_ps_scr_" + data_dir + ".csv"), "sheet": "Scr"},
    "int": {"path": os.path.join(processed_data, "01_ps_int_" + data_dir + ".csv"), "sheet": "Int"},
    "gc": {"path": os.path.join(processed_data, "02_ps_gc_" + data_dir + ".csv"), "sheet": "GC"},
    "ic": {"path": os.path.join(processed_data, "03_ps_ic_" + data_dir + ".csv"), "sheet": "IC"},
    "psfua": {"path": os.path.join(processed_data, "04_psfua_" + data_dir + ".csv"), "sheet": "FUA"},
    "pei": {"path": os.path.join(processed_data, "05_ps_pei_" + data_dir + ".csv"), "sheet": "PEI"},
    "trw": {"path": os.path.join(processed_data, "06_ps_trw_" + data_dir + ".csv"), "sheet": "TRW"},
    "td": {"path": os.path.join(processed_data, "07_ps_td_" + data_dir + ".csv"), "sheet": "TD"},
    "cws": {"path": os.path.join(processed_data, "08_ps_cws_" + data_dir + ".csv"), "sheet": "CWS"},
    "aw": {"path": os.path.join(processed_data, "09_ps_aw_" + data_dir + ".csv"), "sheet": "AW"},
    "psfs": {"path": os.path.join(processed_data, "10_pt_psfs_" + data_dir + ".csv"), "sheet": "PSFS"},
    "ptint": {"path": os.path.join(processed_data, "11_pt_ptint_" + data_dir + ".csv"), "sheet": "PT Int"},
    "gpt": {"path": os.path.join(processed_data, "12_pt_gpt_" + data_dir + ".csv"), "sheet": "GPT"},
    "ipt": {"path": os.path.join(processed_data, "13_pt_ipt_" + data_dir + ".csv"), "sheet": "IPT"},
    "ptfua": {"path": os.path.join(processed_data, "14_ptfua_" + data_dir + ".csv"), "sheet": "FUA"}
}
