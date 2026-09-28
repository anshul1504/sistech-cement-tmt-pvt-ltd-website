export function initFormUX() {
  document.querySelectorAll("form[data-component='ajax-form']").forEach((form) => {
    const submitBtn = form.querySelector("[type='submit']");
    form.addEventListener("submit", () => {
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.dataset.originalText = submitBtn.textContent;
        submitBtn.textContent = "Sending…";
      }
    });
  });
}
