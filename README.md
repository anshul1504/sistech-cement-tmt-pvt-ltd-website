# SISTECH Cement & TMT Pvt. Ltd. — Corporate Website

Django 5.2 site with a fully admin-customizable theme, menus and page/section builder.
No CSS/JS framework, no Node build step — plain CSS layers + vanilla ES6 modules.

## Setup

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env         # edit values as needed
python manage.py migrate
python manage.py seed_demo     # creates all 20 pages + default menu + sample hero slide
python manage.py createsuperuser
python manage.py build_css     # optional in dev; required before setting USE_BUILT_CSS=True
python manage.py runserver
```

Admin: http://127.0.0.1:8000/admin/ (path configurable via `ADMIN_URL_PATH` in `.env`).

## Management commands

- `seed_demo` — creates all 20 `Page` rows with real SISTECH content, the header/footer menu, one sample hero slide, and uploads the extracted logo/favicon assets. Safe to re-run; only fills what's missing.
- `reset_theme` — resets `ThemeSettings` to the shipped defaults.
- `reset_menu --yes` — rebuilds the header/footer menu to the current 7-top-level + CTA structure on an existing database (deletes all `MenuItem` rows first; the `--yes` flag is required).
- `build_css` — concatenates and minifies the layers listed in `static/css/manifest.txt` into `static/dist/main.css` (pure Python, no Node). `base.html` reads the same manifest for dev mode, so there's one ordered list to maintain. Set `USE_BUILT_CSS=True` in `.env` to serve the built file instead of the source layers; production settings default this to `True`.

## Logo assets

`apps/core/seed_assets/` holds the logo extracted from the client's corporate profile PDF (cover page, rendered at 8x and background-removed with a soft-alpha threshold + edge feather — not a hard color-key, to avoid white halos). Variants: `logo_header.png` (full lockup with tagline), `logo_header_compact.png` (no tagline, used when the header is scrolled/collapsed and on mobile), `logo_footer.png` (white/light version for the navy footer), `favicon.png` (512×512, navy rounded square with the gold roof mark), `apple_touch_icon.png` (180×180).

**Replace these with the vector/original logo files from the client when available** — a PDF-rasterized extraction is a fallback, not a substitute for the source AI/EPS/SVG.

## Settings

Split as `config/settings/{base,dev,prod}.py`, selected via `DJANGO_SETTINGS_MODULE`
(`config.settings.dev` by default in `manage.py`/`wsgi.py`/`asgi.py`).
All secrets and environment-specific values come from `.env` (see `.env.example`).

## Where things live

- `apps/core` — ThemeSettings, SiteSettings, MenuItem, HeroSlide, Page/PageSection builder, home view, maintenance middleware
- `apps/faq` — FAQCategory/FAQItem (needed early since PageSection's FAQ accordion links to it)
- `apps/products`, `network`, `programs`, `company`, `media_center`, `careers`, `enquiries` — stubbed, full models land in Phase 3
- `templates/components/*` — header (two-row: top utility bar + main nav, with a right-side mobile drawer), footer (4/2/1-column responsive), hero, breadcrumb, CTA band, icon sprite (`icons.svg`), WhatsApp/back-to-top buttons
- `templates/sections/*` — one partial per `PageSection` type, dispatched via the `render_section` template tag
- `static/css/{base,layout,components,utilities}` — source CSS layers, ordered by `static/css/manifest.txt`; `static/dist/main.css` is the built output
- `static/js/header.js` — sticky header, desktop dropdowns (keyboard nav, hover-bridge, outside-click), mobile accordion, and the slide-in drawer (focus trap, Esc, scroll lock); `static/js/main.js` wires it up alongside the other small per-feature modules

## Header & navigation

- Header menu is capped at 7 top-level items + 1 CTA button (`Become a Dealer`), seeded by `seed_demo`/rebuilt by `reset_menu`. `MenuItem.description` shows under a link inside a dropdown panel; `MenuItem.footer_column` (1/2/3/none) places that same item in a footer column independently of the header.
- The `menu_is_active` template tag highlights the current top-level/parent nav item (a parent is active if any of its children match the current path); `/` is never marked active on other pages.
- The context processor prefetches menu children with `Prefetch(..., to_attr="active_children")` — two queries total for the whole menu tree, regardless of how many items exist (covered by `MenuContextProcessorTests.test_no_n_plus_one_queries`).

## Content editing (non-technical staff)

Everything visible on the site is editable in Django admin:
- **Theme Settings** — colors, fonts, spacing, toggles (sticky header, WhatsApp button, etc.)
- **Site Settings** — company info, contact details, socials, footer text, tracking scripts, maintenance mode
- **Menu Items** — header/footer navigation, drag-and-drop order, dropdowns via Parent
- **Pages → Sections** — build any page from reusable section blocks (rich text, image+text, feature cards, stats, timeline, steps, FAQ accordion, gallery, CTA band, testimonial, downloads, map, custom HTML)

An in-admin **Admin Guide** page (Phase 3) will document each of these in plain language.

## Visual verification without Playwright

Playwright couldn't be installed in this environment (see Known limitation below), but the system's installed
Chrome can take real headless screenshots directly, which is how the header/footer rebuild was actually
verified pixel-by-pixel:

```powershell
& "C:\Program Files\Google\Chrome\Application\chrome.exe" --headless=new --disable-gpu `
  --force-device-scale-factor=1 --screenshot="out.png" --window-size=1440,900 --hide-scrollbars `
  "http://127.0.0.1:8000/"
```

**Caveat found the hard way**: in this sandbox, `--window-size` below roughly 500px produces corrupted
text-wrapping in the screenshot itself (confirmed with a trivial static HTML file with no site CSS involved —
same artifact). Don't trust screenshots narrower than ~500px here; 768px and up render correctly and can be
trusted. For true small-mobile (320–480px) verification, use a real browser/device or re-run Playwright once
it installs cleanly.

## Status

Phase 2 complete: scaffold, settings, CSS variable system, base layout, ThemeSettings/SiteSettings,
dynamic menus, HeroSlide, the Page/PageSection builder with all 13 section types, `seed_demo`/`build_css`/`reset_theme`/`reset_menu`,
maintenance mode, a professionally rebuilt responsive header/footer (real extracted logo, capped nav, accessible dropdowns/drawer),
and the Content Editor/Admin groups (permissions widen in Phase 3 as more apps gain models). All 20 pages are wired and return
200, currently through the generic Page/PageSection builder — dedicated apps/templates (products, careers, blog, etc.) land in Phase 3/4
without changing their URLs.

Remaining phases (per the project brief): full dedicated models for products/network/programs/company/media/careers/faq/enquiries,
their own templates, forms + email routing, SEO/sitemap/JSON-LD, more tests, and deployment hardening.

**Known limitation**: `requirements-dev.txt` lists Playwright for visual regression screenshots, but it couldn't be installed in
this environment — its `greenlet` dependency has no prebuilt wheel for Python 3.14 yet and there's no C compiler available to build
one from source. Header/footer/menu changes were verified via the Django test client (route/status/N+1-query assertions) and manual
HTML/CSS review instead of pixel screenshots. Re-run `pip install -r requirements-dev.txt` on Python 3.11–3.12 to get Playwright working.
