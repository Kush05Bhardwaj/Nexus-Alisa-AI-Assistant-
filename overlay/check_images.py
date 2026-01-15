"""
Check if overlay images are transparent PNGs
"""
from PIL import Image
from pathlib import Path

ASSETS = Path("assets")

def check_image(name):
    img = Image.open(ASSETS / name)
    print(f"\n{name}:")
    print(f"  Mode: {img.mode}")
    print(f"  Size: {img.size}")
    print(f"  Format: {img.format}")
    if img.mode == "RGBA":
        # Check if it has transparency
        alpha = img.split()[3]
        alpha_data = list(alpha.getdata())
        has_transparency = any(a < 255 for a in alpha_data)
        print(f"  Has transparency: {has_transparency}")
        # Check if it has any visible content
        has_content = any(a > 0 for a in alpha_data)
        print(f"  Has visible content: {has_content}")

print("=== Checking Image Properties ===")
images = ["base.png", "happy.png", "eyes_closed.png", "mouth_open.png"]

for img_name in images:
    try:
        check_image(img_name)
    except Exception as e:
        print(f"\n{img_name}: ERROR - {e}")
