export function initLightbox() {
  const groups = document.querySelectorAll("[data-component='lightbox']");
  if (!groups.length) return;

  const overlay = document.createElement("div");
  overlay.className = "lightbox-overlay";
  overlay.hidden = true;
  overlay.innerHTML = '<button class="lightbox-close" aria-label="Close">&times;</button><img alt="">';
  document.body.appendChild(overlay);
  const img = overlay.querySelector("img");

  function close() { overlay.hidden = true; }
  overlay.addEventListener("click", (e) => { if (e.target === overlay || e.target.closest(".lightbox-close")) close(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") close(); });

  groups.forEach((group) => {
    group.querySelectorAll("a").forEach((link) => {
      link.addEventListener("click", (e) => {
        e.preventDefault();
        img.src = link.href;
        img.alt = link.querySelector("img")?.alt || "";
        overlay.hidden = false;
      });
    });
  });
}
