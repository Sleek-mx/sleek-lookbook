#!/usr/bin/env python3
"""
Build the Sleek Beauty Parlour nail lookbook.

Photos live in category folders under photos/originals/ (the folders just keep
things tidy — the website shows everything together in one flowing gallery):

    photos/originals/
        manicure-tips/  manicure-builder-gel/  manicure-gumgel/
        manicure-acrylics/  manicure-stickons/  pedicure/

Each photo is re-exported at full native resolution with a clarity / sharpness /
vibrance pass so it looks crisp and bright on phones (no upscaling — we never
blow a small photo up, which only adds blur).

Run:  python3 build.py     (or ./publish.sh to build + push live)
"""
import json, os
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SRC  = os.path.join(HERE, "photos", "originals")
OUT  = os.path.join(HERE, "photos")
MANIFEST = os.path.join(HERE, "photos.json")
CONFIG   = os.path.join(HERE, "config.json")
MAX_EDGE = 1800          # cap; we never enlarge beyond the original
QUALITY  = 92
EXTS = (".jpg", ".jpeg", ".png", ".heic", ".webp")

FOLDER_MAP = {
    "manicure-tips":        ("Manicure", "Tips"),
    "manicure-builder-gel": ("Manicure", "Builder Gel"),
    "manicure-gumgel":      ("Manicure", "Gumgel"),
    "manicure-acrylics":    ("Manicure", "Acrylics"),
    "manicure-stickons":    ("Manicure", "Stickons"),
    "pedicure":             ("Pedicure", ""),
}

def enhance(im):
    """Make the photo look clear & crystal: gentle clarity, contrast, vibrance."""
    im = ImageOps.exif_transpose(im).convert("RGB")
    # downsize only if larger than cap (LANCZOS = sharp downscale); never upscale
    w, h = im.size
    if max(w, h) > MAX_EDGE:
        s = MAX_EDGE / max(w, h)
        im = im.resize((round(w*s), round(h*s)), Image.LANCZOS)
    # clarity: unsharp mask brings out nail detail
    im = im.filter(ImageFilter.UnsharpMask(radius=2.2, percent=115, threshold=2))
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.10)     # vibrance pop
    im = ImageEnhance.Sharpness(im).enhance(1.12)
    return im

def optimise(src_path, out_path):
    if os.path.exists(out_path) and os.path.getmtime(out_path) >= os.path.getmtime(src_path):
        return
    im = enhance(Image.open(src_path))
    im.save(out_path, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    print(f"  enhanced {os.path.basename(out_path)}")

def load_existing():
    if os.path.exists(MANIFEST):
        try:
            return {p["src"]: p for p in json.load(open(MANIFEST)).get("photos", [])}
        except Exception:
            return {}
    return {}

def main():
    existing = load_existing()
    buckets = {}                      # folder -> list of photo dicts
    print("Enhancing photos…")
    for folder, (service, ptype) in FOLDER_MAP.items():
        fdir = os.path.join(SRC, folder)
        os.makedirs(fdir, exist_ok=True)
        bucket = []
        for name in sorted(os.listdir(fdir)):
            if not name.lower().endswith(EXTS) or name.startswith("."):
                continue
            stem = os.path.splitext(name)[0]
            out_name = f"{folder}__{stem}.jpg"
            optimise(os.path.join(fdir, name), os.path.join(OUT, out_name))
            src = f"photos/{out_name}"
            prev = existing.get(src, {})
            bucket.append({"src": src, "service": service, "type": ptype,
                           "title": prev.get("title", "")})
        if bucket:
            buckets[folder] = bucket

    # interleave categories (round-robin) so the gallery feels varied, not grouped
    photos = []
    longest = max((len(b) for b in buckets.values()), default=0)
    for i in range(longest):
        for folder in buckets:
            if i < len(buckets[folder]):
                photos.append(buckets[folder][i])

    config = json.load(open(CONFIG)) if os.path.exists(CONFIG) else {}
    json.dump({"config": config, "photos": photos},
              open(MANIFEST, "w"), indent=2, ensure_ascii=False)
    print(f"\n✓ photos.json written — {len(photos)} photo(s).")

if __name__ == "__main__":
    main()
