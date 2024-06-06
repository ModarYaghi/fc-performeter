import os
import hashlib
from typing import Dict, List, Tuple


def hash_file(file_path: str, blocksize: int = 65536) -> str:
    """
    Generate SHA-256 hash of the given file.

    Parameters:
        file_path (str): The path to the file to hash.
        blocksize (int): The block size in bytes.


    Returns:
        str: The SHA-256 hash of the file.
    """

    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        buf = f.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(blocksize)
        return hasher.hexdigest()


def find_duplicates(directory: str) -> List[Tuple[str, str]]:
    """
    Finds and lists duplicate files in the given directory.

    Parameters:
        directory (str): The directory to search for duplicate files.

    Returns:
        List[Tuple[str, str]]: A list of tuples, each containing path of duplicate files.
    """
    hashes: Dict[str, str] = {}
    duplicates: List[Tuple[str, str]] = []

    for dir_path, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dir_path, filename)
            try:
                filehash = hash_file(file_path)
                if filehash in hashes:
                    duplicates.append((file_path, hashes[filehash]))
                else:
                    hashes[filehash] = file_path

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

    return duplicates


def remove_duplicates(duplicates: List[Tuple[str, str]]) -> None:
    """
        Removes duplicate files, keeping only one instance of each duplicate set.

        Parameters:
            duplicates (List[Tuple[str, str]]): A list of tuples, each containing path of duplicate files.
    """

    for duplicate_set in duplicates:
        for file in duplicate_set[1:]:
            try:
                os.remove(file)
                print(f"Removed duplicate file: {file}")
            except Exception as e:
                print(f"Error removing file {file}: {e}")


def main(directory: str):
    """
    Main function to find and remove duplicate files in the given directory.

    Parameters:
        directory (str): The directory to search for and remove duplicate files.
    """
    duplicates = find_duplicates(directory)
    if duplicates:
        print("Found duplicates")
        for dup in duplicates:
            print(f"{dup[0]} and {dup[1]}")
        remove_duplicates(duplicates)
    else:
        print("No duplicates found.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find and remove duplicate files.")
    parser.add_argument("directory", type=str, help="The directory to search for duplicate files ")
    args = parser.parse_args()

    main(args.directory)
