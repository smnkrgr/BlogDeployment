import os
import re
import shutil
import yaml

# -----------------------------
# LOAD CONFIGURATION
# -----------------------------
CONFIG_PATH = "config.yaml"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

VAULT_DIR = cfg["vault_dir"]
JEKYLL_NOTES_DIR = cfg["jekyll_notes_dir"]
JEKYLL_IMG_DIR = cfg["jekyll_img_dir"]
IMG_EXTENSIONS = cfg.get("img_extensions", [".png", ".jpg", ".jpeg", ".gif", ".svg"])

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def is_image_file(filename):
    return any(filename.lower().endswith(ext) for ext in IMG_EXTENSIONS)

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

# -----------------------------
# MAIN CONVERSION
# -----------------------------
for root, dirs, files in os.walk(VAULT_DIR):
    for file in files:
        if not file.endswith(".md"):
            continue

        md_path = os.path.join(root, file)
        rel_path = os.path.relpath(md_path, VAULT_DIR)

        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Replace Obsidian-style image links
        def replace_link(match):
            img_name = match.group(1)
            found = None

            for search_root, _, search_files in os.walk(VAULT_DIR):
                if img_name in search_files and is_image_file(img_name):
                    found = os.path.join(search_root, img_name)
                    break

            if not found:
                print(f"⚠️  Warning: {img_name} not found for {md_path}")
                return match.group(0)

            ensure_dir(JEKYLL_IMG_DIR)
            dest_path = os.path.join(JEKYLL_IMG_DIR, img_name)

            if not os.path.exists(dest_path):
                shutil.copy2(found, dest_path)
                print(f"📸 Copied image: {img_name}")

            return f"![{os.path.splitext(img_name)[0]}]({{ '{{' }}/assets/images/{img_name}{{ '}}' | relative_url }})"

        content_new = re.sub(r'!\[\[([^\]]+)\]\]', replace_link, content)

        dest_md_path = os.path.join(JEKYLL_NOTES_DIR, rel_path)
        ensure_dir(os.path.dirname(dest_md_path))
        with open(dest_md_path, "w", encoding="utf-8") as f:
            f.write(content_new)

        print(f"+ Converted: {rel_path}")

