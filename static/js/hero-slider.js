export function initHeroSlider() {
  const slider = document.querySelector("[data-component='hero-slider']");
  if (!slider) return;
  const slides = slider.querySelectorAll(".hero-slide");
  if (slides.length < 2) return;

  let index = 0;
  setInterval(() => {
    slides[index].classList.remove("is-active");
    index = (index + 1) % slides.length;
    slides[index].classList.add("is-active");
  }, 6000);
}
