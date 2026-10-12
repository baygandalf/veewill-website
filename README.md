# Website source (do not upload this folder)

These files generate every page in `veewill-site/`. Keep them for future changes.
Prices are in `data.py` (copied from the app's `lib/pricing.ts`), shared header and
footer in `layout.py`, page text in `pages_a.py` and `pages_b.py`. `en.json` and
`fr.json` are the app's `en.ts` / `fr.ts` text (FAQ, contact, privacy, terms).

To rebuild after a change: `python3 build.py` (needs Python 3, no extra packages).
Easiest: give this folder to Claude with the change you want.
