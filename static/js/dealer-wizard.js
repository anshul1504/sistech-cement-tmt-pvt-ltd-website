function validateStep(fieldset) {
  const controls = [...fieldset.querySelectorAll("input, select, textarea")];
  for (const control of controls) {
    if (!control.checkValidity()) {
      control.reportValidity();
      control.focus();
      return false;
    }
  }
  return true;
}

export function initDealerWizard() {
  const form = document.querySelector("[data-dealer-wizard]");
  if (!form) return;

  const steps = [...form.querySelectorAll("fieldset")];
  if (steps.length < 2) return;

  let current = Math.max(0, steps.findIndex((step) => step.querySelector(".error-text")));
  const progress = document.createElement("div");
  progress.className = "dealer-wizard-progress";
  progress.setAttribute("aria-label", "Application progress");

  const progressButtons = steps.map((step, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = step.querySelector("legend")?.textContent.trim().replace(/^\d\s*/, "") || `Step ${index + 1}`;
    button.addEventListener("click", () => {
      if (index <= current) showStep(index);
    });
    progress.appendChild(button);
    return button;
  });

  form.insertBefore(progress, steps[0]);
  form.classList.add("is-stepped");

  steps.forEach((step, index) => {
    const actions = document.createElement("div");
    actions.className = "dealer-wizard-actions";

    if (index > 0) {
      const back = document.createElement("button");
      back.type = "button";
      back.className = "btn btn--outline";
      back.textContent = "Back";
      back.addEventListener("click", () => showStep(index - 1));
      actions.appendChild(back);
    } else {
      actions.appendChild(document.createElement("span"));
    }

    if (index < steps.length - 1) {
      const next = document.createElement("button");
      next.type = "button";
      next.className = "btn btn--primary";
      next.textContent = "Continue";
      next.addEventListener("click", () => {
        if (validateStep(step)) showStep(index + 1);
      });
      actions.appendChild(next);
    }
    step.appendChild(actions);
  });

  function showStep(index) {
    current = index;
    steps.forEach((step, stepIndex) => step.classList.toggle("is-active", stepIndex === current));
    progressButtons.forEach((button, buttonIndex) => {
      button.classList.toggle("is-active", buttonIndex === current);
      button.classList.toggle("is-complete", buttonIndex < current);
      button.setAttribute("aria-current", buttonIndex === current ? "step" : "false");
    });
    form.classList.toggle("is-final-step", current === steps.length - 1);
    if (index > 0) progress.scrollIntoView({ behavior: "smooth", block: "center" });
  }

  showStep(current);
}
