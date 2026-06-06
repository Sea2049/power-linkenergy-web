# Powerlink Energy Pure Static Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a pure static official website for Powerlink Energy in the project root using only HTML, CSS, and vanilla JavaScript, with no Node-based build or runtime dependency.

**Architecture:** Use one shared stylesheet and one shared JavaScript bundle under `assets/`. Store site copy, navigation, contact info, solutions, products, and cases as structured JavaScript data in `assets/js/data.js`; each overview page and detail page reads that data and renders cards, metrics, sections, and contact calls to action. Use CSS-only text logo and CSS illustration blocks instead of placeholder images, keeping all claims aligned with the approved spec and avoiding fake factory or certification assets.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript

---

## File Structure

### Create

- `index.html`
- `assets/css/site.css`
- `assets/js/data.js`
- `assets/js/site.js`
- `about/index.html`
- `contact/index.html`
- `solutions/index.html`
- `solutions/data-center-backup-power/index.html`
- `solutions/telecom-base-station-backup-power/index.html`
- `solutions/commercial-industrial-energy-storage/index.html`
- `solutions/residential-solar-storage/index.html`
- `solutions/edge-computing-power/index.html`
- `solutions/safety-monitoring-solutions/index.html`
- `products/index.html`
- `products/ups-systems/index.html`
- `products/lithium-battery-systems/index.html`
- `products/hybrid-solar-inverters/index.html`
- `products/telecom-dc-power/index.html`
- `products/monitoring-industrial-cabling/index.html`
- `cases/index.html`
- `cases/small-data-center-backup-power/index.html`
- `cases/telecom-base-station-backup-power/index.html`
- `cases/commercial-industrial-energy-storage/index.html`

### Responsibility Map

- `assets/css/site.css`: brand colors, layout system, cards, sections, responsive styles, CSS text logo, CSS-only visual blocks
- `assets/js/data.js`: approved contact info, navigation, homepage copy, solutions/products/cases content model
- `assets/js/site.js`: shared shell rendering, mobile nav, active navigation, overview/detail rendering helpers
- `index.html`: homepage skeleton and section containers
- `about/index.html`: company story and collaboration approach
- `contact/index.html`: direct contact, inquiry guidance, and static form shell
- `solutions/**/index.html`: overview page plus six detail routes
- `products/**/index.html`: overview page plus five detail routes
- `cases/**/index.html`: overview page plus three detail routes

---

### Task 1: Define shared static data and shell

**Files:**
- Create: `assets/js/data.js`
- Create: `assets/js/site.js`

- [ ] **Step 1: Write the shared data model**

Create `assets/js/data.js` with brand and content constants:

```js
window.POWERLINK_DATA = {
  site: {
    name: "Powerlink Energy",
    domain: "www.power-linkenergy.com",
    email: "Bob-Wang@power-linkenergy.com",
    whatsapp: "+86 13534190063",
    tagline: "Integrated Power Solutions for Critical Applications",
    nav: [
      { label: "Home", href: "/" },
      { label: "Solutions", href: "/solutions/" },
      { label: "Products", href: "/products/" },
      { label: "Cases", href: "/cases/" },
      { label: "About Us", href: "/about/" },
      { label: "Contact", href: "/contact/" }
    ]
  },
  home: {
    heroTitle: "Integrated Power Solutions for Critical Applications",
    heroBody: "Powerlink Energy provides UPS systems, energy storage solutions, telecom power equipment, DC/DC modules, industrial cabling, and monitoring accessories for data centers, telecom sites, commercial energy storage, and other demanding environments."
  },
  solutions: [],
  products: [],
  cases: []
};
```

- [ ] **Step 2: Fill `solutions`, `products`, and `cases` arrays with approved copy**

Each item must include `slug`, `title`, `summary`, `intro`, and page sections. Example solution item:

```js
{
  slug: "data-center-backup-power",
  title: "Data Center Backup Power",
  summary: "Reliable backup power solutions for small and medium-sized server rooms, IDC facilities, and network cabinets.",
  intro: "Powerlink Energy supports data center backup projects with scenario-based combinations of UPS systems, lithium battery systems, monitoring accessories, and related integration parts.",
  challenges: [
    "Minimize downtime for critical IT loads",
    "Fit equipment into limited rack or room space",
    "Improve visibility for battery and power status"
  ],
  configuration: [
    "Online UPS systems",
    "Lithium battery banks",
    "Battery monitoring accessories",
    "Industrial cabling and connectors"
  ],
  benefits: [
    "Stable backup support for critical applications",
    "Flexible rack or floor configuration",
    "Better monitoring and maintenance visibility"
  ]
}
```

- [ ] **Step 3: Write the shared shell and rendering helpers**

Create `assets/js/site.js`:

```js
(function () {
  var data = window.POWERLINK_DATA;

  function renderLogo() {
    return '<a class="brandmark" href="/"><span class="brandmark-power">Powerlink</span><span class="brandmark-energy">energy</span></a>';
  }

  function renderHeader() {
    return (
      '<header class="site-header">' +
      '<div class="container site-header__inner">' +
      renderLogo() +
      '<button class="nav-toggle" type="button" aria-expanded="false" aria-label="Toggle navigation">Menu</button>' +
      '<nav class="site-nav"><ul>' +
      data.site.nav.map(function (item) {
        return '<li><a href="' + item.href + '">' + item.label + '</a></li>';
      }).join("") +
      "</ul></nav></div></header>"
    );
  }

  function renderFooter() {
    return (
      '<footer class="site-footer"><div class="container footer-grid">' +
      '<div><p class="eyebrow">Powerlink Energy</p><h2>' + data.site.tagline + '</h2><p>Scenario-first supply support for power-sensitive and mission-critical applications.</p></div>' +
      '<div><p class="eyebrow">Direct Contact</p><p><a href="mailto:' + data.site.email + '">' + data.site.email + '</a></p><p><a href="https://wa.me/8613534190063">' + data.site.whatsapp + '</a></p><p>' + data.site.domain + "</p></div>" +
      "</div></footer>"
    );
  }

  function mountShell() {
    var header = document.querySelector("[data-site-header]");
    var footer = document.querySelector("[data-site-footer]");
    if (header) header.innerHTML = renderHeader();
    if (footer) footer.innerHTML = renderFooter();
  }

  document.addEventListener("DOMContentLoaded", mountShell);
})();
```

- [ ] **Step 4: Add detail helpers and active navigation**

Extend `assets/js/site.js` with functions for:

```js
function getCollection(name) {
  return data[name] || [];
}

function getEntry(name, slug) {
  return getCollection(name).find(function (item) {
    return item.slug === slug;
  });
}

function setActiveNav() {
  var links = document.querySelectorAll(".site-nav a");
  var current = window.location.pathname;
  Array.prototype.forEach.call(links, function (link) {
    var href = link.getAttribute("href");
    if (href !== "/" && current.indexOf(href) === 0) link.classList.add("is-active");
    if (href === "/" && current === "/") link.classList.add("is-active");
  });
}
```

- [ ] **Step 5: Commit**

```bash
git add assets/js/data.js assets/js/site.js
git commit -m "feat: add shared static site data and shell renderer"
```

### Task 2: Build the shared visual system

**Files:**
- Create: `assets/css/site.css`

- [ ] **Step 1: Add global tokens and reset**

Create `assets/css/site.css`:

```css
:root {
  --pl-navy: #071c49;
  --pl-blue: #1bb7ff;
  --pl-ink: #12233f;
  --pl-muted: #5f6f88;
  --pl-line: #d8e2ef;
  --pl-bg: #f3f7fb;
  --pl-white: #ffffff;
  --pl-radius: 20px;
  --pl-shadow: 0 24px 60px rgba(9, 28, 73, 0.08);
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font: 16px/1.6 Arial, Helvetica, sans-serif;
  color: var(--pl-ink);
  background: var(--pl-white);
}
```

- [ ] **Step 2: Add layout, typography, card, and button styles**

Extend with:

```css
.container {
  width: min(1180px, calc(100% - 32px));
  margin: 0 auto;
}

.section {
  padding: 72px 0;
}

.section--alt {
  background: var(--pl-bg);
}

.grid-3 {
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}

.card {
  border: 1px solid var(--pl-line);
  border-radius: var(--pl-radius);
  background: var(--pl-white);
  padding: 28px;
  box-shadow: var(--pl-shadow);
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
  padding: 0 20px;
  border-radius: 999px;
  text-decoration: none;
  font-weight: 700;
}
```

- [ ] **Step 3: Add header, footer, and CSS text logo**

Add:

```css
.site-header,
.site-footer {
  background: var(--pl-navy);
  color: var(--pl-white);
}

.brandmark {
  display: inline-flex;
  align-items: baseline;
  gap: 4px;
  text-decoration: none;
  font-weight: 700;
  font-size: 28px;
  letter-spacing: 0.02em;
}

.brandmark-power {
  color: var(--pl-white);
}

.brandmark-energy {
  color: var(--pl-blue);
}
```

- [ ] **Step 4: Add CSS-only visual panels instead of placeholder images**

Create visual blocks:

```css
.visual-panel {
  position: relative;
  min-height: 320px;
  border-radius: 28px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0)),
    linear-gradient(135deg, #0b255f, #123984);
  overflow: hidden;
}

.visual-panel::before,
.visual-panel::after {
  content: "";
  position: absolute;
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.16);
}

.visual-panel::before {
  inset: 28px 28px auto auto;
  width: 180px;
  height: 120px;
}

.visual-panel::after {
  inset: auto auto 28px 28px;
  width: 220px;
  height: 140px;
}
```

- [ ] **Step 5: Add responsive rules**

Append:

```css
@media (max-width: 960px) {
  .grid-3,
  .grid-2 {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  .site-nav {
    display: none;
  }

  .site-nav.is-open {
    display: block;
  }
}
```

- [ ] **Step 6: Commit**

```bash
git add assets/css/site.css
git commit -m "feat: add pure static website visual system"
```

### Task 3: Implement homepage and company pages

**Files:**
- Create: `index.html`
- Create: `about/index.html`
- Create: `contact/index.html`

- [ ] **Step 1: Create homepage skeleton**

Create `index.html` with section containers and shared asset references:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Powerlink Energy | Integrated Power Solutions</title>
  <meta name="description" content="Scenario-driven power solutions for data centers, telecom sites, energy storage, and other critical applications.">
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body data-page="home">
  <div data-site-header></div>
  <main>
    <section class="hero">
      <div class="container hero-grid">
        <div class="hero-copy"></div>
        <div class="visual-panel" aria-hidden="true"></div>
      </div>
    </section>
    <section class="section"><div class="container" id="home-applications"></div></section>
    <section class="section section--alt"><div class="container" id="home-solutions"></div></section>
    <section class="section"><div class="container" id="home-products"></div></section>
    <section class="section section--alt"><div class="container" id="home-cases"></div></section>
    <section class="section"><div class="container" id="home-contact"></div></section>
  </main>
  <div data-site-footer></div>
  <script src="/assets/js/data.js"></script>
  <script src="/assets/js/site.js"></script>
</body>
</html>
```

- [ ] **Step 2: Create About page**

Create `about/index.html` with approved sections: company intro, what we do, how we work, why customers choose us, support mindset, bottom CTA.

- [ ] **Step 3: Create Contact page**

Create `contact/index.html` with approved direct contact info, inquiry guidance, and a static form shell that submits nowhere:

```html
<form class="inquiry-form" action="#" method="get">
  <label><span>Name</span><input type="text" name="name"></label>
  <label><span>Company</span><input type="text" name="company"></label>
  <label><span>Country</span><input type="text" name="country"></label>
  <label><span>Email</span><input type="email" name="email"></label>
  <label><span>WhatsApp</span><input type="text" name="whatsapp"></label>
  <label><span>Application</span><input type="text" name="application"></label>
  <label><span>Product Interest</span><input type="text" name="product-interest"></label>
  <label><span>Message</span><textarea name="message" rows="6"></textarea></label>
  <button class="button button--primary" type="submit">Send Your Inquiry</button>
</form>
```

- [ ] **Step 4: Add homepage rendering logic**

Extend `assets/js/site.js` to render homepage content into `#home-applications`, `#home-solutions`, `#home-products`, `#home-cases`, and `#home-contact` using `window.POWERLINK_DATA`.

- [ ] **Step 5: Commit**

```bash
git add index.html about/index.html contact/index.html assets/js/site.js
git commit -m "feat: add homepage about and contact pages"
```

### Task 4: Implement solutions overview and six detail pages

**Files:**
- Create: `solutions/index.html`
- Create: `solutions/data-center-backup-power/index.html`
- Create: `solutions/telecom-base-station-backup-power/index.html`
- Create: `solutions/commercial-industrial-energy-storage/index.html`
- Create: `solutions/residential-solar-storage/index.html`
- Create: `solutions/edge-computing-power/index.html`
- Create: `solutions/safety-monitoring-solutions/index.html`

- [ ] **Step 1: Create Solutions overview page**

Create `solutions/index.html` with containers for hero intro and solution cards:

```html
<body data-page="solutions-overview">
  <div data-site-header></div>
  <main>
    <section class="page-hero">
      <div class="container">
        <p class="eyebrow">Solutions</p>
        <h1>Scenario-Based Power Solutions</h1>
        <p>Instead of offering only standalone products, we help customers combine the right equipment into workable power solution packages.</p>
      </div>
    </section>
    <section class="section">
      <div class="container" id="solutions-list"></div>
    </section>
  </main>
  <div data-site-footer></div>
  <script src="/assets/js/data.js"></script>
  <script src="/assets/js/site.js"></script>
</body>
```

- [ ] **Step 2: Create reusable solution detail template**

Each detail page should be a static HTML file with matching `data-collection` and `data-slug`:

```html
<body data-page="detail" data-collection="solutions" data-slug="data-center-backup-power">
  <div data-site-header></div>
  <main>
    <section class="page-hero"><div class="container" id="detail-hero"></div></section>
    <section class="section"><div class="container detail-layout" id="detail-body"></div></section>
  </main>
  <div data-site-footer></div>
  <script src="/assets/js/data.js"></script>
  <script src="/assets/js/site.js"></script>
</body>
```

- [ ] **Step 3: Duplicate the detail template for all six solution routes**

Use these exact slugs:

- `data-center-backup-power`
- `telecom-base-station-backup-power`
- `commercial-industrial-energy-storage`
- `residential-solar-storage`
- `edge-computing-power`
- `safety-monitoring-solutions`

- [ ] **Step 4: Render solution overview and detail content**

Extend `assets/js/site.js` with `renderSolutionsOverview()` and `renderDetailPage()` so the correct solution data renders automatically from `window.POWERLINK_DATA`.

- [ ] **Step 5: Commit**

```bash
git add solutions assets/js/site.js
git commit -m "feat: add pure static solutions overview and detail pages"
```

### Task 5: Implement products overview and five detail pages

**Files:**
- Create: `products/index.html`
- Create: `products/ups-systems/index.html`
- Create: `products/lithium-battery-systems/index.html`
- Create: `products/hybrid-solar-inverters/index.html`
- Create: `products/telecom-dc-power/index.html`
- Create: `products/monitoring-industrial-cabling/index.html`

- [ ] **Step 1: Create Products overview page**

Create `products/index.html` with intro, product category card container, and support CTA.

- [ ] **Step 2: Create product detail template pages**

Use the same detail shell pattern with:

```html
<body data-page="detail" data-collection="products" data-slug="ups-systems">
```

- [ ] **Step 3: Use these exact product slugs**

- `ups-systems`
- `lithium-battery-systems`
- `hybrid-solar-inverters`
- `telecom-dc-power`
- `monitoring-industrial-cabling`

- [ ] **Step 4: Render product overview and detail content**

Add `renderProductsOverview()` and extend `renderDetailPage()` to support products with applications, integration scope, and contact CTA.

- [ ] **Step 5: Commit**

```bash
git add products assets/js/site.js
git commit -m "feat: add pure static products overview and detail pages"
```

### Task 6: Implement cases overview and three detail pages

**Files:**
- Create: `cases/index.html`
- Create: `cases/small-data-center-backup-power/index.html`
- Create: `cases/telecom-base-station-backup-power/index.html`
- Create: `cases/commercial-industrial-energy-storage/index.html`

- [ ] **Step 1: Create Cases overview page**

Create `cases/index.html` with intro copy explaining these are practical reference structures for future expansion, plus three case cards.

- [ ] **Step 2: Create case detail template pages**

Use the same detail shell pattern with:

```html
<body data-page="detail" data-collection="cases" data-slug="small-data-center-backup-power">
```

- [ ] **Step 3: Use these exact case slugs**

- `small-data-center-backup-power`
- `telecom-base-station-backup-power`
- `commercial-industrial-energy-storage`

- [ ] **Step 4: Render case overview and detail content**

Each case detail must render:

- project overview
- customer challenge
- solution design
- main configuration
- delivery and support
- results
- bottom CTA

- [ ] **Step 5: Commit**

```bash
git add cases assets/js/site.js
git commit -m "feat: add pure static cases overview and detail pages"
```

### Task 7: Final validation and manual smoke test

**Files:**
- Verify: `index.html`
- Verify: `assets/css/site.css`
- Verify: `assets/js/data.js`
- Verify: `assets/js/site.js`
- Verify: `about/index.html`
- Verify: `contact/index.html`
- Verify: `solutions/**/index.html`
- Verify: `products/**/index.html`
- Verify: `cases/**/index.html`

- [ ] **Step 1: Check file coverage**

Confirm the site contains:

- 1 homepage
- 1 About page
- 1 Contact page
- 1 Solutions overview page
- 6 solution detail pages
- 1 Products overview page
- 5 product detail pages
- 1 Cases overview page
- 3 case detail pages

- [ ] **Step 2: Run a simple local server**

Run one of:

```bash
python -m http.server 8000
```

or on PowerShell:

```powershell
py -m http.server 8000
```

Expected: local preview becomes available on `http://localhost:8000/`

- [ ] **Step 3: Manually verify key routes**

Check:

- `/`
- `/about/`
- `/contact/`
- `/solutions/`
- `/solutions/data-center-backup-power/`
- `/products/`
- `/products/ups-systems/`
- `/cases/`
- `/cases/small-data-center-backup-power/`

Expected:

- header and footer render
- active nav state is correct
- text logo appears in white and bright blue
- CSS visual panels render without broken images
- contact details match approved values

- [ ] **Step 4: Content safety review**

Confirm there are no:

- fake factory photos
- fake project claims
- fake certifications
- company address

- [ ] **Step 5: Commit**

```bash
git add index.html assets about contact solutions products cases docs/superpowers/plans/2026-06-04-powerlink-energy-website.md
git commit -m "feat: launch pure static powerlink energy website"
```

---

## Self-Review

### Spec coverage

- Home, About, Contact, Solutions, Products, and Cases are all covered
- Six solutions, five products, and three case detail routes are included
- Cloudflare + OSS compatible static deployment is preserved
- CSS text logo and no-placeholder-image approach are explicit

### Placeholder scan

- No `TODO` or `TBD`
- All tasks point to exact root-level files
- Commands use only static hosting and browser-safe assets

### Type consistency

- `slug` is the lookup key across all overview and detail pages
- All routes use the same `data-page` and `data-collection` conventions
- Contact values come from one shared data source
