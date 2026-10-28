from scraper.build import enrich, url_key
from scraper.platforms import parse_jsonld_product, parse_shopify_product, parse_woo_product
from scraper.text import find_origin, find_process, is_excluded, parse_size_g, roast_level, taste_group

ROASTER = {"id": "test", "name": "Test Roaster"}


def test_parse_size_g():
    assert parse_size_g("Ethiopia Sheka Gr1 (200g)") == 200
    assert parse_size_g("1kg") == 1000
    assert parse_size_g("0,250 kg") == 250
    assert parse_size_g("250 gr") == 250
    assert parse_size_g("Κόκκοι Καφέ 150g") == 150
    assert parse_size_g("Колумбия 200.8 г") == 201
    assert parse_size_g("Default Title") is None


def test_exclusions_keep_coffee_drop_merch():
    assert is_excluded("Colombia Capsules")
    assert is_excluded("Coffee Drip Bag Ethiopia (10 pcs)")
    assert is_excluded("Cold Brew Can 250 ml")
    assert not is_excluded("Good Cup Specialty Coffee blend (250g)")
    assert not is_excluded("Ethiopia Gesha Village Oma")


def test_classifiers():
    assert find_origin("Ethiopia Kokosa Gr1") == "Ethiopia"
    assert find_origin("Καφές Brazil σε κόκκους") == "Brazil"
    assert find_origin("Колумбия by DABOV") == "Colombia"
    assert find_origin("Habit Specialty Coffee blend") == "Blend"
    assert find_process("Rwanda Shyira Washed") == "Washed"
    assert find_process("x", "Process: Anaerobic natural") == "Anaerobic"
    assert taste_group("jasmine, strawberry, blueberry, papaya") == "Fruity / floral"
    assert taste_group("dark chocolate, hazelnut, caramel") == "Chocolate / nutty"
    assert taste_group("") == "Not stated"
    assert roast_level("Medium-light") == ("Medium-light", "Stated")
    assert roast_level("Filter") == ("Light", "Inferred: filter roast")
    assert roast_level("", "Lighthouse Espresso Blend") == ("Medium", "Inferred: espresso roast")


def test_shopify_product():
    product = {
        "title": "Kenya Kiandu AA (250g)", "handle": "kenya-kiandu-aa", "product_type": "Single origin coffee",
        "body_html": "<p>Tasting notes: blackberry, red currant, toffee</p><p>Process: Washed</p>",
        "tags": ["africa"],
        "variants": [{"title": "Default Title", "price": "12.50", "available": True, "grams": 0}],
    }
    parsed = parse_shopify_product(product, "https://kudu.gr")
    assert parsed["url"] == "https://kudu.gr/products/kenya-kiandu-aa"
    assert parsed["options"] == [{"size_g": 250, "price": 12.5, "in_stock": True}]
    coffee = enrich(ROASTER, parsed, {}, {})
    assert coffee["origin"] == "Kenya"
    assert coffee["process"] == "Washed"
    assert coffee["notes"].startswith("blackberry")
    assert coffee["best_per_kg"] == 50.0


def test_woo_product_with_size_variations():
    product = {
        "id": 1, "name": "Brazil, Full Bloom, 200 g", "permalink": "https://www.underdog.gr/shop/full-bloom/",
        "short_description": "<p>Raisin, Milk Chocolate, Vanilla</p>", "description": "",
        "categories": [{"name": "Espresso"}],
        "prices": {"price": "1400", "currency_minor_unit": 2,
                   "price_range": {"min_amount": "1400", "max_amount": "4000"}},
        "is_in_stock": True,
        "attributes": [{"name": "Size", "taxonomy": "pa_size", "terms": [{"name": "200 g"}, {"name": "1 kg"}]}],
        "variations": [
            {"id": 11, "attributes": [{"name": "pa_size", "value": "200-g"}, {"name": "grind", "value": "beans"}]},
            {"id": 12, "attributes": [{"name": "pa_size", "value": "200-g"}, {"name": "grind", "value": "espresso"}]},
            {"id": 13, "attributes": [{"name": "pa_size", "value": "1-kg"}, {"name": "grind", "value": "beans"}]},
        ],
    }
    prices = {11: "1400", 13: "4000"}
    calls = []

    def lookup(vid):
        calls.append(vid)
        return {"prices": {"price": prices[vid], "currency_minor_unit": 2}, "is_in_stock": True}

    parsed = parse_woo_product(product, lookup)
    assert calls == [11, 13]
    assert [(o["size_g"], o["price"]) for o in parsed["options"]] == [(200, 14.0), (1000, 40.0)]


def test_woo_falls_back_to_price_range():
    product = {
        "id": 2, "name": "No 64 AA Kaguyu Kenya", "permalink": "https://theroosters.gr/product/no-64/",
        "short_description": "", "description": "", "categories": [],
        "prices": {"price": "1310", "currency_minor_unit": 2, "price_range": {"min_amount": "1310", "max_amount": "4645"}},
        "is_in_stock": True,
        "attributes": [{"name": "Βάρος", "terms": [{"name": "250gr"}, {"name": "1kg"}]}],
        "variations": [],
    }
    parsed = parse_woo_product(product, None)
    assert [(o["size_g"], o["price"]) for o in parsed["options"]] == [(250, 13.1), (1000, 46.45)]


def test_jsonld_product():
    page = """<html><script type="application/ld+json">{"@context":"https://schema.org","@graph":[
      {"@type":"Product","name":"Guatemala Santa Felisa Red Pacamara Natural 250g",
       "description":"Notes: red cherry, strawberry, vanilla",
       "offers":{"@type":"Offer","price":"14.80","availability":"https://schema.org/InStock"}}]}</script></html>"""
    parsed = parse_jsonld_product(page, "https://mokka.coffee/en/p/x/")
    assert parsed["options"] == [{"size_g": 250, "price": 14.8, "in_stock": True}]
    assert enrich(ROASTER, parsed, {}, {})["origin"] == "Guatemala"


def test_seed_details_override_heuristics():
    raw = {"name": "La Lindosa", "url": "https://www.sambacafe.gr/en/product/la-lindosa/", "text": "",
           "categories": [], "in_stock": True, "options": [{"size_g": 250, "price": 16.5, "in_stock": True}]}
    seed = {url_key("https://www.sambacafe.gr/product/la-lindosa/"): {"origin": "Colombia", "process": "Natural",
            "notes": "blueberry, raisin", "roast": "Espresso"}}
    coffee = enrich(ROASTER, raw, seed, {})
    assert (coffee["origin"], coffee["process"], coffee["roast"]) == ("Colombia", "Natural", "Medium")


def test_per_size_listings_merge_into_one_coffee():
    from scraper.build import merge_same_coffee
    raw = [
        {"name": "Porto Guatemala Single Origin Κόκκος 250gr", "url": "u1", "in_stock": True,
         "options": [{"size_g": 250, "price": 8.7, "in_stock": True}]},
        {"name": "Porto Guatemala Single Origin Κόκκος 1kg", "url": "u2", "in_stock": True,
         "options": [{"size_g": 1000, "price": 33.0, "in_stock": True}]},
    ]
    merged = merge_same_coffee(raw)
    assert len(merged) == 1
    assert [o["size_g"] for o in merged[0]["options"]] == [250, 1000]


def test_woo_fixed_package_size_and_grind_variations():
    product = {
        "id": 3, "name": "KENYA KANJATHI AA", "permalink": "https://www.contecoffeeroasters.com/en/x/",
        "short_description": "", "description": "", "categories": [],
        "prices": {"price": "1400", "currency_minor_unit": 2}, "is_in_stock": True,
        "attributes": [
            {"name": "Milling", "terms": [{"name": "V60"}, {"name": "Whole Beans"}]},
            {"name": "Package", "terms": [{"name": "250gr"}]},
        ],
        "variations": [{"id": 31, "attributes": [{"name": "Milling", "value": None}]}],
    }
    parsed = parse_woo_product(product, lambda vid: {"prices": {"price": "1400", "currency_minor_unit": 2}, "is_in_stock": True})
    assert [(o["size_g"], o["price"]) for o in parsed["options"]] == [(250, 14.0)]


def test_bilingual_listings_merge_and_merch_is_dropped():
    from scraper.build import name_key
    assert name_key("aracacu – brazil – 250g – coffee") == name_key("aracacu – brazil – 250g – καφές")
    assert is_excluded("33% double choco drink powder mix – republic® – 750g")
    assert is_excluded("earl grey μαύρο τσάι")
    assert not is_excluded("Bildimoo Danche, Ethiopia (Filter)")
    assert not is_excluded("Ritual Filter Blend")


def test_product_images_are_captured():
    shop = parse_shopify_product({
        "title": "Kenya AA 250g", "handle": "kenya-aa", "body_html": "",
        "images": [{"src": "https://cdn.shopify.com/s/files/1/kenya.jpg?v=1"}],
        "variants": [{"title": "Default Title", "price": "12.50", "available": True}],
    }, "https://kudu.gr")
    assert shop["image"] == "https://cdn.shopify.com/s/files/1/kenya.jpg?v=1&width=480"
    woo = parse_woo_product({
        "id": 4, "name": "Brazil 250g", "permalink": "https://x.gr/p/", "categories": [],
        "prices": {"price": "1200", "currency_minor_unit": 2}, "is_in_stock": True,
        "images": [{"src": "https://x.gr/big.jpg", "thumbnail": "https://x.gr/small.jpg"}],
    })
    assert woo["image"] == "https://x.gr/small.jpg"
    page = """<script type="application/ld+json">{"@type":"Product","name":"Peru 250g",
      "image":[{"@type":"ImageObject","url":"/img/peru.jpg"}],"offers":{"price":"11"}}</script>"""
    assert parse_jsonld_product(page, "https://mokka.coffee/en/p/peru/")["image"] == "https://mokka.coffee/img/peru.jpg"
    page = """<meta property="og:image" content="https://d.coffee/a.png">
      <script type="application/ld+json">{"@type":"Product","name":"Peru 250g","offers":{"price":"11"}}</script>"""
    assert parse_jsonld_product(page, "https://d.coffee/product/peru")["image"] == "https://d.coffee/a.png"
    assert enrich(ROASTER, shop, {}, {})["image"] == shop["image"]


def test_shopify_ignores_bogus_variant_weight():
    parsed = parse_shopify_product({
        "title": "Amazon Organic Blend", "handle": "amazon", "body_html": "",
        "variants": [{"title": "Κόκκοι", "price": "12.00", "available": True, "grams": 270},
                     {"title": "Φίλτρου", "price": "12.00", "available": True, "grams": 270000}],
    }, "https://www.earthcoffeeco.shop")
    assert parsed["options"] == [{"size_g": 270, "price": 12.0, "in_stock": True}]
