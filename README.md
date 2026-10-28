# Greek Roasters

A small website that compares specialty coffee beans from Greek online roasters by **price per kg**.
Prices refresh automatically every morning.

## How it works

| Part | What it does |
|---|---|
| `roasters.json` | The list of roasters, and how to read each shop |
| `scraper/` | Python scraper. Reads each shop and writes `data/coffees.json` |
| `data/seed.json` | Hand-checked details (origin, process, tasting notes) that fill gaps the shops leave |
| `data/history.csv` | Every price seen, one row per coffee, bag size and day |
| `site/` | The website: plain HTML, CSS and JavaScript, no build step |
| `.github/workflows/update.yml` | Runs the scraper daily at 04:15 UTC, commits the new prices and publishes the site |

### Shop types

- **shopify**: reads `/collections/<collection>/products.json`
- **woocommerce**: reads the WooCommerce Store API (`/wp-json/wc/store/v1/products`), filtered by category
- **jsonld**: opens the listing pages, follows product links and reads the schema.org product data on each page
- **manual**: not scraped. Prices come from `data/seed.json` and only change when edited by hand

If a shop fails on a given day, its coffees from the previous run are kept and the website shows when they were last updated.
The scraper respects each site's `robots.txt` and waits between requests.

## Run it locally

```bash
pip install -r requirements.txt
python -m pytest -q
python -m scraper.build                  # scrape every roaster
python -m scraper.build --only kudu      # refresh one roaster
python -m scraper.build --offline        # rebuild from the previous data and seed, no network
mkdir -p _site/data && cp site/* _site/ && cp data/coffees.json _site/data/
python -m http.server -d _site 8000      # open http://localhost:8000
```

## Add a roaster

Add an entry to `roasters.json`. For a Shopify shop, give its `collection`. For WooCommerce, give its `categories` (slugs).
For other shops, use `jsonld` with `listing_pages` and a `product_link_pattern`.

## One-time setup on GitHub

1. Settings → Pages → Source: **GitHub Actions**.
2. Actions → *Daily price update* → **Run workflow** to publish the first version.
