import yaml
import requests
import sys
from urllib.parse import urlparse

with open("sites.yaml", "r") as f:
    data = yaml.safe_load(f)

errors = []
seen_urls = set()

for entry in data.get("sites", []):
    url = entry.get("url", "").strip()

    # Check 1: starts with https
    if not url.startswith("https://"):
        errors.append(f"{url} does not start with https://")

    # Check 2: disallow localhost or 127.0.0.1
    parsed = urlparse(url)
    if parsed.hostname in ("127.0.0.1", "localhost"):
        errors.append(f"{url} points to localhost")

    # Check 3: is it a duplicate?
    if url in seen_urls:
        errors.append(f"{url} is duplicated")
    else:
        seen_urls.add(url)

    # Check 4: try to access site
    try:
        response = requests.get(url, timeout=5)
        if response.status_code >= 400:
            errors.append(f"{url} returned HTTP {response.status_code}")
    except Exception as e:
        errors.append(f"{url} could not be reached: {str(e)}")

# Final report
if errors:
    for err in errors:
        print("❌", err)
    sys.exit(1)

print("✅ All sites validated successfully.")


