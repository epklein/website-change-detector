import hashlib
import requests
import csv
import os
import re
from datetime import datetime

PAGES_FILE = "pages.txt"
CHECKSUM_FILE = "checksum.csv"

def load_urls(filename):
    urls = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ";" in line:
                url, ignore_file = line.split(";", 1)
                urls.append((url.strip(), ignore_file.strip()))
            else:
                urls.append((line, None))
    return urls

def load_checksums(filename):
    checksums = {}
    if os.path.exists(filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                checksums[row[0]] = (row[1], row[2])
    return checksums

def save_checksums(filename, checksums):
    with open(filename, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for url, (checksum, date) in checksums.items():
            writer.writerow([url, checksum, date])

def clean_html(html):
    # Remove query parameters from all image URLs (jpg, png, gif, etc.)
    html = re.sub(rb'(\.(jpg|png|gif|jpeg))\?\d+', rb'\1', html, flags=re.IGNORECASE)
    # Remove hidden ASP.NET fields that change every request
    html = re.sub(rb'<input[^>]+name="__VIEWSTATE"[^>]*>', b'', html, flags=re.IGNORECASE)
    html = re.sub(rb'<input[^>]+name="__VIEWSTATEGENERATOR"[^>]*>', b'', html, flags=re.IGNORECASE)
    html = re.sub(rb'<input[^>]+name="__EVENTVALIDATION"[^>]*>', b'', html, flags=re.IGNORECASE)
    # Remove all <script>...</script> blocks
    html = re.sub(rb'<script.*?>.*?</script>', b'', html, flags=re.DOTALL|re.IGNORECASE)
    # Remove all HTML comments
    html = re.sub(rb'<!--.*?-->', b'', html, flags=re.DOTALL)
    # Normalize whitespace
    html = re.sub(rb'\s+', b' ', html)
    return html.strip()

def remove_ignore_patterns(content, ignore_file):
    if not ignore_file:
        return content
    ignore_path = os.path.join("ignore", ignore_file)
    if not os.path.exists(ignore_path):
        return content
    with open(ignore_path, "r") as f:
        for pattern in f:
            pattern = pattern.strip()
            if not pattern or pattern.startswith("#"):
                continue
            content = re.sub(pattern.encode(), b'', content)
    return content

def get_checksum(content):
    return hashlib.sha256(content).hexdigest()

def main():
    urls = load_urls(PAGES_FILE)
    old_checksums = load_checksums(CHECKSUM_FILE)
    new_checksums = {} 
    changed_urls = []

    for url, ignore_file in urls:
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            cleaned = clean_html(resp.content)
            cleaned = remove_ignore_patterns(cleaned, ignore_file)
            checksum = get_checksum(cleaned)
            old_checksum, old_date = old_checksums.get(url, (None, None))
            if old_checksum != checksum:
                # New page or changed page
                date = datetime.now().isoformat()
                changed_urls.append((url, date))
            else:
                date = old_date
            new_checksums[url] = (checksum, date)
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    if changed_urls:
        print("Changed URLs since last snapshot:")
        for url, date in changed_urls:
            print(f"{url} (changed at {date})")
    else:
        print("No changes detected.")

    save_checksums(CHECKSUM_FILE, new_checksums)

if __name__ == "__main__":
    main()