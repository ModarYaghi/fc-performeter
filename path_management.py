import os
import sys
from enum import Enum, auto

# from pathlib import Path
from pydantic import BaseModel

from src.config_reader import YAMLConfigReader
from collections import namedtuple
from typing import NamedTuple

# Import necessary enums and classes (assuming they are defined elsewhere)
# from .enums import Category, PSFile, PTFile
# from .path_manager import PathManager


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
    CWS = auto()
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
        return os.path.join(self.root, "data", "processed", "unvfvt23")

    def initialize_data_files(self):
        return {
            Category.PS: {
                PSFile.SCR: DataFile(
                    path=os.path.join(
                        self.processed_data, f"01_psscr_{self.data_dir}.csv"
                    ),
                    sheet="Scr",
                ),
                PSFile.PSNT: DataFile(
                    path=os.path.join(
                        self.processed_data, f"02_psint_{self.data_dir}.csv"
                    ),
                    sheet="Int",
                ),
                PSFile.PSG: DataFile(
                    path=os.path.join(
                        self.processed_data, f"03_psgc_{self.data_dir}.csv"
                    ),
                    sheet="GC",
                ),
                PSFile.PSI: DataFile(
                    path=os.path.join(
                        self.processed_data, f"04_psic_{self.data_dir}.csv"
                    ),
                    sheet="IC",
                ),
                PSFile.PSFU: DataFile(
                    path=os.path.join(
                        self.processed_data, f"05_psfua_{self.data_dir}.csv"
                    ),
                    sheet="FUA",
                ),
                PSFile.PEI: DataFile(
                    path=os.path.join(
                        self.processed_data, f"06_pspei_{self.data_dir}.csv"
                    ),
                    sheet="PEI",
                ),
                PSFile.TRW: DataFile(
                    path=os.path.join(
                        self.processed_data, f"07_pstrw_{self.data_dir}.csv"
                    ),
                    sheet="TRW",
                ),
                PSFile.TD: DataFile(
                    path=os.path.join(
                        self.processed_data, f"08_pstd_{self.data_dir}.csv"
                    ),
                    sheet="TD",
                ),
                PSFile.CWS: DataFile(
                    path=os.path.join(
                        self.processed_data, f"09_pscws_{self.data_dir}.csv"
                    ),
                    sheet="CWS",
                ),
                PSFile.AWW: DataFile(
                    path=os.path.join(
                        self.processed_data, f"10_psaw_{self.data_dir}.csv"
                    ),
                    sheet="AW",
                ),
            },
            Category.PT: {
                PTFile.PSFS: DataFile(
                    path=os.path.join(
                        self.processed_data, f"11_ptpsfs_{self.data_dir}.csv"
                    ),
                    sheet="PSFS",
                ),
                PTFile.PTNT: DataFile(
                    path=os.path.join(
                        self.processed_data, f"12_ptint_{self.data_dir}.csv"
                    ),
                    sheet="PTInt",
                ),
                PTFile.PTG: DataFile(
                    path=os.path.join(
                        self.processed_data, f"13_ptgpt_{self.data_dir}.csv"
                    ),
                    sheet="GPT",
                ),
                PTFile.PTI: DataFile(
                    path=os.path.join(
                        self.processed_data, f"14_ptipt_{self.data_dir}.csv"
                    ),
                    sheet="IPT",
                ),
                PTFile.PTFU: DataFile(
                    path=os.path.join(
                        self.processed_data, f"15_ptfua_{self.data_dir}.csv"
                    ),
                    sheet="FUA",
                ),
            },
        }

    def get_data_file(self, category: Category, file_type: Enum) -> DataFile:
        return self.data_files[category][file_type]


# Define a named tuple for file information
FileInfo = namedtuple("FileInfo", ["path", "sheet"])


class PSFiles:
    """
    A class to manage and provide easy access to PS (Primary Source) file information.

    This class encapsulates the paths and sheet names for various PS file types,
    allowing for convenient attribute-based access to this information.

    Attributes:
        SCR, PSNT, PSG, PSI, PSFU, PEI, TRW, TD, CDW, AWW (FileInfo):
            Named tuples containing 'path' and 'sheet' for each PS file type.
    """

    def __init__(self, path_manager):
        """
        Initialize the PSFiles object with file information from the PathManager.

        Args:
            path_manager (PathManager): An instance of PathManager that provides
                                        access to file paths and sheet names.
        """
        # Initialize each PS file type with its corresponding path and sheet name
        self.SCR = self._create_file_info(path_manager, PSFile.SCR)
        self.PSNT = self._create_file_info(path_manager, PSFile.PSNT)
        self.PSG = self._create_file_info(path_manager, PSFile.PSG)
        self.PSI = self._create_file_info(path_manager, PSFile.PSI)
        self.PSFU = self._create_file_info(path_manager, PSFile.PSFU)
        self.PEI = self._create_file_info(path_manager, PSFile.PEI)
        self.TRW = self._create_file_info(path_manager, PSFile.TRW)
        self.TD = self._create_file_info(path_manager, PSFile.TD)
        self.CWS = self._create_file_info(path_manager, PSFile.CWS)
        self.AWW = self._create_file_info(path_manager, PSFile.AWW)

    def _create_file_info(self, path_manager, file_type: PSFile) -> FileInfo:
        """
        Create a FileInfo named tuple for a given PS file type.

        Args:
            path_manager (PathManager): The PathManager instance to use.
            file_type (PSFile): The enum representing the PS file type.

        Returns:
            FileInfo: A named tuple containing the path and sheet name for the file type.
        """
        data_file = path_manager.get_data_file(Category.PS, file_type)
        return FileInfo(data_file.path, data_file.sheet)


class PTFiles:
    """
    A class to manage and provide easy access to PT (Processed Table) file information.

    This class encapsulates the paths and sheet names for various PT file types,
    allowing for convenient attribute-based access to this information.

    Attributes:
        PSFS, PTNT, PTG, PTI, PTFU (FileInfo):
            Named tuples containing 'path' and 'sheet' for each PT file type.
    """

    def __init__(self, path_manager):
        """
        Initialize the PTFiles object with file information from the PathManager.

        Args:
            path_manager (PathManager): An instance of PathManager that provides
                                        access to file paths and sheet names.
        """
        # Initialize each PT file type with its corresponding path and sheet name
        self.PSFS = self._create_file_info(path_manager, PTFile.PSFS)
        self.PTNT = self._create_file_info(path_manager, PTFile.PTNT)
        self.PTG = self._create_file_info(path_manager, PTFile.PTG)
        self.PTI = self._create_file_info(path_manager, PTFile.PTI)
        self.PTFU = self._create_file_info(path_manager, PTFile.PTFU)

    def _create_file_info(self, path_manager, file_type: PTFile) -> FileInfo:
        """
        Create a FileInfo named tuple for a given PT file type.

        Args:
            path_manager (PathManager): The PathManager instance to use.
            file_type (PTFile): The enum representing the PT file type.

        Returns:
            FileInfo: A named tuple containing the path and sheet name for the file type.
        """
        data_file = path_manager.get_data_file(Category.PT, file_type)
        return FileInfo(data_file.path, data_file.sheet)


# Usage example
# if __name__ == "__main__":
# Assume these variables are properly set in your actual code
root = os.getenv("FcPerformeter")
data_dir = "1224"
config_file = os.path.join(root, "config", "config.yaml")

path_manager = PathManger(root, data_dir, config_file)

ps_raw_data = path_manager.ps_raw_data
pspw = path_manager.pspw
pt_raw_data = path_manager.pt_raw_data
ptpw = path_manager.ptpw

# Create instances of PSFiles and PTFiles
ps_files = PSFiles(path_manager)
pt_files = PTFiles(path_manager)

# Examples of accessing PS files
# print(f"SCR path: {ps_files.SCR.path}")
# print(f"SCR sheet: {ps_files.SCR.sheet}")

# Examples of accessing PT files
# print(f"PSFS path: {pt_files.PSFS.path}")
# print(f"PSFS sheet: {pt_files.PSFS.sheet}")


# Usage Example
