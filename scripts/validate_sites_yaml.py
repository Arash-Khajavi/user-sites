import yaml
import re
import sys
import requests

def is_valid_url(url):
    return re.match(r'^https://[^\s]+$', url) is not None

def is_local_url(url):
    return any(local in url for local in ['localhost', '127.0.0.1', '0.0.0.0'])

def is_deployed(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code < 400
    except requests.RequestException:
        return False

def main():
    with open("sites.yaml", "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(f"YAML Error: {e}")
            sys.exit(1)

    if not isinstance(data, list):
        print("❌ sites.yaml must be a list of site entries.")
        sys.exit(1)

    errors = []
    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            errors.append(f"❌ Entry #{i + 1} is not a dictionary.")
            continue

        name = entry.get("name")
        url = entry.get("url")

        if not name or not isinstance(name, str):
            errors.append(f"❌ Entry #{i + 1}: 'name' is missing or invalid.")

        if not url or not is_valid_url(url):
            errors.append(f"❌ Entry #{i + 1}: 'url' is missing or must start with https://")
        elif is_local_url(url):
            errors.append(f"❌ Entry #{i + 1}: 'url' points to a local address and is not allowed.")
        elif not is_deployed(url):
            errors.append(f"❌ Entry #{i + 1}: '{url}' is not reachable (site not deployed?).")

    if errors:
        for error in errors:
            print(error)
        sys.exit(1)

    print("✅ sites.yaml passed validation.")

if __name__ == "__main__":
    main()

