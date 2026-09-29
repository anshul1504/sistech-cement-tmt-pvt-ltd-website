export function initLeadershipCarousel() {
  document.querySelectorAll("[data-lead-carousel]").forEach((carousel) => {
    const track = carousel.querySelector("[data-lead-track]");
    const slides = [...carousel.querySelectorAll("[data-lead-slide]")];
    const section = carousel.closest(".lead-board");
    const previous = section?.querySelector("[data-lead-prev]");
    const next = section?.querySelector("[data-lead-next]");
    const current = section?.querySelector("[data-lead-current]");
    const dots = section?.querySelector("[data-lead-dots]");
    if (!track || slides.length < 2) return;

    let index = 0;
    let timer;
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const visibleCount = () => window.innerWidth < 700 ? 1 : window.innerWidth < 1000 ? 2 : 3;
    const lastIndex = () => Math.max(0, slides.length - visibleCount());
    const buttons = slides.map((slide, slideIndex) => {
      const button = document.createElement("button");
      button.type = "button";
      button.setAttribute("aria-label", `Show director ${slideIndex + 1}`);
      button.addEventListener("click", () => show(Math.min(slideIndex, lastIndex())));
      dots?.append(button);
      return button;
    });

    function show(nextIndex) {
      index = nextIndex > lastIndex() ? 0 : nextIndex < 0 ? lastIndex() : nextIndex;
      const offset = slides[index].offsetLeft - slides[0].offsetLeft;
      track.style.transform = `translateX(-${offset}px)`;
      slides.forEach((slide, slideIndex) => {
        const hidden = slideIndex < index || slideIndex >= index + visibleCount();
        slide.setAttribute("aria-hidden", String(hidden));
      });
      buttons.forEach((button, buttonIndex) => button.setAttribute("aria-current", String(buttonIndex === index)));
      if (current) current.textContent = String(index + 1).padStart(2, "0");
    }

    const stop = () => window.clearInterval(timer);
    const start = () => {
      stop();
      if (!reduceMotion) timer = window.setInterval(() => show(index + 1), 3800);
    };
    previous?.addEventListener("click", () => { show(index - 1); start(); });
    next?.addEventListener("click", () => { show(index + 1); start(); });
    carousel.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") show(index - 1);
      if (event.key === "ArrowRight") show(index + 1);
    });
    let startX = 0;
    carousel.addEventListener("touchstart", (event) => { startX = event.changedTouches[0].clientX; stop(); }, { passive: true });
    carousel.addEventListener("touchend", (event) => {
      const distance = event.changedTouches[0].clientX - startX;
      if (Math.abs(distance) > 45) show(index + (distance < 0 ? 1 : -1));
      start();
    }, { passive: true });
    carousel.addEventListener("mouseenter", stop);
    carousel.addEventListener("mouseleave", start);
    carousel.addEventListener("focusin", stop);
    carousel.addEventListener("focusout", start);
    window.addEventListener("resize", () => show(Math.min(index, lastIndex())));
    document.addEventListener("visibilitychange", () => document.hidden ? stop() : start());
    show(0);
    start();
  });
}
