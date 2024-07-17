import os
from enum import Enum, auto
from pathlib import Path
from pydantic import BaseModel, ValidationError
from src.config_reader import YAMLConfigReader

class Category(Enum):
    PS = auto()
    PT = auto()


class PSFile(Enum):
    SCR = auto()
    PSNT = auto()
    PSG = auto()
    PSI = auto()
    PSFU = auto()
    PEI = auto()
    TRW = auto()
    TD = auto()
    CDW = auto() 
    AWW = auto()


class PTFile(Enum):
    PSFS = auto()
    PTNT = auto()
    PTG = auto()
    PTI = auto()
    PTFU = auto()


class DataFile(BaseModel):
    path: str
    sheet: str


class PathManger:
    def __init__(self, root: str, data_dir: str, config_file: str):
        self.root = root
        self.data_dir = data_dir
        self.config = YAMLConfigReader(config_file)

        self.ps_raw_data = self.get_raw_data_path("ps")
        self.pspw = self.config.get_passwords_by_directory(self.ps_raw_data)

        self.pt_raw_data = self.get_raw_data_path("pt")
        self.ptpw = self.config.get_passwords_by_directory(self.pt_raw_data)

        self.processed_data = self.get_processed_data_path()
        self.unvfvt24 = self.get_unvfvt24_path()

        self.data_files = self.initialize_data_files()

    def get_raw_data_path(self, subdir: str) -> str:
        return os.path.join(self.root, "data", "raw", self.data_dir, subdir)

    def get_processed_data_path(self) -> str:
        return os.path.join(self.root, "data", "processed", self.data_dir)

    def get_unvfvt24_path(self) -> str:
        return os.path.join(self.root, "data", "processed", "unvfvt24")

    def initialize_data_files(self):
        return {
                Category.PS: {
                    PSFile.SCR: DataFile(
                        path=os.path.join(self.processed_data, f"00_psscr_{self.data_dir}.csv"),
                        sheet="Scr"
                        ),
                    PSFile.PSNT: DataFile(
                        path=os.path.join(self.processed_data, f"01_psint_{self.data_dir}.csv"),
                        sheet="Int",
                        ),
                    PSFile.PSG: DataFile(
                        path=os.path.join(self.processed_data, f"02_psgc_{self.data_dir}.csv"),
                        sheet="GC",
                        ),
                    PSFile.PSI: DataFile(
                        path=os.path.join(self.processed_data, f"03_psic_{self.data_dir}.csv"),
                        sheet="IC",
                        ),
                    PSFile.PSFU: DataFile(
                        path=os.path.join(self.processed_data, f"04_psfua_{self.data_dir}.csv"),
                        sheet="FUA",
                        ),
                    PSFile.PEI: DataFile(
                        path=os.path.join(self.processed_data, f"05_pspei_{self.data_dir}.csv"),
                        sheet="PEI",
                        ),
                    PSFile.TRW: DataFile(
                        path=os.path.join(self.processed_data, f"06_pstrw_{self.data_dir}.csv"),
                        sheet="TRW",
                        ),
                    PSFile.TD: DataFile(
                        path=os.path.join(self.processed_data, f"07_pstd_{self.data_dir}.csv"),
                        sheet="TD",
                        ),
                    PSFile.CDW: DataFile(
                        path=os.path.join(self.processed_data, f"08_pscws_{self.data_dir}.csv"),
                        sheet="cws",
                        ),
                    PSFile.AWW: DataFile(
                        path=os.path.join(self.processed_data, f"09_psaw_{self.data_dir}.csv"),
                        sheet="AW",
                        ),
                    },
                Category.PT: {
                    PTFile.PSFS: DataFile(
                        path=os.path.join(self.processed_data, f"10_ptpsfs_{self.data_dir}.csv"),
                        sheet="PSFS",
                        ),
                    PTFile.PTNT: DataFile(
                        path=os.path.join(self.processed_data, f"11_ptint_{self.data_dir}.csv"),
                        sheet="PTInt",
                        ),
                    PTFile.PTG: DataFile(
                        path=os.path.join(self.processed_data, f"12_ptgpt_{self.data_dir}.csv"),
                        sheet="GPT",
                        ),
                    PTFile.PTI: DataFile(
                        path=os.path.join(self.processed_data, f"13_ptipt_{self.data_dir}.csv"),
                        sheet="IPT",
                        ),
                    PTFile.PTFU: DataFile(
                        path=os.path.join(self.processed_data, f"14_ptfua_{self.data_dir}.csv"),
                        sheet="FUA",
                        ),
                    },
                }

   
    def get_data_file(self, category: Category, file_type: Enum) -> DataFile:
        return self.data_files[category][file_type]


# Usage Example
root = os.getenv("FcPerformeter")
data_dir = "0624"
config_file = os.path.join(root, "config", "config.yaml")

path_manager = PathManger(root, data_dir, config_file)

# ---------------------------------------------------------------------

# Get the environment variable of the project - fc-performeter
# )  # NOTE: set the environment variable for the project in the OFFICE


# # Main directories in use
# config, config_yaml = "config", "config.yaml"
# data = "data"
# raw = "raw"
# ps = "ps"
# pt = "pt"
# processed = "processed"

# data_dir = "0624"


# # path to config.yaml
# config_file = os.path.join(root, config, config_yaml)
# config = YAMLConfigReader(config_file)

# # path to raw data - xlsx files
# ps_raw_data = os.path.join(root, data, raw, data_dir, ps)
# pspw = config.get_passwords_by_directory(ps_raw_data)

# pt_raw_data = os.path.join(root, data, raw, data_dir, pt)
# ptpw = config.get_passwords_by_directory(pt_raw_data)

# processed_data = os.path.join(root, data, processed, data_dir)
# unvfvt24 = os.path.join(root, data, processed, "unvfvt24")

# # --------------------------------------------------------------
# scr_path, scr_sheet = (
#     os.path.join(processed_data, "00_" + "ps" + "scr" + "_" + data_dir + ".csv"),
#     "Scr",
# )

# int_path, int_sheet = (
#     os.path.join(processed_data, "01_" + "ps" + "int" + "_" + data_dir + ".csv"),
#     "Int",
# )

# gc_path, gc_sheet = (os.path.join(processed_data, "02_" + "ps" + "gc" + "_" + data_dir + ".csv"), "GC")

# ic_path, ic_sheet = (os.path.join(processed_data, "03_" + "ps" + "ic" + "_" + data_dir + ".csv"), "IC")

# psfua_path, psfua_sheet = (
#     os.path.join(processed_data, "04_" + "psfua" + "_" + data_dir + ".csv"),
#     "FUA",
# )

# pei_path, pei_sheet = (
#     os.path.join(processed_data, "05_" + "ps" + "pei" + "_" + data_dir + ".csv"),
#     "PEI",
# )

# trw_path, trw_sheet = (
#     os.path.join(processed_data, "06_" + "ps" + "trw" + "_" + data_dir + ".csv"),
#     "TRW",
# )

# td_path, td_sheet = (os.path.join(processed_data, "07_" + "ps" + "td" + "_" + data_dir + ".csv"), "TD")

# cws_path, cws_sheet = (
#     os.path.join(processed_data, "08_" + "ps" + "cws" + "_" + data_dir + ".csv"),
#     "CWS",
# )

# aw_path, aw_sheet = (os.path.join(processed_data, "09_" + "ps" + "aw" + "_" + data_dir + ".csv"), "AW")

# psfs_path, psfs_sheet = (
#     os.path.join(processed_data, "10_" + "pt" + "psfs" + "_" + data_dir + ".csv"),
#     "PSFS",
# )

# ptint_path, ptint_sheet = (
#     os.path.join(processed_data, "11_" + "pt" + "int" + "_" + data_dir + ".csv"),
#     "PTInt",
# )

# gpt_path, gpt_sheet = (
#     os.path.join(processed_data, "12_" + "pt" + "gpt" + "_" + data_dir + ".csv"),
#     "GPT",
# )

# ipt_path, ipt_sheet = (
#     os.path.join(processed_data, "13_" + "pt" + "ipt" + "_" + data_dir + ".csv"),
#     "IPT",
# )

# ptfua_path, ptfua_sheet = (
#     os.path.join(processed_data, "14_" + "pt" + "fua" + "_" + data_dir + ".csv"),
#     "FUA",
# )


