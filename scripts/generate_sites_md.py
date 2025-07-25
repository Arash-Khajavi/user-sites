import yaml

with open("sites.yaml", "r", encoding="utf-8") as f:
    sites = yaml.safe_load(f)

with open("sites.md", "w", encoding="utf-8") as f:
    f.write("# 🌐 Submitted Sites\n\n")
    for site in sites:
        name = site.get("name", "Unnamed Site")
        url = site.get("url", "")
        desc = site.get("description", "")
        tags = ", ".join(site.get("tags", []))

        f.write(f"## [{name}]({url})\n")
        if desc:
            f.write(f"- **Description:** {desc}\n")
        if tags:
            f.write(f"- **Tags:** {tags}\n")
        f.write("\n")

