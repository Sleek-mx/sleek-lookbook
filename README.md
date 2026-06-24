# Sleek Beauty Parlour — Lookbook

A free, QR-accessible style lookbook for salon clients.
**Live site:** https://sleek-mx.github.io/sleek-lookbook/

The QR code is permanent — print it once and it always points here.
Print-ready card: `qr/print-this-qr-card.png`

---

## How to add or change photos (the only thing you ever do)

1. Put your full-size photos into the **`photos/originals/`** folder
   (drag them in from Finder — iPhone HEIC, JPG and PNG all work).
2. Open Terminal in this folder and run:

   ```
   ./publish.sh
   ```

That's it. The script optimises every photo, rebuilds the gallery, and pushes
it live. Changes appear at the URL above in about a minute.

> First time only, you may need to make the script runnable:
> `chmod +x publish.sh`

## Naming, titles & categories (optional)

- New photos show up automatically with no caption, under the **All** filter.
- To add captions or group photos (Braids / Colour / Bridal / etc.), open
  **`photos.json`** and edit the `title` and `category` for each photo, then run
  `./publish.sh` again. Any category you type becomes a filter button on the site.

## Booking button & contact

Edit **`config.json`**:

```json
{
  "bookingUrl": "https://wa.me/2547XXXXXXXX",   // WhatsApp, Calendly, or leave "" to hide
  "contact": "Call us: 07XX XXX XXX"
}
```

Then `./publish.sh`.

---

## What's in here

| File / folder | What it is |
|---|---|
| `index.html` | The website (self-contained, loads instantly) |
| `photos/originals/` | **Drop your full-size photos here** |
| `photos/` | Auto-generated web-optimised versions (don't edit) |
| `photos.json` | The gallery list — edit titles/categories here |
| `config.json` | Booking link + contact line |
| `qr/` | Your QR code (PNG, SVG) + the printable card |
| `build.py` | Optimises photos & rebuilds the gallery |
| `publish.sh` | Build + push live in one command |

Cost: **$0** — hosted free on GitHub Pages.
