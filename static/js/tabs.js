export function initTabs() {
  document.querySelectorAll("[data-component='tabs']").forEach((group) => {
    const buttons = group.querySelectorAll("[data-tab-target]");
    buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const target = group.querySelector(btn.dataset.tabTarget);
        buttons.forEach((b) => b.setAttribute("aria-selected", "false"));
        group.querySelectorAll("[data-tab-panel]").forEach((p) => p.hidden = true);
        btn.setAttribute("aria-selected", "true");
        if (target) target.hidden = false;
      });
    });
  });
}
