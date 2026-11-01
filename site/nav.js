// Highlights the current menu entry and keeps only one dropdown open at a time.
(() => {
  const params = new URLSearchParams(location.search);
  const page = location.pathname.endsWith("roasters.html") ? "roasters" : "home";
  let current = page;
  if (page === "home" && params.get("group")) current = "single";
  else if (page === "home" && params.get("type")) current = "coffee";
  document.querySelector(`[data-nav="${current}"]`)?.classList.add("active");

  const drops = [...document.querySelectorAll(".drop")];
  drops.forEach((d) => d.addEventListener("toggle", () => {
    if (d.open) drops.forEach((o) => { if (o !== d) o.open = false; });
  }));
  document.addEventListener("click", (e) => {
    if (!e.target.closest(".drop")) drops.forEach((d) => { d.open = false; });
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") drops.forEach((d) => { d.open = false; });
  });
})();
