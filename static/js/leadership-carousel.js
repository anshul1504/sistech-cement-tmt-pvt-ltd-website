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
    const buttons = slides.map((slide, slideIndex) => {
      const button = document.createElement("button");
      button.type = "button";
      button.setAttribute("aria-label", `Show director ${slideIndex + 1}`);
      button.addEventListener("click", () => show(slideIndex));
      dots?.append(button);
      return button;
    });

    function show(nextIndex) {
      index = (nextIndex + slides.length) % slides.length;
      track.style.transform = `translateX(-${index * 100}%)`;
      slides.forEach((slide, slideIndex) => slide.setAttribute("aria-hidden", String(slideIndex !== index)));
      buttons.forEach((button, buttonIndex) => button.setAttribute("aria-current", String(buttonIndex === index)));
      if (current) current.textContent = String(index + 1).padStart(2, "0");
    }

    previous?.addEventListener("click", () => show(index - 1));
    next?.addEventListener("click", () => show(index + 1));
    carousel.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") show(index - 1);
      if (event.key === "ArrowRight") show(index + 1);
    });

    let startX = 0;
    carousel.addEventListener("touchstart", (event) => { startX = event.changedTouches[0].clientX; }, { passive: true });
    carousel.addEventListener("touchend", (event) => {
      const distance = event.changedTouches[0].clientX - startX;
      if (Math.abs(distance) > 45) show(index + (distance < 0 ? 1 : -1));
    }, { passive: true });
    show(0);
  });
}
