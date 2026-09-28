const FOCUSABLE = 'a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])';

function initStickyHeader() {
  const header = document.querySelector(".site-header.is-sticky");
  if (!header) return;

  // Hysteresis: different thresholds to enter vs. leave the "scrolled" state,
  // so hovering right around one pixel value (common with trackpad/momentum
  // scroll) can't rapidly flip the class and cause visible flicker.
  const ENTER_AT = 60;
  const EXIT_AT = 20;
  let isScrolled = false;
  let ticking = false;

  const apply = () => {
    const y = window.scrollY;
    if (!isScrolled && y > ENTER_AT) {
      isScrolled = true;
      header.classList.add("is-scrolled");
    } else if (isScrolled && y < EXIT_AT) {
      isScrolled = false;
      header.classList.remove("is-scrolled");
    }
    ticking = false;
  };

  const onScroll = () => {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(apply);
  };

  apply();
  window.addEventListener("scroll", onScroll, { passive: true });
}

function initDesktopDropdowns() {
  const items = document.querySelectorAll(".primary-nav .has-dropdown");
  items.forEach((item) => {
    const trigger = item.querySelector(":scope > a");
    const panel = item.querySelector(":scope > .dropdown");
    if (!trigger || !panel) return;
    const links = () => Array.from(panel.querySelectorAll("a"));

    const open = () => {
      item.classList.add("is-open");
      trigger.setAttribute("aria-expanded", "true");
    };
    const close = ({ focusTrigger = false } = {}) => {
      item.classList.remove("is-open");
      trigger.setAttribute("aria-expanded", "false");
      if (focusTrigger) trigger.focus();
    };

    trigger.addEventListener("click", (e) => {
      e.preventDefault();
      item.classList.contains("is-open") ? close() : open();
    });

    trigger.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown" || e.key === " " || e.key === "Enter") {
        e.preventDefault();
        open();
        links()[0]?.focus();
      } else if (e.key === "Escape") {
        close({ focusTrigger: true });
      }
    });

    panel.addEventListener("keydown", (e) => {
      const list = links();
      const idx = list.indexOf(document.activeElement);
      if (e.key === "ArrowDown") {
        e.preventDefault();
        list[(idx + 1) % list.length]?.focus();
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        if (idx <= 0) {
          close({ focusTrigger: true });
        } else {
          list[idx - 1]?.focus();
        }
      } else if (e.key === "Escape") {
        close({ focusTrigger: true });
      }
    });

    item.addEventListener("focusout", (e) => {
      if (!item.contains(e.relatedTarget)) close();
    });
  });

  document.addEventListener("click", (e) => {
    items.forEach((item) => {
      if (!item.contains(e.target)) {
        item.classList.remove("is-open");
        item.querySelector(":scope > a")?.setAttribute("aria-expanded", "false");
      }
    });
  });
}

function initMobileAccordion() {
  document.querySelectorAll(".mobile-accordion__trigger").forEach((trigger) => {
    trigger.addEventListener("click", () => {
      const panel = trigger.nextElementSibling;
      const isOpen = trigger.getAttribute("aria-expanded") === "true";

      document.querySelectorAll(".mobile-accordion__trigger").forEach((t) => {
        t.setAttribute("aria-expanded", "false");
        t.nextElementSibling?.classList.remove("is-open");
      });

      if (!isOpen) {
        trigger.setAttribute("aria-expanded", "true");
        panel?.classList.add("is-open");
      }
    });
  });
}

function initMobileDrawer() {
  const toggle = document.querySelector(".mobile-menu-toggle");
  const drawer = document.getElementById("mobile-drawer");
  const overlay = document.querySelector("[data-drawer-overlay]");
  const closeBtn = document.querySelector(".mobile-drawer__close");
  if (!toggle || !drawer || !overlay) return;

  let lastFocused = null;

  const open = () => {
    lastFocused = document.activeElement;
    drawer.classList.add("is-open");
    drawer.setAttribute("aria-hidden", "false");
    overlay.hidden = false;
    requestAnimationFrame(() => overlay.classList.add("is-visible"));
    document.body.classList.add("drawer-open");
    toggle.setAttribute("aria-expanded", "true");
    drawer.querySelector(FOCUSABLE)?.focus();
  };

  const close = () => {
    drawer.classList.remove("is-open");
    drawer.setAttribute("aria-hidden", "true");
    overlay.classList.remove("is-visible");
    document.body.classList.remove("drawer-open");
    toggle.setAttribute("aria-expanded", "false");
    setTimeout(() => { if (!drawer.classList.contains("is-open")) overlay.hidden = true; }, 300);
    lastFocused?.focus();
  };

  toggle.addEventListener("click", open);
  closeBtn?.addEventListener("click", close);
  overlay.addEventListener("click", close);

  drawer.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      close();
      return;
    }
    if (e.key !== "Tab") return;
    const focusables = Array.from(drawer.querySelectorAll(FOCUSABLE)).filter((el) => el.offsetParent !== null);
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  });
}

export function initHeader() {
  initStickyHeader();
  initDesktopDropdowns();
  initMobileAccordion();
  initMobileDrawer();
}
