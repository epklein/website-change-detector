# Website Change Detector

This Python script checks whether a list of URLs have changed since the last snapshot. It is useful for monitoring web pages for updates, ignoring common sources of noise such as ad tracking parameters and dynamic hidden fields.

## Features

- Loads URLs from `pages.txt` (one per line, lines starting with `#` are ignored as comments)
- Fetches each URL and cleans the HTML to remove noise (e.g., ad/tracking query parameters, dynamic hidden fields, scripts, comments)
- Computes a checksum of the cleaned content
- Compares with previously saved checksums in `checksum.csv`
- Prints a list of URLs that have changed since the last snapshot
- Saves updated checksums and change dates for future runs

## Usage

1. **Install dependencies**  
   Make sure you have Python 3 and install required packages:
   ```
   pip install requests
   ```

2. **Prepare `pages.txt`**  
   List the URLs you want to monitor, one per line. Lines starting with `#` are treated as comments.

3. **Run the script**
   ```
   python main.py
   ```

4. **View results**  
   - Changed URLs will be printed to the console.
   - The script updates `checksum.csv` with the latest checksums and change dates.

## How it works

- The script fetches each URL and removes common sources of noise (such as ad image query parameters and dynamic hidden fields) before calculating a checksum.
- If the checksum differs from the previous run, the URL is reported as changed and the date is updated.

## Customization

You can adjust the `clean_html` function in `main.py` to further refine what is considered "noise" for your use case.