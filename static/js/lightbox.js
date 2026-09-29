export function initLightbox() {
  const groups = document.querySelectorAll("[data-component='lightbox']");
  if (!groups.length) return;
  const overlay = document.createElement("div");
  overlay.className = "lightbox-overlay"; overlay.hidden = true;
  overlay.setAttribute("role", "dialog"); overlay.setAttribute("aria-modal", "true"); overlay.setAttribute("aria-label", "Media viewer");
  overlay.innerHTML = `<div class="lightbox-shell"><div class="lightbox-toolbar"><span class="lightbox-counter"></span><div><a class="lightbox-download" href="#" download>Download</a><button class="lightbox-close" type="button" aria-label="Close media viewer">&times;</button></div></div><div class="lightbox-stage"><button class="lightbox-nav lightbox-prev" type="button" aria-label="Previous media"><span aria-hidden="true">&#8592;</span><span class="lightbox-nav__label">Previous</span></button><div class="lightbox-media"></div><button class="lightbox-nav lightbox-next" type="button" aria-label="Next media"><span class="lightbox-nav__label">Next</span><span aria-hidden="true">&#8594;</span></button></div><div class="lightbox-info"><div><span class="lightbox-eyebrow">SISTECH Gallery</span><h2 class="lightbox-title"></h2><p class="lightbox-caption"></p></div><div class="lightbox-meta"></div></div></div>`;
  document.body.appendChild(overlay);
  const media = overlay.querySelector(".lightbox-media"); const title = overlay.querySelector(".lightbox-title"); const caption = overlay.querySelector(".lightbox-caption"); const meta = overlay.querySelector(".lightbox-meta"); const counter = overlay.querySelector(".lightbox-counter"); const download = overlay.querySelector(".lightbox-download");
  let currentItems = []; let currentIndex = 0; let lastTrigger = null;
  const itemData = (trigger) => trigger.matches("a") && !trigger.dataset.mediaSrc ? { type: "image", src: trigger.href, title: trigger.querySelector("img")?.alt || "Gallery image", caption: "", location: "", date: "", download: trigger.href } : { type: trigger.dataset.mediaType || "image", src: trigger.dataset.mediaSrc || "", title: trigger.dataset.title || "Gallery media", caption: trigger.dataset.caption || "", location: trigger.dataset.location || "", date: trigger.dataset.date || "", download: trigger.dataset.download || "" };
  function render(index) {
    currentIndex = (index + currentItems.length) % currentItems.length; const data = itemData(currentItems[currentIndex]); media.innerHTML = "";
    if (data.type === "image") { const image = document.createElement("img"); image.src = data.src; image.alt = data.title; media.appendChild(image); }
    else if (data.type === "video") { const video = document.createElement("video"); video.src = data.src; video.controls = true; video.autoplay = true; video.playsInline = true; media.appendChild(video); }
    else { const frame = document.createElement("iframe"); frame.src = `${data.src}?autoplay=1&rel=0`; frame.title = data.title; frame.allow = "autoplay; encrypted-media; picture-in-picture"; frame.allowFullscreen = true; media.appendChild(frame); }
    title.textContent = data.title; caption.textContent = data.caption; caption.hidden = !data.caption;
    meta.innerHTML = ""; [data.date, data.location].filter(Boolean).forEach((value) => { const tag = document.createElement("span"); tag.textContent = value; meta.appendChild(tag); }); counter.textContent = `${currentIndex + 1} / ${currentItems.length}`;
    download.hidden = !data.download; if (data.download) download.href = data.download;
    overlay.querySelectorAll(".lightbox-nav").forEach((button) => { button.hidden = currentItems.length < 2; });
  }
  function open(trigger, group) { currentItems = [...group.querySelectorAll("[data-lightbox-item], a")].filter((item) => !item.closest("[hidden]")); currentIndex = Math.max(0, currentItems.indexOf(trigger)); lastTrigger = trigger; overlay.hidden = false; document.body.classList.add("lightbox-open"); render(currentIndex); overlay.querySelector(".lightbox-close").focus(); }
  function close() { media.innerHTML = ""; overlay.hidden = true; document.body.classList.remove("lightbox-open"); lastTrigger?.focus(); }
  groups.forEach((group) => group.addEventListener("click", (event) => { const trigger = event.target.closest("[data-lightbox-item], a"); if (!trigger) return; event.preventDefault(); open(trigger, group); }));
  overlay.querySelector(".lightbox-close").addEventListener("click", close); overlay.querySelector(".lightbox-prev").addEventListener("click", () => render(currentIndex - 1)); overlay.querySelector(".lightbox-next").addEventListener("click", () => render(currentIndex + 1)); overlay.addEventListener("click", (event) => { if (event.target === overlay) close(); });
  let touchStartX = 0;
  media.addEventListener("touchstart", (event) => { touchStartX = event.changedTouches[0].clientX; }, { passive: true });
  media.addEventListener("touchend", (event) => { const distance = event.changedTouches[0].clientX - touchStartX; if (Math.abs(distance) < 50 || currentItems.length < 2) return; render(distance > 0 ? currentIndex - 1 : currentIndex + 1); }, { passive: true });
  document.addEventListener("keydown", (event) => { if (overlay.hidden) return; if (event.key === "Escape") close(); if (event.key === "ArrowLeft") render(currentIndex - 1); if (event.key === "ArrowRight") render(currentIndex + 1); });
}
