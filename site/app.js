const $ = (id) => document.getElementById(id);
const euro = (n) => (n == null ? "–" : "€" + n.toFixed(2));
const fields = ["q", "origin", "taste", "roast", "type", "roaster", "max", "stock", "group", "sort"];
const TASTE_ORDER = ["Fruity / floral", "Balanced", "Chocolate / nutty", "Not stated"];
const TYPE_TITLES = { Blend: "Blends", "Single origin": "Single origin coffees", Decaf: "Decaf coffees" };
let data = { coffees: [], roasters: [] };
let market = []; // sorted €/kg of every in-stock coffee, for the price scale
const svg = (id) => `<svg class="icon" aria-hidden="true"><use href="#i-${id}"/></svg>`;

function bisect(v, strict) {
  let lo = 0, hi = market.length;
  while (lo < hi) { const mid = (lo + hi) >> 1; if (strict ? market[mid] < v : market[mid] <= v) lo = mid + 1; else hi = mid; }
  return lo;
}

// Where a price sits in today's market: position 0-1, and the share of coffees cheaper / dearer than it.
function standing(perKg) {
  if (perKg == null || market.length < 2) return null;
  const below = bisect(perKg, true), upTo = bisect(perKg, false);
  return { pos: (below + upTo) / 2 / market.length, cheaper: below / market.length, dearer: (market.length - upTo) / market.length };
}

function fillSelect(id, values) {
  const select = $(id);
  [...new Set(values.filter(Boolean))].sort().forEach((v) => select.add(new Option(v, v)));
}

function change(c) {
  if (!c.previous_per_kg || !c.best_per_kg || c.previous_per_kg === c.best_per_kg) return 0;
  return (c.best_per_kg - c.previous_per_kg) / c.previous_per_kg;
}

function card(c) {
  const tpl = $("card");
  const el = tpl.content.firstElementChild.cloneNode(true);
  if (!c.in_stock) el.classList.add("out");
  const a = el.querySelector("h3 a");
  a.href = c.url;
  a.textContent = c.name;
  const pic = el.querySelector(".pic");
  if (c.image) {
    pic.href = c.url;
    const img = pic.querySelector("img");
    img.addEventListener("error", () => { pic.remove(); el.querySelector(".head").prepend(el.querySelector(".tag")); });
    img.src = c.image;
  } else {
    pic.remove();
    el.querySelector(".head").prepend(el.querySelector(".tag")); // no photo: the tag floats beside the title
  }
  el.querySelector(".sub").textContent = [c.roaster, [c.origin === "Not stated" ? "" : c.origin, c.region].filter(Boolean).join(", ")].filter(Boolean).join(" · ");
  const tag = el.querySelector(".tag");
  if (c.best_per_kg != null) {
    tag.querySelector("strong").textContent = euro(c.best_per_kg);
  } else {
    tag.querySelector("strong").textContent = euro(c.cheapest_bag);
    tag.querySelector("span").textContent = "per bag";
  }
  const scale = el.querySelector(".scale");
  const st = standing(c.best_per_kg);
  if (!st) {
    scale.remove();
  } else {
    scale.querySelector(".scale-mark").style.setProperty("--pos", (st.pos * 100).toFixed(1) + "%");
    const b = scale.querySelector("b");
    let phrase;
    if (st.cheaper === 0) { phrase = "Cheapest"; b.nextSibling.textContent = " per kg in stock today"; }
    else if (st.dearer === 0) { phrase = "Dearest"; b.nextSibling.textContent = " per kg in stock today"; }
    else phrase = st.dearer >= st.cheaper ? `Cheaper than ${Math.floor(st.dearer * 100)}%` : `Dearer than ${Math.floor(st.cheaper * 100)}%`;
    b.textContent = phrase;
    scale.setAttribute("aria-label", `Price per kg: ${phrase.toLowerCase()}${b.nextSibling.textContent}`);
  }
  const chips = el.querySelector(".chips");
  const chip = (html, cls) => { const s = document.createElement("span"); s.className = "chip " + (cls || ""); s.innerHTML = html; chips.append(s); return s; };
  const text = (t) => t.replace(/[&<>]/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[ch]));
  const pct = change(c);
  if (pct) chip(`${svg(pct < 0 ? "down" : "up")} ${Math.abs(pct * 100).toFixed(0)}% since last check`, pct < 0 ? "drop" : "rise");
  if (!c.in_stock) chip("Sold out", "sold");
  if (c.taste !== "Not stated") chip(`<span class="dot"></span>${text(c.taste)}`, { "Fruity / floral": "fruity", "Chocolate / nutty": "choc", Balanced: "balanced" }[c.taste]);
  if (c.roast !== "Not stated") chip(text(c.roast + (c.roast_basis.startsWith("Inferred") ? "*" : "") + " roast"));
  if (c.process) chip(text(c.process));
  if (c.type !== "Single origin") chip(text(c.type));
  if (!chips.children.length) chips.remove();
  const notes = el.querySelector(".notes");
  if (c.notes) notes.textContent = c.notes; else notes.remove();
  el.querySelector(".opts").replaceChildren(...c.options.map((o) => {
    const li = document.createElement("li");
    li.innerHTML = `<b>${o.size_g ? (o.size_g >= 1000 ? o.size_g / 1000 + " kg" : o.size_g + " g") : "Bag"}</b> ${euro(o.price)}`;
    return li;
  }));
  return el;
}

function emptyState() {
  const div = document.createElement("div");
  div.className = "empty";
  div.innerHTML = "<p>No coffee matches all of these filters.</p>";
  const b = document.createElement("button");
  b.type = "button";
  b.textContent = "Clear filters";
  b.addEventListener("click", () => {
    fields.forEach((k) => { const el = $(k); if (el.type === "checkbox") el.checked = true; else if (k === "max") el.value = "200"; else if (k === "sort") el.value = "perkg"; else el.value = ""; });
    render();
  });
  div.append(b);
  return div;
}

function render() {
  const f = Object.fromEntries(fields.map((k) => [k, $(k).type === "checkbox" ? $(k).checked : $(k).value]));
  const max = Number(f.max);
  $("maxOut").textContent = max >= 200 ? "Any" : "€" + max;
  const q = f.q.trim().toLowerCase();
  let rows = data.coffees.filter((c) =>
    (!q || [c.name, c.notes, c.region, c.roaster, c.origin, c.process].join(" ").toLowerCase().includes(q)) &&
    (!f.origin || c.origin === f.origin) &&
    (!f.taste || c.taste === f.taste) &&
    (!f.roast || c.roast === f.roast) &&
    (!f.type || c.type === f.type) &&
    (!f.roaster || c.roaster === f.roaster) &&
    (!f.stock || c.in_stock) &&
    (max >= 200 || (c.best_per_kg != null && c.best_per_kg <= max))
  );
  const by = {
    perkg: (a, b) => (a.best_per_kg ?? 1e9) - (b.best_per_kg ?? 1e9),
    bag: (a, b) => (a.cheapest_bag ?? 1e9) - (b.cheapest_bag ?? 1e9),
    drop: (a, b) => change(a) - change(b),
    new: (a, b) => (b.first_seen || "").localeCompare(a.first_seen || ""),
    name: (a, b) => a.name.localeCompare(b.name),
  };
  rows.sort(by[f.sort]);
  $("count").textContent = `${rows.length} of ${data.coffees.length} coffees`;

  const list = $("list");
  if (!rows.length) {
    list.className = "grid";
    list.replaceChildren(emptyState());
  } else if (!f.group) {
    list.className = "grid";
    list.replaceChildren(...rows.map(card));
  } else {
    const groups = new Map();
    rows.forEach((c) => {
      const key = f.group === "taste" ? c.taste : c.origin;
      if (!groups.has(key)) groups.set(key, []);
      groups.get(key).push(c);
    });
    const keys = [...groups.keys()].sort(f.group === "taste"
      ? (a, b) => TASTE_ORDER.indexOf(a) - TASTE_ORDER.indexOf(b)
      : (a, b) => (a === "Not stated") - (b === "Not stated") || a.localeCompare(b));
    list.className = "groups";
    list.replaceChildren(...keys.map((key) => {
      const section = document.createElement("section");
      section.className = "group";
      const h = document.createElement("h2");
      const items = groups.get(key);
      const cheapest = Math.min(...items.map((c) => c.best_per_kg ?? Infinity));
      h.innerHTML = `<span></span> <small>${items.length} coffee${items.length === 1 ? "" : "s"}${isFinite(cheapest) ? " · from " + euro(cheapest) + "/kg" : ""}</small>`;
      h.firstChild.textContent = key;
      const grid = document.createElement("div");
      grid.className = "grid";
      grid.replaceChildren(...items.map(card));
      section.append(h, grid);
      return section;
    }));
  }
  const title = (TYPE_TITLES[f.type] || "Specialty coffee from Greek roasters") +
    (f.group === "origin" ? " by origin" : f.group === "taste" ? " by flavour profile" : "");
  $("pageTitle").textContent = title;
  document.title = f.type || f.group ? `${title} · Greek Roasters` : "Greek Roasters";
  const params = new URLSearchParams();
  fields.forEach((k) => { const v = $(k).type === "checkbox" ? ($(k).checked ? "" : "0") : $(k).value; if (v && !(k === "max" && v === "200") && !(k === "sort" && v === "perkg")) params.set(k, v); });
  history.replaceState(null, "", params.toString() ? "?" + params : location.pathname);
}

async function init() {
  const resp = await fetch("data/coffees.json", { cache: "no-cache" });
  data = await resp.json();
  const when = new Date(data.generated_at);
  $("updated").innerHTML = `${svg("clock")} Last weighed ${when.toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" })}`;
  market = data.coffees.filter((c) => c.in_stock && c.best_per_kg != null).map((c) => c.best_per_kg).sort((a, b) => a - b);
  const ledger = [
    [data.coffees.length, "coffees"],
    [data.roasters.filter((r) => r.coffees).length, "roasters"],
    [market.length ? euro(market[0]) : "–", "cheapest per kg"],
  ];
  $("ledger").replaceChildren(...ledger.map(([n, label]) => {
    const li = document.createElement("li");
    li.innerHTML = `<b></b>${label}`;
    li.firstChild.textContent = n;
    return li;
  }));
  fillSelect("origin", data.coffees.map((c) => c.origin));
  fillSelect("taste", data.coffees.map((c) => c.taste));
  fillSelect("roast", data.coffees.map((c) => c.roast));
  fillSelect("type", data.coffees.map((c) => c.type));
  fillSelect("roaster", data.coffees.map((c) => c.roaster));
  const params = new URLSearchParams(location.search);
  fields.forEach((k) => { if (params.has(k)) { if ($(k).type === "checkbox") $(k).checked = params.get(k) !== "0"; else $(k).value = params.get(k); } });
  fields.forEach((k) => $(k).addEventListener("input", render));
  const panel = $("filterPanel");
  const wide = matchMedia("(min-width: 561px)");
  const sync = () => { if (wide.matches) panel.open = true; };
  sync();
  wide.addEventListener("change", sync);
  const active = ["origin", "taste", "roast", "type", "roaster", "group"].filter((k) => $(k).value).length + ($("max").value !== "200") + (!$("stock").checked);
  if (active && !wide.matches) panel.open = true;
  render();
}

init().catch((err) => { $("count").textContent = "Couldn't load the coffee data: " + err.message; });
