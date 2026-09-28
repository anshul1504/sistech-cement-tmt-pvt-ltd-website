export function initAccordions() {
  document.querySelectorAll("[data-component='accordion']").forEach((accordion) => {
    accordion.querySelectorAll(".accordion__trigger").forEach((trigger) => {
      trigger.addEventListener("click", () => {
        const isOpen = trigger.getAttribute("aria-expanded") === "true";
        accordion.querySelectorAll(".accordion__trigger").forEach((t) => t.setAttribute("aria-expanded", "false"));
        trigger.setAttribute("aria-expanded", String(!isOpen));
      });
    });
  });
}
