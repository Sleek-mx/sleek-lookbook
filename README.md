# Sleek Beauty Parlour — website + look book

The salon's public website, with the nail gallery built in.
**Live:** https://sleek-mx.github.io/sleek-lookbook/

| Page | What it is |
|---|---|
| `/` | The website — services & prices, look book preview, the studio, visit & contact, FAQ |
| `/lookbook/` | The full nail gallery — filter by type, save favourites, tap to enlarge |

The printed QR code still points at `/` and always will, so the card in the salon
never needs reprinting. Clients who scan it land on the homepage with the gallery
one tap away.

---

## Adding photos (the only thing you ever do)

Photos are organised by **folder**. Drop each photo into the folder that matches
its category — the gallery sorts itself automatically:

```
photos/originals/
    manicure-tips/          → Tips
    manicure-builder-gel/   → Builder Gel
    manicure-gumgel/        → Gumgel
    manicure-acrylics/      → Acrylics
    manicure-stickons/      → Stickons
    pedicure/               → Pedicure
```

iPhone HEIC, JPG and PNG all work. Then, in Terminal:

```
cd ~/Websites\ and\ Dashboards/sleek-lookbook
./publish.sh
```

That optimises every photo, rebuilds the gallery, and pushes it live in about a
minute. **The first run takes an extra minute** — it quietly installs its own
private copy of Python's photo tools into `.venv/` (the Mac's built-in `python3`
doesn't have them). Every run after that is fast.

> First time only: `chmod +x publish.sh`

## Captions (optional)

New photos appear with no caption. To add one, open **`photos.json`**, type a
`title` for any photo, and run `./publish.sh` again. Your captions are kept when
you add more photos later.

## Changing prices or text

Prices, services, address, hours and FAQ answers live directly in **`index.html`** —
search for the price (e.g. `1,550`) or the sentence you want to change, edit it,
then run `./publish.sh`.

Two places hold the same prices and must be changed together:
1. the price lists in `index.html`
2. the `hasOfferCatalog` block at the bottom of `index.html` (this is what Google reads)

## Booking button

Edit **`config.json`**:

```json
{ "bookingUrl": "https://wa.me/254755406162", "contact": "Sleek Beauty Parlour" }
```

Leave `bookingUrl` as `""` to hide the Book button in the gallery. Then `./publish.sh`.

---

## What clients can do

- Read services and prices without calling
- Book straight to WhatsApp, or tap to call — from any section of the page
- Browse looks by **Tips / Builder Gel / Gumgel / Acrylics / Stickons**
- Tap the **heart** on any look to save it; the **Saved** filter shows them again
- Tap a photo for a full-screen view, swipe or arrow between looks
- Get directions via Google Maps

## Files

| File / folder | What it is |
|---|---|
| `index.html` | The website (home) |
| `lookbook/index.html` | The gallery page |
| `photos/originals/<category>/` | **Drop your full-size photos here** |
| `photos/` | Auto-generated web versions (don't edit) |
| `photos.json` | The gallery list — edit captions here |
| `config.json` | Booking link + contact |
| `qr/` | QR code + printable card |
| `sitemap.xml`, `robots.txt` | So Google can find the site |
| `build.py` / `publish.sh` | Build + publish |
| `.venv/` | Private photo tools, created on first publish (not committed) |

Cost: **$0** — hosted free on GitHub Pages.
