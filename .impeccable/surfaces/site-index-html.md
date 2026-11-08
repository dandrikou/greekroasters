---
version: 1
slug: "site-index-html"
primary_target: "site/index.html"
related_targets: ["site/roasters.html"]
---

# Coffee list and Roasters pages

Scope: site/index.html (coffee list) and site/roasters.html (roasters directory), sharing site/style.css. Visitor mode: Operate. Task: find the cheapest good bean for your taste, then click through to the roaster's shop. Constraints: static HTML/CSS/JS, live data only, no invented claims.

## Direction contract

THESIS: A risograph print shop's poster wall, where the coffee market is pinned up as two-colour prints and the kilo price is the loudest ink on every sheet. It refuses the category default of a white e-commerce grid with a brown accent. Pinned by Dimitri's reference image (2026-11-08).

OWN-WORLD: Cream paper ground with a fixed grain overlay. Three inks: fluorescent pink, riso blue and yellow, overprinted with multiply blending (screen in dark mode on navy paper). Blue ink text throughout. Fira Sans Extra Condensed in black weight for giant uppercase headings with a 3px pink misregistration offset, and the system UI face for body text. Cards are sheets with a pink keyline. Price tags are yellow blocks with blue numerals and a pink offset shadow.

STORY: The visitor sees the whole Greek market printed per kilo, narrows it by taste and origin (or jumps straight to Blends, Single Origin or Decaf from the menu), spots where each bean sits on the price scale, and goes to buy.

FIRST VIEWPORT: Left sidebar rail with the wordmark, a geometric mark (pink and yellow circles, blue mountain), the five-item menu and a taste legend. To the right, overprinted poster shapes behind a giant condensed title, a "last weighed" line and a ledger of coffees, roasters and cheapest per kg. Then the filter panel, and the card grid starts within the first viewport on desktop. On phones the rail becomes a top strip with a scrolling menu.

FORM: Pinned by the user's reference, so no new roll; the earlier roll (seed:522221a424807d9f, candidate 3, the kilo tag) is carried over only for its scale signature. Signature move kept from the previous round: under each price tag sits a three-ink scale bar (moved off the tag itself so the tag stays legible at phone width) marking where this coffee's €/kg sits among the coffees in stock. Taste is coded by shape (fruity = pink circle, chocolatey = blue triangle, balanced = yellow square).

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
