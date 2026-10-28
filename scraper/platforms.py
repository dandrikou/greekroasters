"""Shop adapters. Each returns a list of raw products:

    {"name", "url", "image", "text", "categories", "in_stock",
     "options": [{"size_g", "price", "in_stock"}]}

Prices are in euro. "text" is the plain-text description used for origin, process and notes.
"""
import html
import json
import re
from urllib.parse import urljoin

from .text import is_excluded, parse_size_g, strip_html

MAX_PAGES = 20


def _option(size_g, price, in_stock=True):
    return {"size_g": size_g, "price": round(float(price), 2), "in_stock": bool(in_stock)}


def _dedupe_options(options):
    """Keep the cheapest price per bag size (grind choices often repeat the same size)."""
    best = {}
    for opt in options:
        key = opt["size_g"]
        if key not in best or opt["price"] < best[key]["price"]:
            best[key] = opt
        elif opt["in_stock"]:
            best[key]["in_stock"] = True
    return sorted(best.values(), key=lambda o: (o["size_g"] is None, o["size_g"] or 0))


# --- Shopify -------------------------------------------------------------------------------------

def parse_shopify_product(product, base_url):
    name = product.get("title", "")
    if is_excluded(name, product.get("product_type", "")):
        return None
    text = strip_html(product.get("body_html", ""))
    options = []
    for variant in product.get("variants", []):
        if variant.get("price") in (None, "", "0.00"):
            continue
        grams = variant.get("grams") or None
        # Shops sometimes enter shipping weight wrongly (e.g. 270000 g), so only trust bag-like weights.
        size = parse_size_g(variant.get("title"), name) or (grams if grams and 30 <= grams <= 5000 else None)
        options.append(_option(size, variant["price"], variant.get("available", True)))
    if not options:
        return None
    known_sizes = {o["size_g"] for o in options if o["size_g"]}
    if len(known_sizes) == 1:
        # Grind-only variants of a single bag size.
        for o in options:
            o["size_g"] = o["size_g"] or next(iter(known_sizes))
    images = product.get("images") or []
    image = images[0].get("src", "") if images else ""
    if image and "cdn.shopify" in image:
        image += ("&" if "?" in image else "?") + "width=480"
    return {
        "name": name,
        "url": f"{base_url.rstrip('/')}/products/{product['handle']}",
        "image": image,
        "text": text,
        "tags": product.get("tags", []),
        "categories": [product.get("product_type", "")],
        "in_stock": any(o["in_stock"] for o in options),
        "options": _dedupe_options(options),
    }


def shopify(client, roaster):
    base = roaster["website"]
    url = f"{base.rstrip('/')}/collections/{roaster['collection']}/products.json"
    products = []
    for page in range(1, MAX_PAGES + 1):
        batch = client.get_json(url, params={"limit": 250, "page": page}).get("products", [])
        if not batch:
            break
        products.extend(p for p in (parse_shopify_product(b, base) for b in batch) if p)
        if len(batch) < 250:
            break
    return products


# --- WooCommerce Store API -------------------------------------------------------------------------

def _woo_price(prices):
    minor = int(prices.get("currency_minor_unit", 2))
    return int(prices["price"]) / (10 ** minor)


def _woo_size_attribute(attributes):
    """Return the attribute whose values look like bag sizes (e.g. 250g / 1kg), if any."""
    for attr in attributes or []:
        values = [t.get("name", "") for t in attr.get("terms", [])] or [attr.get("value", "")]
        if values and all(parse_size_g(v) for v in values):
            return attr
    return None


def parse_woo_product(product, variation_lookup=None):
    """variation_lookup(variation_id) -> Store API product dict, used for per-size prices."""
    name = strip_html(product.get("name", ""))
    categories = [c.get("name", "") for c in product.get("categories", [])]
    if is_excluded(name):
        return None
    text = strip_html(product.get("short_description", "")) + "\n" + strip_html(product.get("description", ""))
    attrs_text = "\n".join(
        f"{a.get('name')}: {', '.join(t.get('name', '') for t in a.get('terms', []))}"
        for a in product.get("attributes", [])
    )
    text = (text + "\n" + attrs_text).strip()
    options = []
    size_attr = _woo_size_attribute(product.get("attributes"))
    variations = product.get("variations") or []
    if variations and size_attr and variation_lookup:
        taxonomy = size_attr.get("taxonomy") or size_attr.get("name", "")
        seen_sizes = set()
        for var in variations:
            label = next((a.get("value", "") for a in var.get("attributes", [])
                          if a.get("name", "").lower() in (taxonomy.lower(), size_attr.get("name", "").lower())), "")
            # Variation values are slugs such as "250-gr", "1-kg" or "0-250-kg".
            size = parse_size_g(re.sub(r"(\d)-(\d)", r"\1.\2", label or "").replace("-", " "))
            if size is None:
                # Size isn't a variation choice (e.g. a fixed "Package: 250gr" attribute).
                term_sizes = {parse_size_g(t.get("name", "")) for t in size_attr.get("terms", [])}
                size = term_sizes.pop() if len(term_sizes) == 1 else parse_size_g(name)
            if size in seen_sizes:
                continue
            seen_sizes.add(size)
            detail = variation_lookup(var["id"])
            if detail and detail.get("prices", {}).get("price"):
                options.append(_option(size, _woo_price(detail["prices"]), detail.get("is_in_stock", True)))
    if not options and product.get("prices", {}).get("price"):
        size = parse_size_g(name, attrs_text, product.get("short_description", ""))
        options.append(_option(size, _woo_price(product["prices"]), product.get("is_in_stock", True)))
        price_range = product["prices"].get("price_range")
        if size_attr and price_range and price_range.get("max_amount") != price_range.get("min_amount"):
            # Couldn't price each size: record the range ends against the smallest and largest sizes.
            sizes = sorted(filter(None, (parse_size_g(t.get("name", "")) for t in size_attr.get("terms", []))))
            if len(sizes) >= 2:
                minor = int(product["prices"].get("currency_minor_unit", 2))
                options = [
                    _option(sizes[0], int(price_range["min_amount"]) / 10 ** minor, product.get("is_in_stock", True)),
                    _option(sizes[-1], int(price_range["max_amount"]) / 10 ** minor, product.get("is_in_stock", True)),
                ]
    if not options:
        return None
    images = product.get("images") or []
    return {
        "name": name,
        "url": product.get("permalink", ""),
        "image": (images[0].get("thumbnail") or images[0].get("src", "")) if images else "",
        "text": text,
        "categories": categories,
        "in_stock": any(o["in_stock"] for o in options),
        "options": _dedupe_options(options),
    }


def woocommerce(client, roaster):
    api = f"{roaster['website'].rstrip('/')}/wp-json/wc/store/v1/products"
    categories = roaster.get("categories") or [None]
    seen, products = set(), []

    def lookup(variation_id):
        try:
            return client.get_json(f"{api}/{variation_id}")
        except Exception:
            return None

    for category in categories:
        for page in range(1, MAX_PAGES + 1):
            params = {"per_page": 100, "page": page}
            if category:
                params["category"] = category
            batch = client.get_json(api, params=params)
            if not batch:
                break
            for item in batch:
                if item["id"] in seen:
                    continue
                seen.add(item["id"])
                parsed = parse_woo_product(item, lookup)
                if parsed:
                    products.append(parsed)
            if len(batch) < 100:
                break
    return products


# --- Any shop with schema.org Product JSON-LD ----------------------------------------------------

JSONLD_RE = re.compile(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', re.IGNORECASE | re.DOTALL)
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
META_DESC_RE = re.compile(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', re.IGNORECASE)
OG_IMAGE_RE = re.compile(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)', re.IGNORECASE)


def _jsonld_image(value):
    """schema.org image can be a URL, a list of URLs, or an ImageObject."""
    if isinstance(value, list):
        value = value[0] if value else ""
    if isinstance(value, dict):
        value = value.get("url") or value.get("contentUrl") or ""
    return value if isinstance(value, str) else ""


def _walk_jsonld(node):
    if isinstance(node, list):
        for item in node:
            yield from _walk_jsonld(item)
    elif isinstance(node, dict):
        if "@graph" in node:
            yield from _walk_jsonld(node["@graph"])
        yield node


def parse_jsonld_product(page_html, url):
    found = None
    for block in JSONLD_RE.findall(page_html):
        try:
            data = json.loads(block.strip())
        except json.JSONDecodeError:
            continue
        for node in _walk_jsonld(data):
            types = node.get("@type")
            types = types if isinstance(types, list) else [types]
            if "Product" in types or "ProductGroup" in types:
                found = node
                break
        if found:
            break
    if not found:
        return None
    name = strip_html(found.get("name", ""))
    if is_excluded(name):
        return None
    offers = found.get("offers") or []
    if isinstance(offers, dict):
        offers = offers.get("offers") or [offers]
    for variant in found.get("hasVariant", []) or []:
        sub = variant.get("offers") or {}
        sub = sub if isinstance(sub, list) else [sub]
        for o in sub:
            offers.append({**o, "name": variant.get("name", ""), "sku": variant.get("sku", "")})
    options = []
    for offer in offers:
        price = offer.get("price") or offer.get("lowPrice")
        if price in (None, ""):
            continue
        try:
            price = float(str(price).replace(",", "."))
        except ValueError:
            continue
        if price <= 0:
            continue
        size = parse_size_g(offer.get("name"), offer.get("sku"), name, found.get("weight", {}).get("value") if isinstance(found.get("weight"), dict) else None)
        in_stock = "OutOfStock" not in str(offer.get("availability", ""))
        options.append(_option(size, price, in_stock))
    if not options:
        return None
    description = strip_html(found.get("description", ""))
    meta = META_DESC_RE.search(page_html)
    text = description or (html.unescape(meta.group(1)) if meta else "")
    og = OG_IMAGE_RE.search(page_html)
    image = _jsonld_image(found.get("image")) or (html.unescape(og.group(1)) if og else "")
    return {
        "name": name,
        "url": url,
        "image": urljoin(url, image) if image else "",
        "text": text,
        "categories": [],
        "in_stock": any(o["in_stock"] for o in options),
        "options": _dedupe_options(options),
    }


def jsonld(client, roaster):
    pattern = re.compile(roaster["product_link_pattern"])
    links = []
    for listing in roaster["listing_pages"]:
        page = client.get_text(listing)
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', page)
        for href in hrefs:
            absolute = urljoin(listing, href)
            if pattern.fullmatch(absolute) and absolute not in links:
                links.append(absolute)
    products = []
    for link in links[:150]:
        try:
            parsed = parse_jsonld_product(client.get_text(link), link)
        except Exception:
            continue
        if parsed:
            products.append(parsed)
    return products


ADAPTERS = {"shopify": shopify, "woocommerce": woocommerce, "jsonld": jsonld}
