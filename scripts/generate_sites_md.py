import yaml

# File paths
yaml_file = "sites.yaml"
markdown_file = "sites.md"

def load_sites():
    with open(yaml_file, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def format_site(site):
    name = site.get('name', 'Unnamed Site')
    url = site.get('url', '#')
    description = site.get('description', '')
    tags = site.get('tags', [])

    tag_line = ""
    if tags:
        tag_line = "**Tags:** " + ", ".join(f"`{tag}`" for tag in tags)

    return f"## [{name}]({url})\n{description}\n{tag_line}\n\n---\n"

def generate_markdown(sites):
    with open(markdown_file, 'w', encoding='utf-8') as md:
        md.write("# 🌐 Submitted Websites\n\n")
        for site in sites:
            md.write(format_site(site))

if __name__ == "__main__":
    sites = load_sites()
    generate_markdown(sites)
    print("✅ sites.md successfully generated.")
