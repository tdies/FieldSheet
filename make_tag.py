#!/usr/bin/env python3
"""Build a printable QR label from a unit tag JSON.

usage: make_tag.py unit.json [--base URL] [--out label.png] [--raw]

The QR encodes  <base>#<payload>  where payload is the minified JSON,
zlib-compressed and base64url-encoded. --raw skips compression so the
stock camera app shows readable text on phones without the app.
"""
import argparse, base64, json, sys, zlib
import qrcode
from PIL import Image, ImageDraw, ImageFont

DEFAULT_BASE = "https://tdies.github.io/FieldSheet/"

def payload(rec: dict, raw: bool) -> str:
    s = json.dumps(rec, separators=(",", ":")).encode()
    if raw:
        return "j" + s.decode()          # 'j' prefix = plain JSON
    z = zlib.compress(s, 9)
    return "z" + base64.urlsafe_b64encode(z).decode().rstrip("=")  # 'z' = zlib+b64url

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--out")
    ap.add_argument("--raw", action="store_true")
    a = ap.parse_args()

    rec = json.load(open(a.json))
    url = a.base + "#" + payload(rec, a.raw)
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=4, box_size=8)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    # caption strip under the code
    unit = rec.get("unit", "")
    cap_h = 90
    w, h = img.size
    out = Image.new("RGB", (w, h + cap_h), "white")
    out.paste(img, (0, 0))
    d = ImageDraw.Draw(out)
    try:
        f1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 44)
        f2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except OSError:
        f1 = f2 = ImageFont.load_default()
    d.text((w / 2, h + 8), unit, fill="black", font=f1, anchor="mt")
    d.text((w / 2, h + 60), f"{rec.get('job','')}  sheets {'/'.join(rec.get('sh', []))}  rev {rec.get('rev','')}",
           fill="black", font=f2, anchor="mt")

    outp = a.out or f"{unit or 'tag'}_tag.png"
    out.save(outp)
    print(f"{outp}: QR version {qr.version}, {len(url)} chars, {w//8 - 8} modules")
    print(url)

if __name__ == "__main__":
    main()
