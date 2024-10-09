#!/usr/bin/env python3

import os
import hashlib
import argparse
from typing import Tuple


def get_file_hash(file_path:str) -> str:
    """Calculate the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()


def write_index(file_path:str, part_files:list, index_filename="index.txt"):
    # Write index.txt file
    num_parts = len(part_files)
    
    with open(index_filename, 'w') as index_file:
        index_file.write(f"FILENAME: {file_path}\n")
    
        for part_index, part_hash, _ in part_files:
            index_file.write(f"{part_index}, {part_hash}\n")
            
    print(f"File '{file_path}' split into {num_parts} parts. Index saved as {index_filename}")
    
    
def read_index(index_filename:str="index.txt") -> Tuple[str, list]:
    lines = None
    with open(index_filename, "r") as index_file:
        lines = index_file.readlines()
        
    original_file = ""
    parts = []

    for line in lines:
        if line.startswith("FILENAME:"):
            original_file = line.split(": ")[1].strip()
        else:
            try:
                part_index, part_hash = line.strip().split(", ")
                parts.append((int(part_index), part_hash))
            except ValueError:
                continue
            
    return original_file, parts
        


def split_file(file_path: str, num_parts: int) -> None:
    """Splits a file into N smaller parts and generates an index.txt with hashes and original filename."""
    file_size = os.path.getsize(file_path)
    part_size = file_size // num_parts
    part_files = []

    with open(file_path, 'rb') as infile:
        for i in range(num_parts):
            if i == num_parts - 1:
                # Last part - read all remaining bytes
                part_data = infile.read()
            else:
                # Read part_size bytes
                part_data = infile.read(part_size)

            # Calculate hash of the part
            part_hash = hashlib.sha256(part_data).hexdigest()
            part_filename = f"{part_hash}.part"
            part_files.append((i, part_hash, part_filename))

            # Write the part to a file
            with open(part_filename, 'wb') as outfile:
                outfile.write(part_data)

    write_index(file_path, part_files)


def merge_files(index_filename: str) -> None:
    """Merges files based on index.txt using the hash values. Sorts the index entries before merging."""
    if not os.path.exists(index_filename):
        print(f"Error: {index_filename} not found.")
        return

    original_file, parts_info = read_index(index_filename)

    # Sort parts by index to ensure correct merge order
    parts_info = sorted(parts_info, key=lambda x: x[0])

    # Merge the part files in the correct order
    with open(original_file, 'wb') as outfile:
        for part_index, part_hash in parts_info:
            part_filename = f"{part_hash}.part"
            if not os.path.exists(part_filename):
                print(f"Error: Part file {part_filename} not found.")
                return
            with open(part_filename, 'rb') as infile:
                outfile.write(infile.read())

    print(f"Files merged into '{original_file}'")


def main() -> None:
    parser = argparse.ArgumentParser(description="File Splitter and Merger")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Split command
    split_parser = subparsers.add_parser('split', help="Split a file into N parts")
    split_parser.add_argument('file', type=str, help="The file to split")
    split_parser.add_argument('parts', type=int, help="Number of parts to split the file into")

    # Merge command
    merge_parser = subparsers.add_parser('merge', help="Merge files based on index.txt")
    merge_parser.add_argument('index', type=str, help="The index file (index.txt)")

    args = parser.parse_args()

    if args.command == 'split':
        split_file(args.file, args.parts)
    elif args.command == 'merge':
        merge_files(args.index)


if __name__ == "__main__":
    main()

