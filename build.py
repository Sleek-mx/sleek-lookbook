#!/usr/bin/env python3
"""
Build the Sleek Beauty Parlour nail lookbook.

HOW IT WORKS
------------
You organise photos by dropping them into category folders inside
`photos/originals/`.  The folder name decides where each photo shows up:

    photos/originals/
        manicure-tips/          -> Manicure ▸ Tips
        manicure-builder-gel/   -> Manicure ▸ Builder Gel
        manicure-gumgel/        -> Manicure ▸ Gumgel
        manicure-acrylics/      -> Manicure ▸ Acrylics
        manicure-stickons/      -> Manicure ▸ Stickons
        pedicure/               -> Pedicure

iPhone HEIC, JPG and PNG all work. Run:

    python3 build.py     (or just ./publish.sh to build + push live)

Captions are optional — edit the "title" of any photo in photos.json and
re-publish; your captions are kept when you add more photos later.
"""
import json, os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "photos", "originals")
OUT  = os.path.join(HERE, "photos")
MANIFEST = os.path.join(HERE, "photos.json")
CONFIG   = os.path.join(HERE, "config.json")
MAX_EDGE = 1400
EXTS = (".jpg", ".jpeg", ".png", ".heic", ".webp")

# folder name -> (service, type)
FOLDER_MAP = {
    "manicure-tips":        ("Manicure", "Tips"),
    "manicure-builder-gel": ("Manicure", "Builder Gel"),
    "manicure-gumgel":      ("Manicure", "Gumgel"),
    "manicure-acrylics":    ("Manicure", "Acrylics"),
    "manicure-stickons":    ("Manicure", "Stickons"),
    "pedicure":             ("Pedicure", ""),
}

def ensure_folders():
    for name in FOLDER_MAP:
        os.makedirs(os.path.join(SRC, name), exist_ok=True)

def optimise(src_path, out_name):
    target = os.path.join(OUT, out_name)
    if os.path.exists(target) and os.path.getmtime(target) >= os.path.getmtime(src_path):
        return
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-Z", str(MAX_EDGE), src_path, "--out", target],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print(f"  optimised {out_name}")

def load_existing():
    if os.path.exists(MANIFEST):
        try:
            return {p["src"]: p for p in json.load(open(MANIFEST)).get("photos", [])}
        except Exception:
            return {}
    return {}

def main():
    ensure_folders()
    existing = load_existing()
    photos = []
    total = 0
    print("Optimising photos…")
    for folder, (service, ptype) in FOLDER_MAP.items():
        fdir = os.path.join(SRC, folder)
        for name in sorted(os.listdir(fdir)):
            if not name.lower().endswith(EXTS) or name.startswith("."):
                continue
            stem = os.path.splitext(name)[0]
            out_name = f"{folder}__{stem}.jpg"
            optimise(os.path.join(fdir, name), out_name)
            src = f"photos/{out_name}"
            prev = existing.get(src, {})
            photos.append({
                "src": src,
                "service": service,
                "type": ptype,
                "title": prev.get("title", ""),
            })
            total += 1

    config = json.load(open(CONFIG)) if os.path.exists(CONFIG) else {}
    json.dump({"config": config, "photos": photos},
              open(MANIFEST, "w"), indent=2, ensure_ascii=False)
    print(f"\n✓ photos.json written — {total} photo(s).")
    if not total:
        print("⚠  No photos found. Drop images into the folders under photos/originals/ and run again.")

if __name__ == "__main__":
    main()
