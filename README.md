# SubFilter Tool

**SubFilter** is a Python tool used to filter subdomain URLs generated from various tools like Amass, Subfinder, Sublist3r, Knockpy, etc. The tool filters URLs to reduce redundancy by keeping only unique subdomains with specific query parameters.

## Features
- Supports input from various tools like Amass, Subfinder, Sublist3r, Knockpy.
- Filters URLs based on query parameters and ensures unique subdomains.
- Saves the filtered URLs to an output file.

## Installation
- Ensure you have Python 3.7+ installed.
- Install required libraries using the following command:

  ```bash
  pip install -r requirements.txt
  ```

## Usage
To run the tool, use the following command:

```bash
python SubFilter.py <input_file> --tool <tool_name> --output <output_file>

