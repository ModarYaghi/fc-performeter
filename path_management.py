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

data_dir = "0124"

# path to config.yaml
config_file = os.path.join(root, config, config_yaml)

# path to raw data - xlsx files
ps_raw_data = os.path.join(root, data, raw, data_dir, ps)
pt_raw_data = os.path.join(root, data, raw, data_dir, pt)
processed_data = os.path.join(root, data, processed, data_dir)

# --------------------------------------------------------------
scr_path, scr_sheet = (
    os.path.join(processed_data, "ps" + "scr" + "_" + data_dir + ".csv"),
    "Scr",
)

int_path, int_sheet = (
    os.path.join(processed_data, "ps" + "int" + "_" + data_dir + ".csv"),
    "Int",
)

gc_path, gc_sheet = (os.path.join(processed_data, "ps" + "gc" + "_" + data_dir + ".csv"), "GC")

ic_path, ic_sheet = (os.path.join(processed_data, "ps" + "ic" + "_" + data_dir + ".csv"), "IC")

psfua_path, psfua_sheet = (
    os.path.join(processed_data, "psfua" + "_" + data_dir + ".csv"),
    "FUA",
)

pei_path, pei_sheet = (
    os.path.join(processed_data, "ps" + "pei" + "_" + data_dir + ".csv"),
    "PEI",
)

td_path, td_sheet = (os.path.join(processed_data, "ps" + "td" + "_" + data_dir + ".csv"), "TD")

cws_path, cws_sheet = (
    os.path.join(processed_data, "cws" + "_" + data_dir + ".csv"),
    "CWS",
)

trw_path, trw_sheet = (
    os.path.join(processed_data, "trw" + "_" + data_dir + ".csv"),
    "TRW",
)

aw_path, aw_sheet = (os.path.join(processed_data, "aw" + "_" + data_dir + ".csv"), "AW")

psfs_path, psfs_sheet = (
    os.path.join(processed_data, "psfs" + "_" + data_dir + ".csv"),
    "PSFS",
)

ptint_path, ptint_sheet = (
    os.path.join(processed_data, "pt" + "ptint" + "_" + data_dir + ".csv"),
    "PT Int",
)

gpt_path, gpt_sheet = (
    os.path.join(processed_data, "pt" + "gpt" + "_" + data_dir + ".csv"),
    "GPT",
)

ipt_path, ipt_sheet = (
    os.path.join(processed_data, "pt" + "ipt" + "_" + data_dir + ".csv"),
    "IPT",
)

ptfua_path, ptfua_sheet = (
    os.path.join(processed_data, "pt" + "ptfua" + "_" + data_dir + ".csv"),
    "FUA",
)
