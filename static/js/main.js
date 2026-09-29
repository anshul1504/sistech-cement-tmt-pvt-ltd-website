import { initHeader } from "./header.js";
import { initTabs } from "./tabs.js";
import { initAccordions } from "./accordion.js";
import { initLightbox } from "./lightbox.js";
import { initCounters } from "./counters.js";
import { initScrollReveal } from "./scroll-reveal.js";
import { initFormUX } from "./form-ux.js";
import { initGalleryFilter } from "./gallery-filter.js";
import { initHeroSlider } from "./hero-slider.js";
import { initBackToTop } from "./back-to-top.js";
import { initMaps } from "./map.js";
import { initDealerWizard } from "./dealer-wizard.js";
import { initLeadershipCarousel } from "./leadership-carousel-v2.js";

document.addEventListener("DOMContentLoaded", () => {
  initHeader();
  initTabs();
  initAccordions();
  initLightbox();
  initCounters();
  initScrollReveal();
  initFormUX();
  initGalleryFilter();
  initHeroSlider();
  initBackToTop();
  initMaps();
  initDealerWizard();
  initLeadershipCarousel();
});
