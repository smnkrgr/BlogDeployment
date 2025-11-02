from PIL import Image
import os

# -----------------------------
# CONFIGURATION
# -----------------------------
source_image = "logo.png"   # Your original PNG
output_dir = "output"     # Folder to save all icons
os.makedirs(output_dir, exist_ok=True)

# Sizes to generate (favicon.ico & PNG touch icons)
favicon_sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
apple_touch_sizes = [(180,180), (152,152), (120,120), (76,76)]

# -----------------------------
# OPEN IMAGE
# -----------------------------
img = Image.open(source_image)

# -----------------------------
# GENERATE favicon.ico
# -----------------------------
ico_path = os.path.join(output_dir, "favicon.ico")
img.save(ico_path, format="ICO", sizes=favicon_sizes)
print(f"Generated {ico_path}")

# -----------------------------
# GENERATE PNG ICONS
# -----------------------------
for size in apple_touch_sizes:
    icon = img.resize(size, Image.LANCZOS)
    path = os.path.join(output_dir, f"apple-touch-icon-{size[0]}x{size[1]}.png")
    icon.save(path, format="PNG")
    print(f"Generated {path}")

