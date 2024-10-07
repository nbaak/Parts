# Parts: File Splitter and Merger Tool

**Parts** is a Python-based tool that enables you to split large files into smaller parts and merge them back together. Each part is uniquely identified by its SHA-256 hash, and an `index.txt` file is generated to track the original filename and the part hashes. The tool ensures correct reassembly of files, even if the entries in `index.txt` are stored in a random order.

## Features

- **Split Files:** Break down a large file into smaller parts for easier storage or transfer.
- **Merge Files:** Reassemble the split parts into the original file using the `index.txt` file.
- **SHA-256 Hashing:** File parts are named using their unique SHA-256 hash for identification.
- **Index File Generation:** The tool generates an `index.txt` containing the original file name and part hashes.
- **Random Order Handling:** The tool sorts the parts based on the index before merging, ensuring proper file reconstruction.



## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Splitting Files](#splitting-files)
  - [Merging Files](#merging-files)
- [Index File Format](#index-file-format)
- [Example](#example)
- [Notes](#notes)
- [License](#license)



## Installation

### Requirements:
- **Python 3.6+**

No additional dependencies are required.

### Setup:
1. Clone or download this repository.
2. Ensure Python is installed and available in your PATH.



## Usage

The tool has two main operations: **split** and **merge**. You can invoke them using the command-line interface as follows:

```bash
python parts.py [command] [arguments]
```

### Splitting Files

To split a file into N parts:

```bash
python parts.py split <file_path> <number_of_parts>
```

- `<file_path>`: The path to the file you want to split.
- `<number_of_parts>`: The number of parts to split the file into.

#### Example:

```bash
python parts.py split example.webp 3
```

This command will split `example.webp` into 3 parts and generate part files named using their hash values. It also creates an `index.txt` file in the following format:

```text
FILENAME: example.webp
0, d089634832ee6b86155e25d79a5c282ebfdebf51c9c1f605720477f851e3fff9
1, c9ecb5cc46714a511b4d4a7d7aed7f7e2aee0f34d318a590af2f8917ca321a9c
2, 1c1d2a00745cafa0c1ba4eb6622c7b4552f1c6d40f427a75465489f1a7cd4e00
```

### Merging Files

To merge split files back into the original file, use the `merge` command:

```bash
python parts.py merge <index_file>
```

- `<index_file>`: The path to the `index.txt` file that tracks the parts.

#### Example:

```bash
python parts.py merge index.txt
```

This command reads the `index.txt`, sorts the part hashes by their index, and merges the parts back into the original file.



## Index File Format

The `index.txt` file serves as a record of the split parts and their SHA-256 hashes. The format is:

```text
FILENAME: <original_file_name>
<part_index>, <part_hash>
<part_index>, <part_hash>
...
```

- **FILENAME**: The original file's name.
- **Part Index**: The numerical index of the part (starting from 0).
- **Part Hash**: The SHA-256 hash of the part file.

**Example `index.txt`:**

```text
FILENAME: example.webp
1, c9ecb5cc46714a511b4d4a7d7aed7f7e2aee0f34d318a590af2f8917ca321a9c
2, 1c1d2a00745cafa0c1ba4eb6622c7b4552f1c6d40f427a75465489f1a7cd4e00
0, d089634832ee6b86155e25d79a5c282ebfdebf51c9c1f605720477f851e3fff9
```

Even if the part entries are in random order, **Parts** will sort them by their index before merging.



## Example

### 1. Splitting a File

To split `example.webp` into 3 parts:

```bash
python parts.py split example.webp 3
```

This will create:
- 3 part files, each named using its SHA-256 hash.
- An `index.txt` file with the part information.

### 2. Merging the File Back

To merge the parts back into `example.webp`, run:

```bash
python parts.py merge index.txt
```

This will read the `index.txt`, sort the entries by index, and recreate the `example.webp` file.



## Notes

- **Error Handling**: If a part file is missing or the index file is corrupted, the tool will report the issue and stop the merging process.
- **File Integrity**: The tool does not verify the file integrity beyond using hashes for part identification. Make sure the part files are not tampered with after splitting.
- **Duplicate Entries**: If duplicate entries appear in `index.txt`, the tool will safely ignore them.



## License

**Parts** is available under the MIT License.



### Happy File Splitting and Merging!

