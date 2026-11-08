const $ = (id) => document.getElementById(id);
const euro = (n) => (n == null ? "–" : "€" + n.toFixed(2));
let roasters = [];
let market = [];
const svg = (id) => `<svg class="icon" aria-hidden="true"><use href="#i-${id}"/></svg>`;

function render() {
  const q = $("rq").value.trim().toLowerCase();
  const by = {
    name: (a, b) => a.name.localeCompare(b.name),
    cheapest: (a, b) => (a.cheapest_per_kg ?? 1e9) - (b.cheapest_per_kg ?? 1e9),
    median: (a, b) => (a.median_per_kg ?? 1e9) - (b.median_per_kg ?? 1e9),
    count: (a, b) => (b.coffees || 0) - (a.coffees || 0),
  };
  const rows = roasters
    .filter((r) => !q || [r.name, r.city].join(" ").toLowerCase().includes(q))
    .sort(by[$("rsort").value]);
  const label = { live: "Updated", previous: "Last good update", manual: "Checked by hand" };
  const tpl = $("roasterCard");
  $("rcount").textContent = `${rows.length} of ${roasters.length} roasters`;
  $("roasterList").replaceChildren(...rows.map((r) => {
    const el = tpl.content.firstElementChild.cloneNode(true);
    if (!r.coffees) el.classList.add("out");
    const a = el.querySelector("h3 a");
    a.href = r.website;
    a.textContent = r.name;
    el.querySelector(".sub").textContent = r.city && r.city !== "Greece" ? r.city : "Greece";
    el.querySelector(".tag strong").textContent = euro(r.cheapest_per_kg);
    const facts = el.querySelector(".facts");
    [["Coffees", r.coffees || 0], ["Median per kg", euro(r.median_per_kg)],
     ["Free shipping", r.free_shipping_eur ? `from €${r.free_shipping_eur}` : "Not stated"]].forEach(([k, v]) => {
      const dt = document.createElement("dt"); dt.textContent = k;
      const dd = document.createElement("dd"); dd.textContent = v;
      facts.append(dt, dd);
    });
    const scale = el.querySelector(".scale");
    if (r.cheapest_per_kg == null || market.length < 2) {
      scale.remove();
    } else {
      // Where this roaster's cheapest kilo price (the number on its tag) sits among every coffee in stock.
      const cheaper = market.filter((v) => v < r.cheapest_per_kg).length / market.length;
      const dearer = market.filter((v) => v > r.cheapest_per_kg).length / market.length;
      scale.querySelector(".scale-mark").style.setProperty("--pos", ((cheaper + 1 - dearer) / 2 * 100).toFixed(1) + "%");
      const phrase = cheaper === 0 ? "Cheapest per kg in the market" : dearer >= cheaper ? `Cheaper than ${Math.floor(dearer * 100)}%` : `Dearer than ${Math.floor(cheaper * 100)}%`;
      scale.querySelector("b").textContent = phrase;
      if (cheaper === 0) scale.querySelector("b").nextSibling.textContent = "";
      scale.setAttribute("aria-label", `Cheapest coffee per kg: ${phrase.toLowerCase()}${cheaper === 0 ? "" : " of coffees in stock"}`);
    }
    const status = el.querySelector(".status");
    status.innerHTML = svg("clock") + "<span></span>";
    status.lastChild.textContent = r.coffees ? `${label[r.source] || ""} ${r.last_checked || ""}`.trim() : "Not tracked yet";
    if (r.source === "previous") status.classList.add("stale");
    status.title = r.note || r.error || "";
    const more = el.querySelector(".more");
    if (r.coffees) {
      more.href = "index.html?roaster=" + encodeURIComponent(r.name);
      more.innerHTML = `See ${r.coffees} coffee${r.coffees === 1 ? "" : "s"} ${svg("arrow")}`;
    } else {
      more.remove();
    }
    return el;
  }));
}

async function init() {
  const resp = await fetch("data/coffees.json", { cache: "no-cache" });
  const data = await resp.json();
  roasters = data.roasters;
  market = data.coffees.filter((c) => c.in_stock && c.best_per_kg != null).map((c) => c.best_per_kg);
  const when = new Date(data.generated_at);
  $("updated").innerHTML = `${svg("clock")} ${roasters.filter((r) => r.coffees).length} roasters with coffee online · last weighed ${when.toLocaleString("en-GB", { dateStyle: "medium", timeStyle: "short" })}`;
  ["rq", "rsort"].forEach((id) => $(id).addEventListener("input", render));
  render();
}

init().catch((err) => { $("roasterList").textContent = "Couldn't load the roaster data: " + err.message; });
