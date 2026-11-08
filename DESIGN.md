---
name: Greek Roasters
description: Every Greek specialty coffee, priced per kilo, on one grocer's counter.
colors:
  espresso: "#2a1a11"
  espresso-2: "#3b261a"
  on-espresso: "#e9d7b6"
  on-espresso-2: "#bfa47c"
  ground: "#d2b78c"
  band: "#c7a87a"
  bag: "#f1e5cd"
  bag-line: "#c9b088"
  window: "#ffffff"
  ink: "#23170f"
  ink-2: "#4e3726"
  ink-3: "#5e4733"
  ochre: "#e2a62a"
  ochre-deep: "#b9811a"
  on-ochre: "#1f140c"
  olive: "#4c5a20"
  olive-soft: "#dfe1c3"
  terracotta: "#8f3621"
  terracotta-soft: "#f0d2c4"
  cherry: "#8e2433"
  cocoa: "#5b3a24"
typography:
  display:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "clamp(1.9rem, 1.3rem + 2.4vw, 3rem)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "1.7rem"
    fontWeight: 800
    lineHeight: 1.1
  price:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "1.7rem"
    fontWeight: 800
    lineHeight: 1
    letterSpacing: "-0.01em"
    fontFeature: "\"tnum\""
  title:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "1.28rem"
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "0.005em"
  nav:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "1.05rem"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "0.01em"
  body:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  body-small:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "0.88rem"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "0.82rem"
    fontWeight: 600
    lineHeight: 1
    letterSpacing: "0.04em"
  tag-unit:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "0.72rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.08em"
rounded:
  chip: "4px"
  control: "6px"
  menu: "8px"
  container: "10px"
  pill: "50%"
spacing:
  hair: "4px"
  tight: "6px"
  gap: "10px"
  pad: "14px"
  gutter: "16px"
components:
  nav-link:
    textColor: "{colors.on-espresso}"
    typography: "{typography.nav}"
    rounded: "{rounded.control}"
    padding: "8px 12px"
  nav-link-hover:
    backgroundColor: "{colors.espresso-2}"
  nav-link-active:
    textColor: "{colors.ochre}"
  kilo-tag:
    backgroundColor: "{colors.ochre}"
    textColor: "{colors.on-ochre}"
    typography: "{typography.price}"
    padding: "6px 12px 7px 22px"
  bag-card:
    backgroundColor: "{colors.bag}"
    textColor: "{colors.ink}"
    rounded: "{rounded.container}"
    padding: "{spacing.pad}"
  counter:
    backgroundColor: "{colors.bag}"
    rounded: "{rounded.container}"
    padding: "{spacing.pad}"
  input-field:
    backgroundColor: "{colors.window}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "9px 12px"
    height: "42px"
  chip:
    backgroundColor: "{colors.ground}"
    textColor: "{colors.ink}"
    rounded: "{rounded.chip}"
    padding: "2px 8px"
  chip-drop:
    backgroundColor: "{colors.olive-soft}"
    textColor: "{colors.olive}"
  chip-rise:
    backgroundColor: "{colors.terracotta-soft}"
    textColor: "{colors.terracotta}"
  chip-sold:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.bag}"
  button-primary:
    backgroundColor: "{colors.olive}"
    textColor: "{colors.bag}"
    rounded: "{rounded.control}"
    padding: "10px 16px"
  link-more:
    textColor: "{colors.olive}"
    padding: "6px 0"
---

# Design System: Greek Roasters

## Overview

**Creative North Star: "The Bakaliko Counter"**

The site is an old Greek grocer's shop where everything is sold by the kilo. An espresso-brown shop rail runs across the top, the floor is kraft-paper tan, and every coffee sits on the counter as a pale paper bag with a stitched seam and an ochre price tag hanging off its edge. The kilo price is the first thing you read on every bag, set in heavy condensed numerals on that tag, and directly under it a small graduated scale shows where the price sits in today's market, from olive (cheap) through ochre to terracotta (dear).

The density is a working shop, not a showroom: a full filter counter, a four-up grid of bags on desktop, everything scannable on a phone. Condensed grotesk carries the voice (prices, names, labels, navigation); a system UI face carries everything you read at length. Colour is earthy and warm throughout, with ochre reserved for price and the current place, olive for action and falling prices, terracotta for rising prices and stale data.

The world deliberately refuses the category default of a white e-commerce grid with a brown accent. White appears only as the "window" inside controls and behind product photos in dark mode, never as the ground.

**Key Characteristics:**
- Kraft ground, espresso rail, bag-paper cards with a dashed stitched seam.
- The ochre kilo tag with a punched hole, hung off the card's right edge, holds the headline price.
- A per-card market scale (olive to ochre to terracotta) with a tag-shaped marker.
- Condensed Fira Sans Extra Condensed for numerals and labels; system UI for body text.
- Tabular numerals wherever prices or counts line up.
- Full light and dark schemes from one token set; dark is roasted, not inverted grey.

## Colors

An earth palette of roasted browns and kraft paper, with three market colours (ochre, olive, terracotta) carrying meaning rather than decoration. Every token has a dark-scheme counterpart in the same CSS custom property (see the sidecar); the values below are the light scheme.

### Primary
- **Price-Tag Ochre** (ochre): the kilo tag, the scale marker, the active menu item and text selection. Ochre means "the price" or "you are here", nothing else.
- **Burnt Ochre** (ochre-deep): the deeper ochre for ochre-on-light needs; in dark it lifts to a brighter gold.
- **Tag Ink** (on-ochre): near-black numerals on the tag; it stays dark in both schemes because the tag stays ochre.

### Secondary
- **Grocer's Olive** (olive): the action colour (primary button, "See coffees" link, range and checkbox accent, caret) and the price-drop colour. Also the light-scheme focus ring.
- **Olive Paper** (olive-soft): the price-drop chip background.

### Tertiary
- **Terracotta** (terracotta): price rises and stale-data status; the dear end of the market scale.
- **Terracotta Paper** (terracotta-soft): the price-rise chip background.
- **Cherry** (cherry) and **Cocoa** (cocoa): flavour-profile dots only (fruity/floral and chocolate/nutty; balanced uses olive).

### Neutral
- **Espresso** (espresso): the sticky shop rail and the browser theme colour.
- **Espresso Crema** (espresso-2): hover and open-menu fill on the rail.
- **Kraft Type** (on-espresso) and **Faded Kraft** (on-espresso-2): text and chevrons on the rail.
- **Kraft Ground** (ground): the page floor; also the plain chip fill and dropdown hover.
- **Counter Band** (band): the title band under the rail, one step darker than the ground.
- **Bag Paper** (bag): cards, the filter counter, dropdown menus and the empty state.
- **Bag Seam** (bag-line): every 1px border and the dashed seam inside cards.
- **Window** (window): the field fill inside inputs and selects. It stays light in dark mode (warm cream) so controls read as lit shop windows.
- **Roast Ink** (ink), **Ink 2** (ink-2), **Ink 3** (ink-3): primary text, secondary text, and field labels and scale ticks.

### Named Rules
**The Market Colours Rule.** Ochre is price and place, olive is action and cheaper, terracotta is dearer and stale. Never use one of these three for the other's meaning, and never as decoration.

**The Kraft Floor Rule.** The page ground is kraft tan (light) or roasted brown (dark), never white or grey. White exists only inside controls.

## Typography

**Display Font:** Fira Sans Extra Condensed, self-hosted as "Fira XC" at 600/700/800 (with Arial Narrow, system-ui)
**Body Font:** system-ui stack (-apple-system, Segoe UI, Roboto)

**Character:** A tall, tight grocer's-sign condensed for everything that is a number, a name or a label, set against a neutral system face for anything read as a sentence. The condensed face lets a price like €128.50 sit big inside a small tag.

### Hierarchy
- **Display** (800, clamp 1.9rem to 3rem, 1.02): the page title in the counter band, balanced wrapping.
- **Headline** (800, 1.7rem, 1.1): group headings in grouped view, ruled underneath with a 2px ink line, count set beside it in a 600 1rem condensed.
- **Price** (800, 1.7rem, 1, tabular): the kilo-tag numeral. The ledger stats use the same face at 800 1.6rem (1.35rem on phones).
- **Title** (700, 1.28rem, 1.12): coffee and roaster names on cards.
- **Nav** (600, 1.05rem, 1.2): menu items and the result count. The brand is 800 1.45rem uppercase.
- **Body** (400, 16px, 1.5): lede (max 58ch), notes and copy. **Body small** (0.88rem) for subtitles, meta lines, bag options and fine print (max 75ch).
- **Label** (600, 0.82rem, 0.04em, uppercase): filter field labels only.
- **Tag unit** (700, 0.72rem, 0.08em, uppercase): "PER KG" under the tag numeral.

### Named Rules
**The Condensed Numeral Rule.** Prices, counts, sizes and names are set in the condensed face; prices and anything that lines up in columns use tabular numerals.

**The Sentences Are System Rule.** Anything read as a sentence (lede, notes, captions, fine print) stays in the system UI face. Condensed body copy is not part of this world.

## Layout

A single centred column (max 1200px, 16px side gutters) under a full-bleed sticky rail and a full-bleed counter band. The band holds the title, lede and "last weighed" line on the left and the ledger stats bottom-aligned on the right, wrapping beneath on narrow screens.

The filter counter is an auto-fit grid of 160px-minimum fields with the search spanning the full row. Cards sit in an auto-fill grid (272px minimum on the coffee list, 260px on roasters) with a 16px gap. Inside a card the rhythm is 10px between blocks; the bag options or facts are pushed to the bottom (margin-top auto) behind a dashed seam so prices align along the row.

Spacing steps are small and practical: 4, 6, 10, 14 and 16px, with larger section gaps (34px between groups, 26/22px band padding) used locally.

At 560px and below: the menu spreads across the full width, the filter counter collapses to one column and its controls fold into a "Filter and sort" disclosure laid out two-up, product photos switch from 4:3 to 3:2, and ledger numerals drop to 1.35rem.

## Elevation & Depth

Mostly flat, paper-on-counter depth. Cards and dropdown menus carry one soft, warm two-layer shadow; the filter counter and empty state are flat with a border. The kilo tag is the one object that lifts off its surface: a drop shadow follows its notched silhouette so it reads as a tag hung on the bag.

### Shadow Vocabulary
- **Paper lift** (`box-shadow: 0 1px 2px rgb(42 26 17 / 0.10), 0 6px 18px -8px rgb(42 26 17 / 0.30)`; dark: `0 1px 2px rgb(0 0 0 / 0.4), 0 8px 20px -10px rgb(0 0 0 / 0.7)`): cards and dropdown menus.
- **Hung tag** (`filter: drop-shadow(0 3px 4px rgb(42 26 17 / 0.35))`): the kilo tag only.
- **Punched hole** (`box-shadow: inset 0 1px 1px rgb(0 0 0 / 0.35)`): the tag's hole, filled with the bag colour.

### Named Rules
**The One Hung Object Rule.** Only the kilo tag casts a silhouette shadow. Everything else is either paper lift or flat.

## Shapes

Softly cut paper. Containers (cards, filter counter, empty state) are 10px; dropdown menus 8px; controls, menu items, photo frames and the button 6px; chips 4px. The kilo tag is the signature silhouette: a rectangle with a notched point on its left (clip-path polygon, 10px point) and a 7px round punched hole, overhanging the card's right edge by 6px. The scale marker repeats that shape in miniature (14 by 18px, pointed bottom, with a hole), outlined in ink.

Borders are always 1px in bag-seam colour; inside cards the seam is dashed, like a stitched bag. The active menu item has a 2px ochre underline (inset shadow) with its bottom corners squared.

## Components

### Buttons
Sparse. The shop is navigated by links and filters; the only button is "Clear filters" in the empty state.
- **Shape:** gently rounded (6px).
- **Primary:** olive fill, pale cream label in 700 1rem condensed, 10px 16px padding, no border.
- **Focus:** the global 2px focus outline, offset 2px.
- **Text link action ("See N coffees"):** olive, 700 1.02rem condensed, trailing arrow icon, underline on hover.

### Chips
- **Style:** 4px corners, 1px bag-seam border, kraft-ground fill, 0.8rem ink text, 2px 8px padding.
- **Flavour:** an 8px dot in cherry, cocoa or olive before the label.
- **Price change:** borderless, 600 weight: olive on olive paper with a down arrow for drops, terracotta on terracotta paper with an up arrow for rises.
- **Sold out:** inverted, ink fill with bag-paper text; the whole card drops to 0.62 opacity.

### Cards / Containers (the bag)
- **Corner Style:** 10px.
- **Background:** bag paper, 1px bag-seam border.
- **Shadow Strategy:** paper lift.
- **Internal Padding:** 14px, 10px between blocks.
- **Anatomy:** kilo tag hung top-right; product photo in a 6px frame (contained, multiplied onto the bag in light mode, set on a light window in dark mode); title and subtitle; market scale; chips; notes; bag options behind a dashed seam with sizes in bold condensed. Roaster cards swap the photo and options for a facts list (label left, tabular value right) and a status line.

### Inputs / Fields
- **Style:** 42px minimum height, window fill, 1px bag-seam border, 6px corners, 0.95rem text. Text is fixed dark ink so it stays legible on the window in both schemes. Selects use a custom chevron; search has a leading magnifier.
- **Labels:** the uppercase condensed label style, ink-3, 4px above the control.
- **Range and checkbox:** native, accent-colored olive; the range shows its live value right-aligned in its label row.
- **Focus:** 2px solid focus colour (olive light, ochre dark), offset 1px.

### Navigation
- **Style:** sticky espresso rail, 60px minimum height. Brand at left (ochre coffee-bean mark, 800 uppercase condensed), menu at right.
- **States:** kraft-type items; hover and open dropdowns fill espresso-2; the current page turns ochre with a 2px ochre underline. Focus outlines on the rail are ochre.
- **Dropdowns:** native details/summary with a chevron that rotates 180deg (0.2s, cubic-bezier(0.16, 1, 0.3, 1)); the menu is a bag-paper panel with paper lift, items in body face, hover kraft ground.
- **Mobile:** the menu spans the full width, items tighten to 8px padding.

### Kilo Tag (signature)
The headline price of every coffee and roaster. Ochre, notched left point, punched hole, overhanging the card edge with a hung shadow. Numeral in the price style; the unit ("per kg", "from, per kg") beneath in the tag-unit style, right-aligned.

### Market Scale (signature)
A 6px gradient bar (olive, ochre, terracotta) with ten ink-3 tick marks under it, and a miniature tag marker positioned at the coffee's percentile. The caption states the position in words ("Cheaper than 99% of coffees in stock", bold phrase in ink). It is omitted rather than faked when there is no price or no market.

## Do's and Don'ts

### Do:
- **Do** put the kilo price on an ochre kilo tag on every coffee and roaster card, in 800 condensed tabular numerals.
- **Do** keep ochre, olive and terracotta to their market meanings (The Market Colours Rule).
- **Do** use the dashed bag-seam line to separate a card's footer facts from its body.
- **Do** define every new colour as a custom property with both a light and a dark value.
- **Do** keep control text and borders legible on the light window fill in both schemes.
- **Do** show missing or stale data in words ("Not stated", stale status in terracotta) rather than hiding it.
- **Do** use stroked SVG icons (2px stroke, round caps, 1em) from the shared sprite.

### Don't:
- **Don't** use a white or grey page ground; the floor is kraft (The Kraft Floor Rule).
- **Don't** give any element other than the kilo tag a silhouette drop shadow (The One Hung Object Rule).
- **Don't** set sentences in the condensed face, or prices in the system face.
- **Don't** use ochre for buttons or links; action is olive.
- **Don't** add a hardcoded light-on-olive colour without checking it against the dark-scheme olive, which is light.
