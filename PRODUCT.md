# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Specialty-coffee buyers in Greece, starting with the owner (Dimitri), who want to find the best deal on whole beans across Greek online roasters. They browse on phone and desktop, compare bags from many shops, and click through to the roaster's own shop to buy.

## Product Purpose
Greek Roasters collects every coffee from about 30 Greek online specialty roasters into one list, normalises prices to euros per kilo, and refreshes them automatically every day. Success means a visitor finds the cheapest good bean for their taste in under a minute, without opening 30 shop tabs.

## Positioning
The only place that puts all Greek specialty roasters side by side on price per kg, with daily price changes tracked. It is an independent comparison, not a shop: it sells nothing and links out to each roaster.

## Operating Context
- Data is scraped daily by GitHub Actions and published as a static GitHub Pages site (dandrikou.github.io/greekroasters).
- Pages: coffee list (index.html, with filters for origin, flavour profile, roast, type, roaster, max €/kg, in stock, plus grouping by origin or flavour and sorting) and a Roasters page (roasters.html).
- Menu labels are partly Greek (Αρχική) and partly English. Data includes Greek, English and Bulgarian product names.

## Capabilities and Constraints
- Static HTML/CSS/JS, no build step, no framework. The scraper writes data/coffees.json.
- Product photos come from the roasters' own shops, and they vary in quality and background.
- Many coffees lack a stated roast level, tasting notes or origin, so the interface must handle "Not stated" gracefully.

## Brand Commitments
- Name: "Greek Roasters".
- Dimitri asked (2026-11-08) for earth colours suited to a coffee-roasting business, replacing the current generic look.

## Evidence on Hand
Real, live data only: around 450 coffees, 32 roasters, prices, sizes, origins, tasting notes and product photos from the shops. There are no testimonials, user counts or partnerships, and none may be invented.

## Product Principles
1. Price per kilo is the headline fact on every coffee.
2. The roasters are the heroes; the site is a fair, neutral guide to them.
3. Honest about gaps: show when data is missing or stale instead of hiding it.
4. Fast to scan on a phone.
