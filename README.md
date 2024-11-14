# Flow Log Tagging and Counting Tool

## Overview

This tool parses flow log data and maps each entry to a tag based on a lookup table. The lookup table is defined in an Excel or CSV file containing destination port and protocol combinations, which are mapped to tags. The tool also counts occurrences of tags and unique port/protocol combinations, outputting the results into two separate CSV files.

## Features

- Parses flow log data in plain text format.
- Maps each flow log entry to a tag based on a lookup table.
- Counts and reports tag occurrences, including "Untagged" entries in tag_counts.csv.
- Counts unique port/protocol combinations and outputs them in port_protocol_counts.csv.
- Supports loading lookup tables in `.csv` format.

## Requirements

- Python 3.x
- Libraries:
  - `openpyxl` for reading `.xlsx` files
  - `csv` (included in Python standard library)

Install the `openpyxl` library if not already installed:
```bash
pip install openpyxl
