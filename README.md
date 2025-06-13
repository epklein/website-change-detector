# Website Change Detector

This Python script checks whether a list of URLs have changed since the last snapshot. It is useful for monitoring web pages for updates, ignoring common sources of noise such as ad tracking parameters and dynamic hidden fields.

## Features

- Loads URLs from `pages.txt` (one per line, lines starting with `#` are ignored as comments)
- Supports per-URL ignore patterns: specify a filename after a semicolon to remove custom patterns from the page before comparison (see the `ignore/` directory)
- Fetches each URL and cleans the HTML to remove noise (e.g., ad/tracking query parameters, dynamic hidden fields, scripts, comments)
- Computes a checksum of the cleaned content
- Compares with previously saved checksums in `checksum.csv`
- Prints a list of URLs that have changed since the last snapshot
- Saves updated checksums and change dates for future runs
- Saves a snapshot of the cleaned HTML for each changed page in the `snapshots/` directory, along with a log of changes, for debugging purposes.

## Usage

1. **Install dependencies**  
   Make sure you have Python 3 and install required packages:
   ```
   pip install requests
   ```

2. **Prepare `pages.txt`**  
   List the URLs you want to monitor, one per line. Lines starting with `#` are treated as comments.

   - To use custom ignore patterns for a URL, add a semicolon and the ignore filename (e.g., `https://example.com;example.com`).
   - Place your ignore pattern files in the `ignore/` directory, one regex per line.

3. **Run the script**
   ```
   python main.py
   ```

4. **View results**  
   - Changed URLs will be printed to the console.
   - A log of changes is kept in `snapshots/snapshots.log`.

## How it works

- The script fetches each URL and removes common sources of noise (such as ad image query parameters and dynamic hidden fields) before calculating a checksum.
- If an ignore pattern file is specified for a URL, all matching patterns are removed from the page before comparison.
- If the checksum differs from the previous run, the URL is reported as changed and the date is updated.
- When a change is detected, the cleaned HTML is saved as a snapshot in the `snapshots/` directory, and the change is logged.

## Customization

You can adjust the `clean_html` function in `main.py` to further refine what is considered "noise" for your use case.