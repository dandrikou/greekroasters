---
name: Greek Roasters
description: The Greek specialty-coffee market, printed per kilo on a risograph poster wall.
colors:
  paper: "#f2e8d3"
  paper-2: "#ebdfc5"
  sheet: "#f8f1e2"
  field: "#fffaf0"
  riso-blue: "#2140b8"
  fluoro-pink: "#e43f7e"
  pink-ink: "#b8205a"
  pink-soft: "#fbd6e4"
  riso-yellow: "#f5c330"
  teal: "#0f6e60"
  teal-soft: "#d3eee6"
  ink: "#1f2f8f"
  ink-2: "#46508f"
  on-pink: "#ffffff"
  on-yellow: "#1f2f8f"
typography:
  display:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "clamp(2.6rem, 1.6rem + 4.2vw, 5.4rem)"
    fontWeight: 900
    lineHeight: 0.9
    letterSpacing: "-0.005em"
  wordmark:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "2.55rem"
    fontWeight: 900
    lineHeight: 0.86
    letterSpacing: "-0.01em"
  headline:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "2.3rem"
    fontWeight: 900
    lineHeight: 1
  title:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "1.4rem"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "0.005em"
  price:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "1.85rem"
    fontWeight: 900
    lineHeight: 0.95
    letterSpacing: "-0.005em"
    fontFeature: "\"tnum\" 1"
  nav:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "1.2rem"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "0.03em"
  label:
    fontFamily: "Fira XC, Arial Narrow, system-ui, sans-serif"
    fontSize: "0.85rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.05em"
  body:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  small:
    fontFamily: "system-ui, -apple-system, Segoe UI, Roboto, sans-serif"
    fontSize: "0.88rem"
    fontWeight: 400
    lineHeight: 1.4
rounded:
  none: "0px"
  dot: "50%"
spacing:
  xs: "6px"
  sm: "10px"
  md: "14px"
  lg: "18px"
  xl: "24px"
  2xl: "36px"
  section: "40px"
components:
  price-tag:
    backgroundColor: "{colors.riso-yellow}"
    textColor: "{colors.on-yellow}"
    typography: "{typography.price}"
    rounded: "{rounded.none}"
    padding: "6px 10px 7px"
  card:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "14px"
  chip:
    textColor: "{colors.riso-blue}"
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "2px 8px"
  chip-drop:
    backgroundColor: "{colors.teal-soft}"
    textColor: "{colors.teal}"
  chip-rise:
    backgroundColor: "{colors.pink-soft}"
    textColor: "{colors.pink-ink}"
  chip-sold:
    backgroundColor: "{colors.riso-blue}"
    textColor: "{colors.paper}"
  input-field:
    backgroundColor: "{colors.field}"
    textColor: "{colors.ink}"
    rounded: "{rounded.none}"
    padding: "9px 12px"
    height: "44px"
  button-primary:
    backgroundColor: "{colors.pink-ink}"
    textColor: "{colors.on-pink}"
    rounded: "{rounded.none}"
    padding: "12px 20px"
  nav-link:
    textColor: "{colors.riso-blue}"
    typography: "{typography.nav}"
    padding: "6px 0"
  nav-link-active:
    textColor: "{colors.pink-ink}"
  ledger-cell:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink-2}"
    typography: "{typography.label}"
    padding: "8px 14px 10px"
---

# Design System: Greek Roasters

## Overview

**Creative North Star: "The Riso Poster Wall"**

The site is a risograph print shop's wall with the Greek coffee market pinned up on it. Everything is printed in three inks (fluorescent pink, riso blue, sunflower yellow) on warm cream paper, overprinted with multiply blending so where two inks cross a third colour appears, and a fixed grain sheet lies over the whole print. Headings are giant black-weight condensed caps in blue with a pink plate printed a few pixels out of register. The kilo price is the loudest ink on every sheet: a yellow block with blue numerals.

Density is a working market list, not a showroom. A printed left rail carries the wordmark, a geometric mark, the menu and a shape legend; the page to the right opens with a poster header (overprinting circles, triangles and blocks behind the title) and then goes straight to filters and a tight card grid. Corners are square everywhere; rules are 1.5-2px ink lines. Depth only ever comes from ink: overprint, misregistration offset, grain. In dark mode the same press runs on navy paper, the inks lighten and blend by screen instead of multiply.

**Key Characteristics:**
- Cream paper (`paper`) under a fixed fractal-noise grain at 16% opacity (10% in dark).
- Three inks only, plus a teal signal ink reserved for "fresh" and "price dropped".
- Fira Sans Extra Condensed, uppercase, 700-900, for every heading, label, number and nav item; the system UI face for reading text.
- Pink misregistration (3px text-shadow on display type, 3-4px offset on the price tag) as the signature print artefact.
- Overprinting flat geometric shapes (circle, triangle, square/block) with `mix-blend-mode: multiply` (screen in dark).
- Square corners, 1.5-2px ink rules, no soft shadows, no gradients except the three-band price scale.

## Colors

A three-ink riso palette (pink, blue, yellow) printed on cream, with blue doubling as the text ink and a single teal reserved for good news.

### Primary
- **Riso Blue** (`riso-blue`): the main ink. Display and card headings, nav links, the wordmark, input and panel keylines, chip outlines, ledger numerals, the chocolate/nutty triangle. Dark scheme lifts it to a periwinkle (#7f95ff).
- **Fluorescent Pink** (`fluoro-pink`): the second plate. Misregistration shadow under display type, page rules (the rail's right edge, header and fine-print rules), card keylines, the price tag's offset, the scale's marker dot, the active-nav dot, the fruity circle, focus rings and range accent. Never used for body-size text on paper; that job belongs to Pink Ink.
- **Pink Ink** (`pink-ink`): the text-strength pink. Field labels, the "last weighed" meta line, active and hovered nav, grouped-view headings, "See coffees" links, stale-status text, the only filled button.

### Secondary
- **Sunflower Yellow** (`riso-yellow`): the price ink. The kilo price tag, the middle band of the price scale, the balanced square, selection highlight, and the large poster disc. Always carries blue numerals (`on-yellow`), never white.

### Tertiary
- **Signal Teal** (`teal`, with `teal-soft` fill): a functional fourth ink, outside the poster palette. Only the "price dropped" chip and the fresh-data status clock.
- **Pink Wash** (`pink-soft`): the fill behind the "price rose" chip.

### Neutral
- **Cream Paper** (`paper`): the page ground and the mobile rail strip. Dark scheme: navy #161a3a.
- **Kraft Shadow** (`paper-2`): photo well behind product images (images sit on it with multiply so white shop backgrounds drop out).
- **Fresh Sheet** (`sheet`): the lighter stock for cards, the filter panel, ledger cells and the empty state.
- **Field White** (`field`): input and select fill. Stays cream (#f2e8d3) in dark mode, so form fields always read as paper with navy text.
- **Navy Ink** (`ink`): body text and lede. In dark mode it inverts to cream.
- **Faded Ink** (`ink-2`): secondary text: subtitles, legend descriptions, figcaptions, fact labels, bag sizes.

### Named Rules
**The Three Inks Rule.** Decorative colour is pink, blue and yellow and nothing else. Teal is a signal, never a decoration; a fourth decorative hue breaks the press.

**The Overprint Rule.** Ink shapes that overlap blend with `multiply` on paper and `screen` on navy (`--blend`). The crossing colour is the point; never stack opaque shapes.

**The Yellow Carries Blue Rule.** Yellow is always printed with blue (`on-yellow`) on top. White or pink on yellow is never legible enough.

## Typography

**Display Font:** Fira Sans Extra Condensed, self-hosted as "Fira XC" in 600/700/800/900 (with Arial Narrow, system-ui fallback)
**Body Font:** system UI stack (system-ui, -apple-system, Segoe UI, Roboto)

**Character:** Poster caps against plain reading text. The condensed face does every job a print shop would set in wood type (titles, prices, labels, nav, counts); the system face handles sentences, notes and fine print so the long list stays fast to read on a phone.

### Hierarchy
- **Display** (900, clamp 2.6rem to 5.4rem, 0.9): page title only, uppercase, blue with a 3px pink misregistration text-shadow, `text-wrap: balance`. Blends with multiply on paper.
- **Wordmark** (900, 2.55rem desktop / 1.6rem in the mobile strip, 0.86): "Greek Roasters" in the rail, stacked on two lines on desktop.
- **Headline** (900, 2.3rem / 1.9rem on phones, 1): grouped-view section headings, uppercase, pink ink, ruled underneath in blue, with a 1rem blue count beside them.
- **Price** (900, 1.85rem, 0.95, tabular): the kilo price inside the yellow tag; ledger figures run the same weight at 1.9rem.
- **Title** (800, 1.4rem, 1.02): coffee and roaster names on cards, uppercase blue.
- **Nav** (700, 1.2rem desktop / 1.05rem mobile, 0.03em): rail menu, uppercase blue.
- **Label** (700, 0.85rem, 0.05em, uppercase): field labels in pink ink, chips and ledger captions in blue; the tag's "per kg" drops to 800 at 0.72rem with 0.08em tracking.
- **Body** (400, 16px, 1.5): lede (1.08rem, max 56ch), notes, check labels.
- **Small** (400, 0.82-0.9rem): subtitles, captions, facts, status lines, fine print (max 75ch).

### Named Rules
**The Misregistration Rule.** Only the display title gets the pink text plate (3px 3px 0). Smaller headings print in one ink; a doubled plate at card size turns to mush.

**The Condensed Caps Rule.** Anything that is a heading, number, label or button is Fira XC in uppercase at 700 or heavier. Sentences are never set in it.

## Layout

A two-column shell: a sticky 250px printed rail on the left, ruled off by a 2px pink line, and the page column to the right. Inside the page, content sits in a 1240px max wrap with 24px gutters. The header is a poster: title block (max 760px) left, the ledger of three figures bottom-right, and an absolutely placed shape cluster (`min(32vw, 380px)`) behind the title. Below it, a filter panel spanning the width (search on its own row, then auto-fit 160px columns), a count line, and an auto-fill card grid (min 270px, 260px on the roasters page, 18px gap). Grouped view stacks sections 40px apart.

Spacing rhythm runs on small, slightly irregular steps (6, 10, 14, 18, 24, 36px) rather than a strict 8-grid, as a print layout would.

Responsive: at 900px the rail collapses into a sticky top strip (small mark, one-line wordmark, wrapping horizontal menu; legend and rail note hidden), gutters drop to 16px and the poster shapes move to the right edge. At 560px the filters fold into a `details` disclosure ("Filter and sort") with a two-column body, photos go 3:2 and headings step down. All touch targets in the filter panel are at least 44px.

### Named Rules
**The Rail Rule.** Navigation lives in the left rail on desktop and becomes a top strip on phones; there is no separate header bar.

## Elevation & Depth

Flat print. There are no soft or ambient shadows anywhere. Depth comes from ink behaviour: shapes overprinting with multiply, one plate printed out of register, and the global grain overlay (fixed, `pointer-events: none`, z-index 100). The out-of-register offset is the only "shadow", always a second ink and always hard-edged.

### Shadow Vocabulary
- **Display misregistration** (`text-shadow: 3px 3px 0 var(--pink)`): the page title.
- **Mark misregistration** (`filter: drop-shadow(3px 2px 0 var(--pink))`): the mountain in the brand mark and the top shape of the poster cluster.
- **Tag offset** (`box-shadow: 4px 4px 0 var(--pink)`): the yellow price tag.
- **Button offset** (`box-shadow: 4px 4px 0 var(--blue)`, 2px on press): the pink-ink button.

### Named Rules
**The Second Plate Rule.** An offset is a second ink, never grey or black, never blurred, and never more than 4px.

## Shapes

Square corners throughout (0px): cards, tags, inputs, selects, chips, panels, buttons. The only round forms are ink dots: the scale marker, the active-nav dot, the fruity circle and the poster discs. Edges are drawn as ink keylines: 2px blue around panels, ledger cells and the rail note; 1.5px pink around cards and as internal card rules; 1.5px blue on inputs and chips; 2px pink for page-level rules; a 2px dashed pink border marks the empty state.

Taste is coded by shape and ink together: fruity/floral is a pink circle, chocolate/nutty a blue triangle, balanced a yellow square. The same three primitives (circle, triangle, rectangle) compose the brand mark and the per-page poster clusters, which vary between pages.

## Components

### Price Tag (signature)
A yellow ink block pinned to the top-right corner of each card, slightly out of register.
- **Shape:** square, 6px 10px 7px padding, right-aligned.
- **Color:** yellow fill, navy numerals (`on-yellow`), pink 4px offset.
- **Content:** the €/kg figure in Price type, "per kg" (or "from, per kg" on roasters) in micro caps below.
- **Placement:** absolute 24px from the card's top-right, over the photo; on photo-less roaster cards it floats right inside the heading block.

### Price Scale (signature)
A three-ink bar under each tag: blue, yellow, pink thirds (6px tall), with an 18px pink dot ringed 2.5px in blue placed at this coffee's percentile among coffees in stock. A small caption below reads "Cheaper than N% of coffees in stock" with the phrase in bold ink.

### Cards / Containers
- **Corner Style:** square.
- **Background:** fresh sheet on paper.
- **Shadow Strategy:** none (see Elevation).
- **Border:** 1.5px pink keyline; internal rules (bag options, facts) are 1.5px pink too.
- **Internal Padding:** 14px, 10px gap between blocks.
- **Photo well:** 4:3 (3:2 on phones), paper-2 ground, image contained and multiplied.
- **Out of stock / not tracked:** whole card at 60% opacity.

### Chips
- **Style:** square, 1.5px blue outline, condensed caps label in blue, 2px 8px padding.
- **Taste chips:** lead with an 11px shape dot in the taste's ink.
- **State chips:** price drop is teal on teal wash, price rise is pink ink on pink wash, sold out is paper on solid blue; state chips drop the outline. Arrow icons are inline SVG.

### Inputs / Fields
- **Style:** square, 1.5px blue stroke, field fill, navy text, 44px minimum height; search and select carry inline blue SVG glyphs (magnifier, chevron). Labels sit above in pink-ink caps.
- **Focus:** 2.5px pink outline, 1px offset.
- **Range and checkbox:** native controls tinted with `accent-color` (pink range, blue checkbox).
- **Panel:** fields live on a fresh-sheet panel with a 2px blue keyline and 16px padding (12px on phones).

### Buttons
- **Shape:** square, 12px 20px.
- **Primary:** pink-ink fill, white label in 800 condensed caps at 1.1rem, 4px blue offset; on press it moves 2px into the offset.
- **Text link ("See N coffees"):** pink-ink condensed caps with a 2px underline rule and an arrow; turns blue on hover.

### Navigation
- **Style:** rail menu of five items, uppercase condensed 700 in blue, 6px vertical padding, closed by a 2px pink rule.
- **Hover / Active:** pink ink; the active item gets a 9px pink dot before it and `aria-current="page"`.
- **Mobile:** a single wrapping row in the top strip at 1.05rem, 16px apart.

### Ledger
Three figure cells in the poster header (coffees, roasters, cheapest per kg): fresh sheet, 2px blue keyline, a 900-weight blue tabular figure over a caps caption.

### Taste Legend
The rail's key to the shape code: a 26px ink shape, the taste name in blue caps, a short description in faded ink. Hidden on phones.

## Do's and Don'ts

### Do:
- **Do** print every decorative mark in pink, blue or yellow, and let overlaps blend (`--blend`: multiply on paper, screen on navy).
- **Do** keep the kilo price in the yellow tag with blue numerals and the pink 4px offset, and keep the three-ink scale under it.
- **Do** set headings, numbers, labels, nav and buttons in Fira XC uppercase at 700-900; set sentences in the system face.
- **Do** keep corners square and draw edges as 1.5-2px ink keylines.
- **Do** use pink ink (`pink-ink`), not fluorescent pink, for any pink text.
- **Do** code taste by shape and ink together (pink circle, blue triangle, yellow square).
- **Do** keep form fields as cream paper with navy text in both schemes, at least 44px tall.

### Don't:
- **Don't** add soft, blurred, grey or black shadows; the only offset is a second ink of up to 4px.
- **Don't** round corners on cards, tags, chips, inputs or buttons.
- **Don't** use teal decoratively; it means fresh data or a price drop.
- **Don't** put the pink misregistration plate on anything smaller than the page title.
- **Don't** print white or pink text on yellow.
- **Don't** add gradients beyond the three-band price scale.
