# Powerlink Energy Cases Launch Package Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the Cases experience with a stronger overview hero, honest real-project image slots, reusable case template fields, and OSS + Cloudflare launch documentation.

**Architecture:** Keep the current static-site architecture and extend the existing data-driven renderers in `assets/js/site.js` instead of adding new page-specific scripts. Store new Cases media metadata in `assets/js/data.js`, reuse the current detail card and CTA system, and document deployment in Markdown so the launch package stays easy to maintain.

**Tech Stack:** HTML, CSS, Vanilla JavaScript, Python smoke tests, static hosting on Alibaba Cloud OSS with Cloudflare CDN

---

## File Structure

- **Modify:** `assets/js/data.js`
  - Extend case objects with optional hero and gallery fields.
- **Modify:** `assets/js/site.js`
  - Add Cases-specific hero rendering, card media fallbacks, gallery rendering, and empty-state logic.
- **Modify:** `assets/css/site.css`
  - Add styles for the new Cases hero support block, card image slots, gallery layout, and empty states.
- **Modify:** `cases/index.html`
  - Replace the simple overview hero with hook containers for richer Cases hero content.
- **Modify:** `tests/check_cases_visual_system.py`
  - Expand coverage for hero media, gallery, and empty-state hooks.
- **Modify:** `README.md`
  - Add concise launch-package and maintenance instructions.
- **Create:** `docs/deployment/cloudflare-oss-launch.md`
  - Write the final release guide for OSS + Cloudflare deployment and cache refresh flow.

### Task 1: Lock the new Cases hooks with a failing test

**Files:**
- Modify: `tests/check_cases_visual_system.py`
- Test: `tests/check_cases_visual_system.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    site_js = read("assets/js/site.js")
    css = read("assets/css/site.css")
    cases_html = read("cases/index.html")

    assert "renderCaseFrameworkCard" in site_js, "missing case framework card renderer"
    assert "renderCaseHero" in site_js, "missing cases overview hero renderer"
    assert "renderCaseGallery" in site_js, "missing case gallery renderer"
    assert "renderCaseMedia" in site_js, "missing case media renderer"
    assert ".cases-hero" in css, "missing cases hero styles"
    assert ".case-gallery" in css, "missing case gallery styles"
    assert ".case-empty-state" in css, "missing case empty state styles"
    assert 'id="cases-hero"' in cases_html, "missing cases hero hook"

    print("cases launch package hooks OK")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run test to verify it fails**

Run:

```bash
py -3 tests/check_cases_visual_system.py
```

Expected:

```text
AssertionError: missing cases overview hero renderer
```

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/check_cases_visual_system.py
git commit -m "test: add cases launch package checks"
```

### Task 2: Extend Cases data to support honest media placeholders

**Files:**
- Modify: `assets/js/data.js`
- Test: `tests/check_cases_visual_system.py`

- [ ] **Step 1: Add optional media fields to each case entry**

Use this shape for the three existing case objects:

```javascript
{
  slug: "small-data-center-backup-power",
  title: "Small Data Center Backup Power",
  summary: "Backup power configuration reference for compact server rooms and IDC environments.",
  region: "Reference Framework",
  application: "Compact server rooms and IDC environments",
  projectStatus: "Reference Framework",
  imageMode: "placeholder",
  heroImage: "",
  heroImageAlt: "",
  gallery: [],
  galleryNote: "Project photos will be added as verified project assets become available."
}
```

- [ ] **Step 2: Keep the new fields optional and non-breaking**

Make sure existing cases still render if only these keys are added:

```javascript
projectStatus: item.projectStatus || "Reference Framework",
imageMode: item.imageMode || "placeholder",
gallery: item.gallery || [],
galleryNote: item.galleryNote || ""
```

- [ ] **Step 3: Re-run the test to confirm it still fails only on rendering hooks**

Run:

```bash
py -3 tests/check_cases_visual_system.py
```

Expected:

```text
AssertionError: missing cases overview hero renderer
```

- [ ] **Step 4: Commit the data-model update**

```bash
git add assets/js/data.js
git commit -m "feat: extend cases data model for media slots"
```

### Task 3: Implement Cases hero, image slots, and gallery UI

**Files:**
- Modify: `cases/index.html`
- Modify: `assets/js/site.js`
- Modify: `assets/css/site.css`
- Test: `tests/check_cases_visual_system.py`

- [ ] **Step 1: Add the Cases overview hero hook in HTML**

Replace the current hero body with a render target:

```html
<section class="page-hero page-hero--cases">
  <div class="container" id="cases-hero"></div>
</section>
```

- [ ] **Step 2: Add minimal rendering helpers in `assets/js/site.js`**

Add these functions near the other renderer helpers:

```javascript
function renderCaseMedia(item, variant) {
  if (item && item.image) {
    return '<div class="' + variant + '"><img src="' + item.image + '" alt="' + (item.imageAlt || item.title) + '"></div>';
  }

  if (item && item.heroImage) {
    return '<div class="' + variant + '"><img src="' + item.heroImage + '" alt="' + (item.heroImageAlt || item.title) + '"></div>';
  }

  return (
    '<div class="' + variant + ' case-empty-state">' +
    '<p class="eyebrow">Verified Project Assets</p>' +
    '<h3>Project images will be added later</h3>' +
    '<p>' + ((item && item.galleryNote) || 'Project photos will be added as verified project assets become available.') + '</p>' +
    '</div>'
  );
}

function renderCaseHero() {
  return (
    '<div class="cases-hero">' +
    '<div class="cases-hero__copy">' +
    '<p class="eyebrow">Cases</p>' +
    '<h1>Reference Frameworks That Can Grow Into a Real Case Library</h1>' +
    '<p>Use structured case content to explain applications clearly now and add verified project photos later without changing the page system.</p>' +
    '<div class="pill-list"><li>Scenario-led</li><li>Expandable</li><li>Project-ready</li></div>' +
    '</div>' +
    '<aside class="cases-hero__panel info-card">' +
    '<p class="eyebrow">How We Structure Cases</p>' +
    '<h3>Application first, assets second</h3>' +
    '<p>Each case explains the challenge, design logic, main configuration, and future project media in one reusable template.</p>' +
    '</aside>' +
    '</div>'
  );
}

function renderCaseGallery(entry) {
  var gallery = entry.gallery || [];
  if (!gallery.length) {
    return (
      '<section class="card case-gallery case-gallery--empty">' +
      '<div class="case-empty-state">' +
      '<p class="eyebrow">Project Photos</p>' +
      '<h2>Verified project visuals will be added here</h2>' +
      '<p>' + (entry.galleryNote || 'Project photos will be added as verified project assets become available.') + '</p>' +
      '</div>' +
      '</section>'
    );
  }

  return (
    '<section class="card case-gallery">' +
    '<div class="detail-info-card__head"><p class="eyebrow">Project Photos</p><h2>Verified Project Visuals</h2></div>' +
    '<div class="case-gallery__grid">' + gallery.map(function (image) {
      return '<figure class="case-gallery__item"><img src="' + image.src + '" alt="' + image.alt + '"></figure>';
    }).join('') + '</div>' +
    (entry.galleryNote ? '<p class="case-gallery__note">' + entry.galleryNote + '</p>' : '') +
    '</section>'
  );
}
```

- [ ] **Step 3: Wire the new helpers into overview and detail rendering**

Use these targeted replacements:

```javascript
function renderCaseFrameworkCard(item) {
  return (
    '<article class="card case-framework-card">' +
    renderCaseMedia(item, 'card-media card-media--case') +
    '<div class="case-framework-card__body">' +
    '<div class="case-framework-card__head">' +
    '<p class="eyebrow">' + (item.projectStatus || item.region) + '</p>' +
    '<span class="case-framework-card__tag">' + item.application + '</span>' +
    '</div>' +
    '<h3>' + item.title + '</h3>' +
    '<p>' + item.summary + '</p>' +
    '<a class="route-link" href="/cases/' + item.slug + '/">View details</a>' +
    '</div>' +
    '</article>'
  );
}
```

```javascript
var casesHero = byId('cases-hero');
if (casesHero) {
  casesHero.innerHTML = renderCaseHero();
}
```

```javascript
hero.innerHTML =
  '<div class="split-hero">' +
  '<div class="detail-hero">' +
  '<p class="eyebrow">' + (entry.projectStatus || 'Case Framework') + '</p>' +
  '<h1>' + entry.title + '</h1>' +
  '<p>' + subtitle + '</p>' +
  '<ul class="pill-list"><li>' + entry.region + '</li><li>' + entry.application + '</li></ul>' +
  '</div>' +
  renderCaseMedia(entry, 'visual-panel visual-panel--image visual-panel--case') +
  '</div>';
```

```javascript
body.innerHTML =
  '<div class="detail-card-stack">' +
  detailSections(entry, collectionName) +
  (collectionName === 'cases' ? renderCaseGallery(entry) : '') +
  '</div>' +
  renderDetailCta(collectionName);
```

- [ ] **Step 4: Add the matching CSS in `assets/css/site.css`**

Add these blocks alongside the current Cases/detail styles:

```css
.page-hero--cases {
  overflow: hidden;
}

.cases-hero {
  display: grid;
  gap: 28px;
  grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
  align-items: stretch;
}

.cases-hero__panel {
  background: linear-gradient(180deg, rgba(255,255,255,0.14), rgba(255,255,255,0.06));
  border: 1px solid rgba(255,255,255,0.14);
}

.card-media--case,
.visual-panel--case,
.case-empty-state {
  min-height: 220px;
  border-radius: 20px;
}

.case-empty-state {
  display: grid;
  align-content: end;
  padding: 24px;
  background:
    linear-gradient(180deg, rgba(7, 28, 73, 0.24), rgba(7, 28, 73, 0.74)),
    radial-gradient(circle at top right, rgba(24, 187, 255, 0.32), transparent 42%);
  color: var(--pl-white);
}

.case-gallery {
  border-radius: 24px;
  padding: 28px;
}

.case-gallery__grid {
  display: grid;
  gap: 16px;
  grid-template-columns: repeat(3, minmax(0, 1fr));
}
```

- [ ] **Step 5: Run the focused test and expect success**

Run:

```bash
py -3 tests/check_cases_visual_system.py
```

Expected:

```text
cases launch package hooks OK
```

- [ ] **Step 6: Run the existing detail-system regression test**

Run:

```bash
py -3 tests/check_detail_card_system.py
```

Expected:

```text
detail card system hooks OK
```

- [ ] **Step 7: Commit the UI implementation**

```bash
git add cases/index.html assets/js/site.js assets/css/site.css tests/check_cases_visual_system.py
git commit -m "feat: upgrade cases hero and media template"
```

### Task 4: Write the launch package docs and verify locally

**Files:**
- Modify: `README.md`
- Create: `docs/deployment/cloudflare-oss-launch.md`
- Test: local browser preview

- [ ] **Step 1: Update `README.md` with local preview and delivery notes**

Append a short maintenance section like this:

```md
## Cases Maintenance

- Add new case data in `assets/js/data.js`
- Create a matching detail route under `cases/<slug>/index.html`
- Fill `heroImage`, `gallery`, and `galleryNote` only when verified project assets are available

## Launch Package

- Upload all static files in the project root to OSS
- Set `index.html` as the default document
- Use Cloudflare in front of OSS for DNS, HTTPS, and caching
- Purge Cloudflare cache after updates
```

- [ ] **Step 2: Create the dedicated deployment guide**

Create `docs/deployment/cloudflare-oss-launch.md` with these sections:

```md
# Cloudflare + OSS Launch Guide

## 1. Package Contents
- Root HTML routes
- `assets/`
- `downloads/` if referenced by page content

## 2. Upload to Alibaba Cloud OSS
1. Create or open the target bucket
2. Enable static website hosting
3. Set the default homepage to `index.html`
4. Set the error page to `/404.html` or fall back to `index.html` if needed
5. Upload the project files preserving paths

## 3. Connect Cloudflare
1. Add the domain to Cloudflare
2. Point `www` through Cloudflare to the OSS origin
3. Enable proxy, HTTPS, Brotli, and Auto Minify when appropriate

## 4. Publish Updates
1. Replace changed files in OSS
2. Purge Cloudflare cache for `/cases/*` after Cases updates
3. Recheck `https://www.power-linkenergy.com/cases/`
```

- [ ] **Step 3: Start local preview**

Run:

```bash
py -3 -m http.server 8013
```

Expected:

```text
Serving HTTP on 0.0.0.0 port 8013
```

- [ ] **Step 4: Verify the upgraded pages in the browser**

Open and check:

```text
http://127.0.0.1:8013/cases/?v=9
http://127.0.0.1:8013/cases/small-data-center-backup-power/?v=9
```

Expected:

- overview page shows richer Cases hero plus case cards with image-slot behavior
- detail page shows hero media plus project-photos section or empty state

- [ ] **Step 5: Commit the delivery docs**

```bash
git add README.md docs/deployment/cloudflare-oss-launch.md
git commit -m "docs: add cases launch package guide"
```
