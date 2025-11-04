import os
import re
import shutil
from datetime import date
import yaml
from urllib.parse import unquote

# ---------------------------------
# Load configuration
# ---------------------------------
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

OBSIDIAN_POSTS = config["obsidian_posts_folder"]
OBSIDIAN_IMAGES = config["obsidian_images_folder"]
JEKYLL_POSTS = config["jekyll_posts_folder"]
JEKYLL_IMAGES = config["jekyll_images_folder"]

# Ensure output folders exist
os.makedirs(JEKYLL_POSTS, exist_ok=True)
os.makedirs(JEKYLL_IMAGES, exist_ok=True)

# ---------------------------------
# Helper Functions
# ---------------------------------
def convert_image_links(content):
    """
    Convert both Obsidian and Markdown image links into Jekyll-compatible format.
    Only processes known image file extensions.
    """

    valid_extensions = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")

    # Pattern for Obsidian-style images: ![[image.png]]
    obsidian_pattern = r"!\[\[(.*?)\]\]"

    # Pattern for Markdown-style images: ![](image.png) or ![](Pasted%20image.png)
    markdown_pattern = r"!\[.*?\]\((.*?)\)"

    # Combine both matches
    matches = re.findall(obsidian_pattern, content) + re.findall(markdown_pattern, content)

    for match in matches:
        # Decode URL-encoded filenames like "Pasted%20image.png"
        decoded_name = unquote(os.path.basename(match))

        # Skip if not an image
        if not decoded_name.lower().endswith(valid_extensions):
            continue

        src_path = os.path.join(OBSIDIAN_IMAGES, decoded_name)
        dest_path = os.path.join(JEKYLL_IMAGES, decoded_name)

        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Copied image: {decoded_name}")
        else:
            print(f"Warning: Image not found: {src_path}")

        # Replace both types of image links in content
        jekyll_link = f"![{decoded_name}](/assets/images/{decoded_name})"
        content = re.sub(rf"!\[\[\s*{re.escape(match)}\s*\]\]", jekyll_link, content)
        content = re.sub(rf"!\[.*?\]\(\s*{re.escape(match)}\s*\)", jekyll_link, content)

    return content


def create_jekyll_post(title, content):
    """
    Wrap the content with Jekyll front matter.
    """
    today = date.today().strftime("%Y-%m-%d")
    header = f"""---
layout: post
title: "{title}"
date: {today}
---

"""
    return header + content


def safe_title_to_filename(title):
    """
    Convert note title to a filesystem-safe slug and add the date prefix.
    """
    slug = re.sub(r"[^a-zA-Z0-9-_]+", "-", title.lower()).strip("-")
    today = date.today().strftime("%Y-%m-%d")
    return f"{today}-{slug}.md"


# ---------------------------------
# Convert Markdown Files
# ---------------------------------
for filename in os.listdir(OBSIDIAN_POSTS):
    if not filename.endswith(".md"):
        continue

    obsidian_path = os.path.join(OBSIDIAN_POSTS, filename)

    with open(obsidian_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Convert image links and copy images
    converted_content = convert_image_links(content)

    # Use the first heading or filename as title
    lines = converted_content.splitlines()
    if lines and lines[0].startswith("# "):
        title_line = lines[0].lstrip("# ").strip()
        converted_content = "\n".join(lines[1:]).strip()
    else:
        title_line = os.path.splitext(filename)[0]

    # Add Jekyll front matter
    post_content = create_jekyll_post(title_line, converted_content)

    # Generate filename
    jekyll_filename = safe_title_to_filename(title_line)
    output_path = os.path.join(JEKYLL_POSTS, jekyll_filename)

    # Write the converted file (overwrite if exists)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(post_content)

    print(f"Converted: {filename} -> {jekyll_filename}")

print("Conversion complete.")

