# Sleek Beauty Parlour — The Look Book

A free, QR-accessible nail gallery for salon clients.
**Live site:** https://sleek-mx.github.io/sleek-lookbook/

The QR code is permanent — print it once and it always points here.
Print-ready card: `qr/print-this-qr-card.png`

---

## Adding photos (the only thing you ever do)

Photos are organised by **folder**. Drop each photo into the folder that matches
its category — the gallery sorts itself automatically:

```
photos/originals/
    manicure-tips/          → Manicure ▸ Tips
    manicure-builder-gel/   → Manicure ▸ Builder Gel
    manicure-gumgel/        → Manicure ▸ Gumgel
    manicure-acrylics/      → Manicure ▸ Acrylics
    manicure-stickons/      → Manicure ▸ Stickons
    pedicure/               → Pedicure
```

iPhone HEIC, JPG and PNG all work. Then, in Terminal:

```
cd ~/Websites\ and\ Dashboards/sleek-lookbook
./publish.sh
```

That optimises every photo, rebuilds the gallery, and pushes it live in about a
minute. The pink sample tiles disappear automatically once your real photos land.

> First time only: `chmod +x publish.sh`

## Captions (optional)

New photos appear with no caption. To add one, open **`photos.json`**, type a
`title` for any photo, and run `./publish.sh` again. Your captions are kept when
you add more photos later.

## Booking button & contact

Edit **`config.json`**:

```json
{ "bookingUrl": "https://wa.me/2547XXXXXXXX", "contact": "Sleek Beauty Parlour" }
```

Leave `bookingUrl` as `""` to hide the button. Then `./publish.sh`.

---

## What clients can do on the site

- Browse by **Manicure / Pedicure** and the manicure sub-categories
- Tap the **♥** on any look to save it; **Favourites** filter shows saved looks
- Tap a photo for a full-screen view with swipe between looks
- Scan-to-open QR; works on any phone, no app needed

## Files

| File / folder | What it is |
|---|---|
| `index.html` | The website |
| `photos/originals/<category>/` | **Drop your full-size photos here** |
| `photos/` | Auto-generated web versions (don't edit) |
| `photos.json` | The gallery list — edit captions here |
| `config.json` | Booking link + contact |
| `qr/` | QR code + printable card |
| `build.py` / `publish.sh` | Build + publish |

Cost: **$0** — hosted free on GitHub Pages.
