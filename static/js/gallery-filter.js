export function initGalleryFilter() {
  document.querySelectorAll("[data-component='gallery-filter']").forEach((wrap) => {
    const buttons = wrap.querySelectorAll("[data-filter]");
    const items = [...wrap.querySelectorAll("[data-category]")];
    const pagination = wrap.querySelector("[data-gallery-pagination]");
    const previous = wrap.querySelector("[data-page-prev]");
    const next = wrap.querySelector("[data-page-next]");
    const status = wrap.querySelector("[data-page-status]");
    const pageSize = 9;
    let activeFilter = "all";
    let currentPage = 1;

    const render = (scroll = false) => {
      const matches = items.filter((item) => activeFilter === "all" || (item.dataset.category || "").split(" ").includes(activeFilter));
      const pages = Math.max(1, Math.ceil(matches.length / pageSize));
      currentPage = Math.min(Math.max(1, currentPage), pages);
      items.forEach((item) => { item.hidden = true; });
      matches.slice((currentPage - 1) * pageSize, currentPage * pageSize).forEach((item) => { item.hidden = false; });
      const empty = wrap.querySelector(".media-no-results");
      if (empty) empty.hidden = matches.length !== 0;
      if (pagination) pagination.hidden = pages <= 1;
      if (status) status.innerHTML = `Page <strong>${currentPage}</strong> of ${pages}`;
      if (previous) previous.disabled = currentPage <= 1;
      if (next) next.disabled = currentPage >= pages;
      if (scroll) wrap.querySelector(".media-grid")?.scrollIntoView({ behavior: "smooth", block: "start" });
    };

    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        activeFilter = btn.dataset.filter;
        currentPage = 1;
        buttons.forEach((b) => b.classList.remove("is-active"));
        btn.classList.add("is-active");
        render();
      });
    });
    previous?.addEventListener("click", () => { if (currentPage > 1) { currentPage -= 1; render(true); } });
    next?.addEventListener("click", () => { currentPage += 1; render(true); });
    render();
  });
}
