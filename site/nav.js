// Highlights the current menu entry.
(() => {
  const params = new URLSearchParams(location.search);
  const page = location.pathname.endsWith("roasters.html") ? "roasters" : "home";
  const type = params.get("type");
  const current = page === "home" && type ? type : page;
  const link = document.querySelector(`[data-nav="${current}"]`);
  if (link) { link.classList.add("active"); link.setAttribute("aria-current", "page"); }
})();
