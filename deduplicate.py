import os
import hashlib
from typing import Dict, List, Tuple


def hash_file(filepath: str, blocksize: int = 65536) -> str:
    """
    Generates a SHA-256 hash for the given file.

    Parameters:
    filepath (str): The path to the file to hash.
    blocksize (int): The block size to use for reading the file. Defaults to 65536.

    Returns:
    str: The SHA-256 hash of the file.
    """
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as file:
            buf = file.read(blocksize)
            while len(buf) > 0:
                hasher.update(buf)
                buf = file.read(blocksize)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None


def find_duplicates(directory: str) -> List[Tuple[str, str]]:
    """
    Finds and lists duplicate files in the given directory and its sub-directories.

    Parameters:
    directory (str): The directory to search for duplicate files.

    Returns:
    List[Tuple[str, str]]: A list of tuples, each containing paths of duplicate files.
    """
    hashes: Dict[str, str] = {}
    duplicates: List[Tuple[str, str]] = []
    file_count = 0

    print(f"Scanning directory: {directory}")

    for dirpath, _, filenames in os.walk(directory):
        print(f"Checking directory: {dirpath}")
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            print(f"Processing file: {filepath}")
            filehash = hash_file(filepath)
            if filehash:
                file_count += 1
                if filehash in hashes:
                    duplicates.append((filepath, hashes[filehash]))
                else:
                    hashes[filehash] = filepath
            else:
                print(f"Skipping file due to error: {filepath}")

    print(f"Total files processed: {file_count}")
    return duplicates


def remove_duplicates(duplicates: List[Tuple[str, str]]):
    """
    Removes duplicate files, keeping only one instance of each duplicate set.

    Parameters:
    duplicates (List[Tuple[str, str]]): A list of tuples, each containing paths of duplicate files.
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
        print("Found duplicates:")
        for dup in duplicates:
            print(f"{dup[0]} and {dup[1]}")
        remove_duplicates(duplicates)
    else:
        print("No duplicates found.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Find and remove duplicate files.")
    parser.add_argument("directory", type=str, help="The directory to search for duplicate files.")
    args = parser.parse_args()

    main(args.directory)
