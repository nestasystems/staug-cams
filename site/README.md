# Watch St. Augustine — website pages

Everything for watchstaugustine.com besides the camera feed (which is the rest of this repo).

## What's here
- `pages/` — the 7 live pages, numbered in build order. Each goes into GoHighLevel at the address below.
- `PAGE-SEO.txt` — page title, meta description (≤155 chars) and keywords for each page, to paste into the builder's SEO boxes.
- `assets/badge.png` — the "Recommended on Watch St. Augustine" badge. Must live at https://watchstaugustine.com/badge.png
- `cards/` — print-ready leave-behind card (front = page 1, back = page 2) and its source.
- `tools/build.py` — generates pages 2–7 from one template. Edit the RESTAURANTS list, run `python3 build.py`, copy from `pages/`.
- `business-snippets.txt` — badge code + live-cam link to give each business.

## Page addresses (GoHighLevel funnel "Watch St. Augustine")
| File | Address |
|---|---|
| 1-home-page.html | https://watchstaugustine.com/ |
| 2-restaurants.html | https://watchstaugustine.com/restaurants |
| 3-about.html | https://watchstaugustine.com/about |
| 4-restaurant-ice-plant.html | https://watchstaugustine.com/ice-plant |
| 5-restaurant-17-king.html | https://watchstaugustine.com/17-king |
| 6-restaurant-the-floridian.html | https://watchstaugustine.com/the-floridian |
| 7-restaurant-la-nouvelle.html | https://watchstaugustine.com/la-nouvelle |

No trailing slashes. GoHighLevel doesn't support nested paths, so restaurant pages sit at the top level.

## Adding a restaurant
1. Add a dict to `RESTAURANTS` in `tools/build.py` (copy an existing one). Facts from the restaurant's own site; the story in Matt and Malena's words.
2. `python3 tools/build.py` — writes to `pages/` next to the script.
3. Create a new funnel step in GoHighLevel with the slug as its path, paste the page in, fill the SEO boxes.
4. Copy the regenerated Restaurants page in too (it lists every pick).

## The plan, in short
List first, then visit. Pages are free, no ads, no commissions. Malena visits each owner to tell them they made the list, hands them a card, collects two photos and a sentence, and books a 90-day follow-up with a traffic report. Working docs (visit checklist, tracker, report template) are in the Google Drive folder "Watch St. Augustine - Local Picks".
