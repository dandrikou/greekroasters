const $ = (id) => document.getElementById(id);
const euro = (n) => (n == null ? "–" : "€" + n.toFixed(2));
const fields = ["q", "origin", "taste", "roast", "type", "roaster", "max", "stock", "sort"];
let data = { coffees: [], roasters: [] };

function fillSelect(id, values) {
  const select = $(id);
  [...new Set(values.filter(Boolean))].sort().forEach((v) => select.add(new Option(v, v)));
}

function change(c) {
  if (!c.previous_per_kg || !c.best_per_kg || c.previous_per_kg === c.best_per_kg) return 0;
  return (c.best_per_kg - c.previous_per_kg) / c.previous_per_kg;
}

function render() {
  const f = Object.fromEntries(fields.map((k) => [k, $(k).type === "checkbox" ? $(k).checked : $(k).value]));
  const max = Number(f.max);
  $("maxOut").textContent = max >= 200 ? "any" : "€" + max;
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
  const tpl = $("card");
  list.replaceChildren(...rows.map((c) => {
    const el = tpl.content.firstElementChild.cloneNode(true);
    if (!c.in_stock) el.classList.add("out");
    const a = el.querySelector("h3 a");
    a.href = c.url;
    a.textContent = c.name;
    el.querySelector(".sub").textContent = [c.roaster, [c.origin, c.region].filter(Boolean).join(", ")].filter(Boolean).join(" · ");
    el.querySelector(".kg strong").textContent = euro(c.best_per_kg);
    const chips = el.querySelector(".chips");
    const chip = (text, cls) => { const s = document.createElement("span"); s.className = "chip " + (cls || ""); s.textContent = text; chips.append(s); };
    const pct = change(c);
    if (pct) chip(`${pct < 0 ? "▼" : "▲"} ${Math.abs(pct * 100).toFixed(0)}% since last check`, pct < 0 ? "drop" : "rise");
    if (c.taste !== "Not stated") chip(c.taste, { "Fruity / floral": "fruity", "Chocolate / nutty": "choc", Balanced: "balanced" }[c.taste]);
    if (c.roast !== "Not stated") chip(c.roast + (c.roast_basis.startsWith("Inferred") ? "*" : "") + " roast");
    if (c.process) chip(c.process);
    if (c.type !== "Single origin") chip(c.type);
    if (!c.in_stock) chip("Sold out");
    el.querySelector(".notes").textContent = c.notes;
    el.querySelector(".opts").replaceChildren(...c.options.map((o) => {
      const li = document.createElement("li");
      li.innerHTML = `<b>${o.size_g ? (o.size_g >= 1000 ? o.size_g / 1000 + " kg" : o.size_g + " g") : "?"}</b> ${euro(o.price)}`;
      return li;
    }));
    return el;
  }));
  const params = new URLSearchParams();
  fields.forEach((k) => { const v = $(k).type === "checkbox" ? ($(k).checked ? "" : "0") : $(k).value; if (v && !(k === "max" && v === "200") && !(k === "sort" && v === "perkg")) params.set(k, v); });
  history.replaceState(null, "", params.toString() ? "?" + params : location.pathname);
}

function renderRoasters() {
  const label = { live: "Updated", previous: "Last good update", manual: "Checked by hand" };
  $("roasterRows").replaceChildren(...data.roasters.map((r) => {
    const tr = document.createElement("tr");
    const status = r.coffees ? `${label[r.source] || ""} ${r.last_checked || ""}` : "Not tracked yet";
    tr.innerHTML = `<td><a target="_blank" rel="noopener"></a></td><td></td><td>${r.coffees || 0}</td>
      <td>${euro(r.cheapest_per_kg)}</td><td>${euro(r.median_per_kg)}</td>
      <td>${r.free_shipping_eur ? "€" + r.free_shipping_eur + "+" : "–"}</td><td class="${r.source === "previous" ? "stale" : ""}"></td>`;
    const a = tr.querySelector("a");
    a.href = r.website;
    a.textContent = r.name;
    tr.children[1].textContent = r.city || "";
    tr.children[6].textContent = status;
    tr.children[6].title = r.note || r.error || "";
    return tr;
  }));
}

async function init() {
  const resp = await fetch("data/coffees.json", { cache: "no-cache" });
  data = await resp.json();
  const when = new Date(data.generated_at);
  $("updated").textContent = `Last updated ${when.toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" })} · ${data.roasters.filter((r) => r.coffees).length} roasters`;
  fillSelect("origin", data.coffees.map((c) => c.origin));
  fillSelect("taste", data.coffees.map((c) => c.taste));
  fillSelect("roast", data.coffees.map((c) => c.roast));
  fillSelect("type", data.coffees.map((c) => c.type));
  fillSelect("roaster", data.coffees.map((c) => c.roaster));
  const params = new URLSearchParams(location.search);
  fields.forEach((k) => { if (params.has(k)) { if ($(k).type === "checkbox") $(k).checked = params.get(k) !== "0"; else $(k).value = params.get(k); } });
  fields.forEach((k) => $(k).addEventListener("input", render));
  render();
  renderRoasters();
}

init().catch((err) => { $("count").textContent = "Couldn't load the coffee data: " + err.message; });
