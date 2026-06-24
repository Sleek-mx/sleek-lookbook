#!/usr/bin/env python3
"""
Build the Sleek Beauty Parlour lookbook.

What it does:
  1. Optimises every image in  photos/originals/  -> photos/  (resized, web-ready)
  2. Regenerates  photos.json  (the gallery the website reads)
     - keeps any titles/categories you already set
     - new photos appear automatically with a blank title and category "All"
  3. Pulls booking URL / contact from config.json

Usage:
    python3 build.py

Then:  git add -A && git commit -m "update photos" && git push
(or just run ./publish.sh which does the commit + push for you)
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "photos", "originals")   # drop full-size photos here
OUT  = os.path.join(HERE, "photos")                # optimised versions live here
MANIFEST = os.path.join(HERE, "photos.json")
CONFIG   = os.path.join(HERE, "config.json")
MAX_EDGE = 1400          # px, long edge — sharp on phones, small in bytes
EXTS = (".jpg", ".jpeg", ".png", ".heic", ".webp")

os.makedirs(SRC, exist_ok=True)

def optimise():
    """Resize each original into OUT as a .jpg, skipping ones already done."""
    made = []
    for name in sorted(os.listdir(SRC)):
        if not name.lower().endswith(EXTS) or name.startswith("."):
            continue
        stem = os.path.splitext(name)[0]
        target_name = stem + ".jpg"
        target = os.path.join(OUT, target_name)
        src = os.path.join(SRC, name)
        if os.path.exists(target) and os.path.getmtime(target) >= os.path.getmtime(src):
            made.append(target_name)
            continue
        # sips: resize long edge + convert to jpeg (handles HEIC from iPhone too)
        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-Z", str(MAX_EDGE), src, "--out", target],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        made.append(target_name)
        print(f"  optimised {name} -> photos/{target_name}")
    return made

def load_existing():
    if os.path.exists(MANIFEST):
        try:
            return {p["src"]: p for p in json.load(open(MANIFEST)).get("photos", [])}
        except Exception:
            return {}
    return {}

def main():
    print("Optimising photos…")
    files = optimise()
    if not files:
        print("\n⚠  No photos found in  photos/originals/ — drop your images there and run again.")
    existing = load_existing()
    photos = []
    for f in files:
        src = f"photos/{f}"
        prev = existing.get(src, {})
        photos.append({
            "src": src,
            "title": prev.get("title", ""),
            "category": prev.get("category", "All"),
        })
    config = json.load(open(CONFIG)) if os.path.exists(CONFIG) else {}
    json.dump({"config": config, "photos": photos},
              open(MANIFEST, "w"), indent=2, ensure_ascii=False)
    print(f"\n✓ photos.json written — {len(photos)} photo(s) in the lookbook.")
    if photos:
        print("  Edit titles/categories in photos.json any time, then re-run publish.")

if __name__ == "__main__":
    main()
