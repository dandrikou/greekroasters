"""Daily update: scrape every roaster, merge with curated details, and write data/coffees.json.

Run with:  python -m scraper.build
"""
import argparse
import csv
import datetime as dt
import json
import re
import sys
import traceback
from pathlib import Path
from urllib.parse import unquote, urlsplit

from .http import Client
from .platforms import ADAPTERS
from .text import SIZE_RE, find_notes, find_origin, find_process, find_type, roast_level, taste_group

ROOT = Path(__file__).resolve().parent.parent
ROASTERS_FILE = ROOT / "roasters.json"
SEED_FILE = ROOT / "data" / "seed.json"
OUTPUT_FILE = ROOT / "data" / "coffees.json"
HISTORY_FILE = ROOT / "data" / "history.csv"


def url_key(url):
    path = unquote(urlsplit(url or "").path).lower().rstrip("/")
    path = re.sub(r"^/(en|el)(?=/)", "", path)
    return path


def name_key(name):
    """Name without bag size or 'beans' words, so the 250 g and 1 kg listings of one coffee match."""
    text = SIZE_RE.sub(" ", name.lower())
    text = re.sub(r"\b(κόκκος|κόκκοι|κοκκοι|σε κόκκους|καφές|καφέ|οργανικός|organic|coffee|whole ?beans?|beans)\b|[()|,\-–]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def slug(text):
    return re.sub(r"[^a-z0-9α-ωа-я]+", "-", text.lower()).strip("-")[:80]


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def per_kg(option):
    if option.get("size_g") and option.get("price"):
        return round(option["price"] / option["size_g"] * 1000, 2)
    return None


def enrich(roaster, raw, seed_by_url, seed_by_name):
    """Combine a scraped product with curated seed details (curated wins where it has a value)."""
    raw = {**raw, "name": " ".join(raw["name"].split())}
    curated = seed_by_name.get(name_key(raw["name"])) or seed_by_url.get(url_key(raw["url"])) or {}
    text = raw.get("text", "")
    tags_text = " ".join(raw.get("tags", []))
    origin = curated.get("origin") or find_origin(raw["name"], text)
    process = curated.get("process") or find_process(raw["name"], text + "\n" + tags_text)
    notes = curated.get("notes") or find_notes(text)
    roast, basis = roast_level(curated.get("roast", ""), raw["name"], text + " " + " ".join(raw.get("categories", [])))
    options = []
    for opt in raw["options"]:
        size = opt.get("size_g") or curated.get("size_g")
        options.append({**opt, "size_g": size, "per_kg": per_kg({**opt, "size_g": size})})
    priced = [o for o in options if o["per_kg"]]
    in_stock_priced = [o for o in priced if o["in_stock"]] or priced
    best = min(in_stock_priced, key=lambda o: o["per_kg"]) if in_stock_priced else None
    return {
        "id": f"{roaster['id']}:{slug(name_key(raw['name'])) or url_key(raw['url'])}",
        "roaster_id": roaster["id"],
        "roaster": roaster["name"],
        "name": raw["name"],
        "origin": origin or "Not stated",
        "region": curated.get("region", ""),
        "type": find_type(raw["name"], origin, process),
        "process": process,
        "notes": notes,
        "taste": taste_group(notes),
        "roast": roast,
        "roast_basis": basis,
        "url": raw["url"],
        "in_stock": raw["in_stock"],
        "options": options,
        "best_per_kg": best["per_kg"] if best else None,
        "cheapest_bag": min((o["price"] for o in options), default=None),
    }


def index_seed(seed):
    """Index curated rows by name, and by URL only where a URL belongs to a single coffee."""
    by_url, by_name, url_names = {}, {}, {}
    for item in seed:
        key = (item["roaster_id"], url_key(item["url"]))
        url_names.setdefault(key, set()).add(name_key(item["name"]))
        by_url.setdefault(key, item)
        by_name.setdefault((item["roaster_id"], name_key(item["name"])), item)
    by_url = {k: v for k, v in by_url.items() if len(url_names[k]) == 1}
    return by_url, by_name


def merge_same_coffee(raw_products):
    """Shops that list each bag size as its own product become one coffee with several options."""
    merged = {}
    for product in raw_products:
        key = name_key(product["name"])
        if key in merged:
            target = merged[key]
            target["options"] = sorted(target["options"] + product["options"], key=lambda o: o.get("size_g") or 0)
            target["in_stock"] = target["in_stock"] or product["in_stock"]
        else:
            merged[key] = {**product, "options": list(product["options"])}
    return list(merged.values())


def seed_products(roaster_id, seed):
    """Turn seed rows into raw products, for roasters we can't scrape (prices as last checked by hand)."""
    grouped = {}
    for item in seed:
        if item["roaster_id"] != roaster_id:
            continue
        key = (item["name"], item["url"])
        product = grouped.setdefault(key, {
            "name": item["name"], "url": item["url"], "text": "", "categories": [],
            "in_stock": not item.get("sold_out"), "options": [],
        })
        if item.get("price"):
            product["options"].append({"size_g": item.get("size_g"), "price": item["price"], "in_stock": not item.get("sold_out")})
    return [p for p in grouped.values() if p["options"]]


def run(only=None, offline=False):
    today = dt.date.today().isoformat()
    roasters = load_json(ROASTERS_FILE, [])
    seed = load_json(SEED_FILE, [])
    previous = load_json(OUTPUT_FILE, {"coffees": [], "roasters": []})
    prev_coffees = {c["id"]: c for c in previous.get("coffees", [])}
    prev_status = {r["id"]: r for r in previous.get("roasters", [])}
    seed_by_url, seed_by_name = index_seed(seed)
    client = Client()

    coffees, statuses = [], []
    for roaster in roasters:
        rid = roaster["id"]
        if only and rid not in only:
            coffees.extend(c for c in prev_coffees.values() if c["roaster_id"] == rid)
            statuses.append(prev_status.get(rid, {"id": rid}))
            continue
        s_url = {k[1]: v for k, v in seed_by_url.items() if k[0] == rid}
        s_name = {k[1]: v for k, v in seed_by_name.items() if k[0] == rid}
        status = {key: roaster.get(key) for key in ("id", "name", "city", "website", "free_shipping_eur", "note")}
        adapter = ADAPTERS.get(roaster["platform"])
        error = None
        raw = []
        if adapter and not offline:
            try:
                raw = adapter(client, roaster)
            except Exception as exc:  # one broken shop must not stop the others
                error = f"{type(exc).__name__}: {exc}"
                traceback.print_exc(file=sys.stderr)
        if raw:
            items = [enrich(roaster, r, s_url, s_name) for r in merge_same_coffee(raw)]
            status.update(source="live", last_checked=today, error=None)
        else:
            carried = [c for c in prev_coffees.values() if c["roaster_id"] == rid]
            if carried:
                items = carried
                status.update(source="previous", last_checked=prev_status.get(rid, {}).get("last_checked"))
            else:
                items = [enrich(roaster, r, s_url, s_name) for r in merge_same_coffee(seed_products(rid, seed))]
                status.update(source="manual", last_checked=max((i.get("checked", "") for i in seed if i["roaster_id"] == rid), default=None))
            status["error"] = error or (None if (not adapter or offline) else "no products found")
        for item in items:
            old = prev_coffees.get(item["id"])
            item["first_seen"] = (old or {}).get("first_seen", today)
            item["previous_per_kg"] = (old or {}).get("best_per_kg") if status["source"] == "live" else (old or {}).get("previous_per_kg")
            if item.get("best_per_kg") and item.get("previous_per_kg") and item["previous_per_kg"] != item["best_per_kg"] and status["source"] == "live":
                item["price_changed_on"] = today
            else:
                item["price_changed_on"] = (old or {}).get("price_changed_on")
        status["coffees"] = len(items)
        per = sorted(i["best_per_kg"] for i in items if i.get("best_per_kg") and i.get("in_stock"))
        status["cheapest_per_kg"] = per[0] if per else None
        status["median_per_kg"] = per[len(per) // 2] if per else None
        statuses.append(status)
        coffees.extend(items)
        print(f"{rid:12} {status['source']:8} {len(items):4} coffees {status.get('error') or ''}")

    coffees.sort(key=lambda c: (c["best_per_kg"] is None, c["best_per_kg"] or 0))
    output = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"),
              "roasters": statuses, "coffees": coffees}
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=1), encoding="utf-8")
    append_history(today, coffees, {s["id"] for s in statuses if s.get("source") == "live"})
    return output


def append_history(today, coffees, live_ids):
    new_file = not HISTORY_FILE.exists()
    existing = set()
    if not new_file:
        with HISTORY_FILE.open(encoding="utf-8") as f:
            existing = {(r["date"], r["coffee_id"], r["size_g"]) for r in csv.DictReader(f)}
    with HISTORY_FILE.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["date", "roaster_id", "coffee_id", "size_g", "price", "in_stock"])
        for c in coffees:
            if c["roaster_id"] not in live_ids:
                continue
            for o in c["options"]:
                key = (today, c["id"], str(o.get("size_g") or ""))
                if key in existing:
                    continue
                writer.writerow([today, c["roaster_id"], c["id"], o.get("size_g") or "", o["price"], int(o["in_stock"])])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="*", help="roaster ids to refresh; others keep their previous data")
    parser.add_argument("--offline", action="store_true", help="don't scrape; rebuild from previous data and seed")
    args = parser.parse_args()
    run(only=set(args.only) if args.only else None, offline=args.offline)


if __name__ == "__main__":
    main()
