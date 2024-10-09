# import os
# from enum import Enum, auto
#
# # from pathlib import Path
# from pydantic import BaseModel
#
# from src.config_reader import YAMLConfigReader
#
#
# class Category(Enum):
#     PS = auto()
#     PT = auto()
#
#
# class PSFile(Enum):
#     SCR = auto()
#     PSNT = auto()
#     PSG = auto()
#     PSI = auto()
#     PSFU = auto()
#     PEI = auto()
#     TRW = auto()
#     TD = auto()
#     CDW = auto()
#     AWW = auto()
#
#
# class PTFile(Enum):
#     PSFS = auto()
#     PTNT = auto()
#     PTG = auto()
#     PTI = auto()
#     PTFU = auto()
#
#
# class DataFile(BaseModel):
#     path: str
#     sheet: str
#
#
# class PathManger:
#     def __init__(self, root: str, data_dir: str, config_file: str):
#         self.root = root
#         self.data_dir = data_dir
#         self.config = YAMLConfigReader(config_file)
#
#         self.ps_raw_data = self.get_raw_data_path("ps")
#         self.pspw = self.config.get_passwords_by_directory(self.ps_raw_data)
#
#         self.pt_raw_data = self.get_raw_data_path("pt")
#         self.ptpw = self.config.get_passwords_by_directory(self.pt_raw_data)
#
#         self.processed_data = self.get_processed_data_path()
#         self.unvfvt24 = self.get_unvfvt24_path()
#
#         self.data_files = self.initialize_data_files()
#
#     def get_raw_data_path(self, subdir: str) -> str:
#         return os.path.join(self.root, "data", "raw", self.data_dir, subdir)
#
#     def get_processed_data_path(self) -> str:
#         return os.path.join(self.root, "data", "processed", self.data_dir)
#
#     def get_unvfvt24_path(self) -> str:
#         return os.path.join(self.root, "data", "processed", "unvfvt24")
#
#     def initialize_data_files(self):
#         return {
#             Category.PS: {
#                 PSFile.SCR: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"00_psscr_{self.data_dir}.csv"
#                     ),
#                     sheet="Scr",
#                 ),
#                 PSFile.PSNT: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"01_psint_{self.data_dir}.csv"
#                     ),
#                     sheet="Int",
#                 ),
#                 PSFile.PSG: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"02_psgc_{self.data_dir}.csv"
#                     ),
#                     sheet="GC",
#                 ),
#                 PSFile.PSI: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"03_psic_{self.data_dir}.csv"
#                     ),
#                     sheet="IC",
#                 ),
#                 PSFile.PSFU: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"04_psfua_{self.data_dir}.csv"
#                     ),
#                     sheet="FUA",
#                 ),
#                 PSFile.PEI: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"05_pspei_{self.data_dir}.csv"
#                     ),
#                     sheet="PEI",
#                 ),
#                 PSFile.TRW: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"06_pstrw_{self.data_dir}.csv"
#                     ),
#                     sheet="TRW",
#                 ),
#                 PSFile.TD: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"07_pstd_{self.data_dir}.csv"
#                     ),
#                     sheet="TD",
#                 ),
#                 PSFile.CDW: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"08_pscws_{self.data_dir}.csv"
#                     ),
#                     sheet="cws",
#                 ),
#                 PSFile.AWW: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"09_psaw_{self.data_dir}.csv"
#                     ),
#                     sheet="AW",
#                 ),
#             },
#             Category.PT: {
#                 PTFile.PSFS: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"10_ptpsfs_{self.data_dir}.csv"
#                     ),
#                     sheet="PSFS",
#                 ),
#                 PTFile.PTNT: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"11_ptint_{self.data_dir}.csv"
#                     ),
#                     sheet="PTInt",
#                 ),
#                 PTFile.PTG: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"12_ptgpt_{self.data_dir}.csv"
#                     ),
#                     sheet="GPT",
#                 ),
#                 PTFile.PTI: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"13_ptipt_{self.data_dir}.csv"
#                     ),
#                     sheet="IPT",
#                 ),
#                 PTFile.PTFU: DataFile(
#                     path=os.path.join(
#                         self.processed_data, f"14_ptfua_{self.data_dir}.csv"
#                     ),
#                     sheet="FUA",
#                 ),
#             },
#         }
#
#     def get_data_file(self, category: Category, file_type: Enum) -> DataFile:
#         return self.data_files[category][file_type]
#
#
# # Usage Example
# root = os.getenv("FcPerformeter")
# data_dir = "0924"
# config_file = os.path.join(root, "config", "config.yaml")
#
# path_manager = PathManger(root, data_dir, config_file)

from enum import Enum, auto
import os
from dataclasses import dataclass
import logging

# Constants for Directory Paths
DATA_RAW_DIR = "data/raw"
DATA_PROCESSED_DIR = "data/processed"
UNVFVT24_DIR = "unvfvt24"

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@dataclass
class DataFile:
    """
    Represents a data file with its path and sheet name.

    Attributes:
        path (str): The file path of the data file.
        sheet (str): The sheet name within the data file.
    """
    path: str
    sheet: str

class Category(Enum):
    """
    Enumeration for data categories.

    Attributes:
        PS (auto): Represents the PS category.
        PT (auto): Represents the PT category.
    """
    PS = auto()
    PT = auto()

class PSFile(Enum):
    """
    Enumeration for PS file types with filename prefix and sheet name.

    Attributes:
        SCR (tuple): Screening file.
        PSNT (tuple): Intake file.
        PSG (tuple): General Counseling file.
        PSI (tuple): Individual Counseling file.
        PSFU (tuple): Follow-Up Assessment file.
        PEI (tuple): Psychoeducation Intervention file.
        TRW (tuple): Trauma Resilience Workshop file.
        TD (tuple): Therapeutic Documentation file.
        CDW (tuple): Community Workshop file.
        AWW (tuple): Awareness Workshop file.
    """
    SCR = ("00_psscr", "Scr")
    PSNT = ("01_psint", "Int")
    PSG = ("02_psgc", "GC")
    PSI = ("03_psic", "IC")
    PSFU = ("04_psfua", "FUA")
    PEI = ("05_pspei", "PEI")
    TRW = ("06_pstrw", "TRW")
    TD = ("07_pstd", "TD")
    CDW = ("08_pscws", "cws")
    AWW = ("09_psaw", "AW")

    def __init__(self, filename_prefix, sheet):
        self.filename_prefix = filename_prefix
        self.sheet = sheet

class PTFile(Enum):
    """
    Enumeration for PT file types with filename prefix and sheet name.

    Attributes:
        PSFS (tuple): Psycho-Social Follow-Up Screening file.
        PTNT (tuple): Intake file for PT.
        PTG (tuple): General Group Therapy file.
        PTI (tuple): Individual Therapy file.
        PTFU (tuple): Follow-Up Assessment file for PT.
    """
    PSFS = ("10_ptpsfs", "PSFS")
    PTNT = ("11_ptint", "PTInt")
    PTG = ("12_ptgpt", "GPT")
    PTI = ("13_ptipt", "IPT")
    PTFU = ("14_ptfua", "FUA")

    def __init__(self, filename_prefix, sheet):
        self.filename_prefix = filename_prefix
        self.sheet = sheet

class PathManager:
    """
    Manages paths for raw and processed data files.

    Attributes:
        root (str): The root directory path.
        data_dir (str): The directory for storing data.
        ps_raw_data (str): Path to raw PS data.
        pt_raw_data (str): Path to raw PT data.
        processed_data (str): Path to processed data.
        unvfvt24 (str): Path to UNVFVT24 data.
        data_files (dict): Dictionary of data files categorized by category and file type.
    """
    def __init__(self, root: str, data_dir: str, config_file: str):
        """
        Initializes the PathManager with root directory, data directory, and configuration file.

        Args:
            root (str): The root directory path.
            data_dir (str): The data directory name.
            config_file (str): The configuration file path.
        """
        if not root:
            raise EnvironmentError("FcPerformeter environment variable is not set.")

        self.root = root
        self.data_dir = data_dir
        # Example config reader initialization - replace with your implementation
        # self.config = YAMLConfigReader(config_file)

        # Defining paths
        self.ps_raw_data = self.get_raw_data_path("ps")
        self.pt_raw_data = self.get_raw_data_path("pt")
        self.processed_data = self.get_processed_data_path()
        self.unvfvt24 = self.get_unvfvt24_path()

        # Initialize data files dynamically
        self.data_files = self.initialize_data_files()

    def get_raw_data_path(self, subdir: str) -> str:
        """
        Constructs the path to the raw data directory for the given subdirectory.

        Args:
            subdir (str): The subdirectory name (e.g., 'ps' or 'pt').

        Returns:
            str: The path to the raw data directory.
        """
        return os.path.join(self.root, DATA_RAW_DIR, self.data_dir, subdir)

    def get_processed_data_path(self) -> str:
        """
        Constructs the path to the processed data directory.

        Returns:
            str: The path to the processed data directory.
        """
        return os.path.join(self.root, DATA_PROCESSED_DIR, self.data_dir)

    def get_unvfvt24_path(self) -> str:
        """
        Constructs the path to the UNVFVT24 processed data directory.

        Returns:
            str: The path to the UNVFVT24 processed data directory.
        """
        return os.path.join(self.root, DATA_PROCESSED_DIR, UNVFVT24_DIR)

    def initialize_data_files(self):
        """
        Initializes the data files dictionary for each category and file type.

        Returns:
            dict: A dictionary containing data files categorized by Category and file type.
        """
        data_files = {Category.PS: {}, Category.PT: {}}

        # Initialize PS Files
        for ps_file in PSFile:
            data_files[Category.PS][ps_file] = DataFile(
                path=os.path.join(self.processed_data, f"{ps_file.filename_prefix}_{self.data_dir}.csv"),
                sheet=ps_file.sheet
            )
            logging.info(f"Initialized PS data file: {ps_file.filename_prefix}_{self.data_dir}.csv")

        # Initialize PT Files
        for pt_file in PTFile:
            data_files[Category.PT][pt_file] = DataFile(
                path=os.path.join(self.processed_data, f"{pt_file.filename_prefix}_{self.data_dir}.csv"),
                sheet=pt_file.sheet
            )
            logging.info(f"Initialized PT data file: {pt_file.filename_prefix}_{self.data_dir}.csv")

        return data_files

    def get_data_file(self, category: Category, file_type: Enum) -> DataFile:
        """
        Retrieves the data file for a given category and file type.

        Args:
            category (Category): The category of the data (PS or PT).
            file_type (Enum): The file type (PSFile or PTFile).

        Returns:
            DataFile: The corresponding DataFile object.

        Raises:
            ValueError: If the category or file type is invalid.
        """
        try:
            data_file = self.data_files[category][file_type]
            logging.info(f"Retrieved data file: {data_file.path}")
            return data_file
        except KeyError:
            logging.error(f"Invalid category or file type: {category}, {file_type}")
            raise ValueError(f"Invalid category or file type: {category}, {file_type}")

    def get_all_file_paths(self) -> dict:
        """
        Retrieves all file paths managed by the PathManager.

        Returns:
            dict: A dictionary of all file paths categorized by Category and file type.
        """
        all_file_paths = {}
        for category, files in self.data_files.items():
            all_file_paths[category] = {file_type: data_file.path for file_type, data_file in files.items()}
        logging.info("Retrieved all file paths.")
        return all_file_paths

# Usage Example
root = os.getenv("FcPerformeter")
data_dir = "0924"
config_file = os.path.join(root, "config", "config.yaml")

path_manager = PathManager(root, data_dir, config_file)

# Example to get a data file
# data_file = path_manager.get_data_file(Category.PS, PSFile.SCR)
# print(data_file.path, data_file.sheet)
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
