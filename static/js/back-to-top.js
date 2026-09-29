export function initBackToTop() {
  const btn = document.querySelector(".back-to-top");
  const whatsapp = document.querySelector(".whatsapp-button");
  const footerBottom = document.querySelector(".footer__bottom");
  if (!btn && !whatsapp) return;

  let frameRequested = false;
  const syncControls = () => {
    frameRequested = false;
    const baseBottom = window.innerWidth < 640 ? 16 : 24;
    let safeBottom = baseBottom;
    if (footerBottom) {
      const rowTop = footerBottom.getBoundingClientRect().top;
      if (rowTop < window.innerHeight) safeBottom = Math.max(baseBottom, window.innerHeight - rowTop + 16);
    }
    if (whatsapp) whatsapp.style.bottom = `${safeBottom}px`;
    if (btn) btn.style.bottom = `${safeBottom + (whatsapp ? 68 : 0)}px`;
    if (btn) btn.hidden = window.scrollY < 400;
  };
  const scheduleSync = () => {
    if (frameRequested) return;
    frameRequested = true;
    window.requestAnimationFrame(syncControls);
  };

  window.addEventListener("scroll", scheduleSync, { passive: true });
  window.addEventListener("resize", scheduleSync);
  syncControls();

  if (btn) btn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
}
