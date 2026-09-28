export function initGalleryFilter() {
  document.querySelectorAll("[data-component='gallery-filter']").forEach((wrap) => {
    const buttons = wrap.querySelectorAll("[data-filter]");
    const items = wrap.querySelectorAll("[data-category]");

    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const filter = btn.dataset.filter;
        buttons.forEach((b) => b.classList.remove("is-active"));
        btn.classList.add("is-active");
        items.forEach((item) => {
          item.hidden = filter !== "all" && item.dataset.category !== filter;
        });
      });
    });
  });
}
