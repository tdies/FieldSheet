# ES2 Equipment Tags

Offline QR tags for HVAC equipment: the QR carries the unit's controllers, network IDs, and point-to-terminal list. The app (a PWA) renders it. No job data is ever hosted — only the renderer.

## Layout
- `tags/` — the app. Publish this folder with GitHub Pages.
- `tools/make_tag.py` — JSON → printable QR label PNG.
- `samples/` — AHU-34 record and generated labels.

## Publish
1. Push this repo to GitHub.
2. Settings → Pages → Deploy from branch → `main`, folder `/tags` (or move `tags/` contents to root / `docs`).
3. Your app URL is `https://<org>.github.io/<repo>/`. Put that in `tools/make_tag.py` (`DEFAULT_BASE`) so labels point at it.

## Make a label
```
pip install qrcode pillow
python3 tools/make_tag.py samples/AHU-34_tag.json
python3 tools/make_tag.py samples/AHU-34_tag.json --raw   # uncompressed; stock camera shows readable text
```
Compressed AHU-34 = QR version 23 (109 modules). Print at ≥ 0.5 mm/module → ~2.3" square plus quiet zone. Error correction M.

## Test without a printed tag
- **Open sample tag** button on the home screen.
- **Paste** — the textarea accepts the full URL, the `#...` payload, or raw JSON.
- Display `samples/AHU-34_tag.png` on a laptop screen and scan it with a phone (requires the app to be hosted over https; camera won't open from a local file).
- Locally: `cd tags && python3 -m http.server 8000`, open `http://localhost:8000` on the same machine (camera works on localhost).

## Tag format
`<base>#<payload>`. Payload prefix `z` = zlib + base64url of minified JSON; `j` = plain JSON.
Record: `v, unit, typ, job, sh[], rev, asb, ctl[{tag, mdl, role, di, mac, net, ip, exp}], pts[[controller, channel, name, type, cable, terminals]]`.
Types: TH, mA, V, DI, DO. Fields `asb`, `di`, `ip` are filled at checkout.
