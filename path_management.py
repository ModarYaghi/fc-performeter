import os


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

data_dir = "0324"

# path to config.yaml
config_file = os.path.join(root, config, config_yaml)

# path to raw data - xlsx files
ps_raw_data = os.path.join(root, data, raw, data_dir, ps)
pt_raw_data = os.path.join(root, data, raw, data_dir, pt)
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

