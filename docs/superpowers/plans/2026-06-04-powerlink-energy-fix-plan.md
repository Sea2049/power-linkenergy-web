# Powerlink Energy Website Fix Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the highest-risk issues in the current Powerlink Energy website without changing scope, so the site becomes crawlable, lead-friendly, resilient to data or route failures, safer to deploy, and less likely to expose internal assets or inconsistent claims.

**Architecture:** Keep the current static multi-page HTML/CSS/JavaScript structure, but shift critical pages from JS-only rendering to static-first rendering with JavaScript enhancement. Treat the contact form, detail-page fallback, shared data resilience, content-source consolidation, external resource cleanup, publication-package hardening, and deployment hardening as separate workstreams so they can be delivered and verified in small batches. Keep one canonical source for shared copy and contact data, explicitly separate public website assets from internal review materials, and document runtime assumptions such as root-path deployment and 404 behavior explicitly.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, Python smoke tests

---

## File Structure

### Modify

- `index.html`
- `about/index.html`
- `contact/index.html`
- `solutions/index.html`
- `products/index.html`
- `cases/index.html`
- `solutions/data-center-backup-power/index.html`
- `solutions/telecom-base-station-backup-power/index.html`
- `solutions/commercial-industrial-energy-storage/index.html`
- `solutions/residential-solar-storage/index.html`
- `solutions/edge-computing-power/index.html`
- `solutions/safety-monitoring-solutions/index.html`
- `products/ups-systems/index.html`
- `products/lithium-battery-systems/index.html`
- `products/hybrid-solar-inverters/index.html`
- `products/telecom-dc-power/index.html`
- `products/monitoring-industrial-cabling/index.html`
- `cases/small-data-center-backup-power/index.html`
- `cases/telecom-base-station-backup-power/index.html`
- `cases/commercial-industrial-energy-storage/index.html`
- `assets/js/site.js`
- `assets/js/data.js`
- `assets/css/site.css`
- `sitemap.xml`
- `README.md`
- `docs/deployment/cloudflare-oss-launch.md`
- `downloads/supplier_images/summary.md`
- `downloads/supplier_images/shortlist.md`
- `tests/check_about_process_layout.py`
- `tests/check_about_contact_visual.py`
- `tests/check_home_advantage_cards.py`
- `tests/check_detail_card_system.py`
- `tests/check_cases_visual_system.py`
- `tests/check_contact_promise_cards.py`

### Create

- `404.html`
- `tests/check_static_rendering.py`
- `tests/check_route_data_alignment.py`
- `tests/check_sitemap_routes.py`
- `tests/check_deployment_assumptions.py`
- `tests/check_public_artifact_hygiene.py`

### Responsibility Map

- `index.html`, overview pages, and detail pages: provide static-first page structure, essential SEO copy, and no-JS fallback readability.
- `contact/index.html`: define the real lead capture UX, fallback messaging, and conversion-safe submission flow.
- `assets/js/site.js`: keep shared rendering and navigation enhancement, but add runtime guards, fallback states, and safer route handling.
- `assets/js/data.js`: remain the single source of truth for shared content while tolerating missing optional fields.
- `assets/css/site.css`: support fallback layouts, error states, and accessible mobile navigation behavior.
- `404.html`: provide an explicit not-found page instead of relying on homepage fallback.
- `sitemap.xml`: only list routes that are directly crawlable and stable.
- `README.md` and `docs/deployment/cloudflare-oss-launch.md`: define supported preview, deployment, root-path, and cache/404 behavior after the fixes land.
- `downloads/supplier_images/*.md`: document internal-review-only asset rules and must not be treated as public website copy or deployment inventory.
- `tests/*`: validate static content presence, route/data alignment, sitemap correctness, and deployment assumptions.

---

### Task 1: Freeze current behavior and define acceptance criteria

**Files:**
- Reference: `index.html`
- Reference: `contact/index.html`
- Reference: `assets/js/site.js`
- Reference: `assets/js/data.js`
- Reference: `sitemap.xml`

- [ ] **Step 1: Capture the repair scope**

Document these defects as the accepted repair scope:

- home, overview, and detail pages are nearly empty before JavaScript runs
- contact form depends on `mailto:` instead of a real submission path
- detail pages fail silently when `slug` lookup misses
- shared shell rendering fails hard when critical data fields are absent
- about/contact content and shared contact values are maintained in both HTML and `assets/js/data.js`
- homepage metric counts are hard-coded instead of derived from content data
- cases positioning is inconsistent with the actual content being "reference frameworks"
- sitemap points to routes whose primary content is currently JS-injected
- critical pages depend on external `trae.ai` image URLs
- root-level spreadsheets, strategy docs, logs, and internal review files can be accidentally published if deployment follows broad "upload project root" guidance
- `downloads/supplier_images` contains internal-review-only provenance and permission notes but also sits under a web-served path
- README claims about image policy and launch contents are not fully aligned with the current implementation and repository layout
- deployment guidance still treats homepage fallback as an acceptable temporary 404 strategy
- the current site assumes domain-root hosting because routes and assets use absolute `/...` paths

- [ ] **Step 2: Define release gates**

Use these release gates for all following tasks:

- every route in `sitemap.xml` must contain visible HTML body copy before JS runs
- contact form must support a submission path that works without a local mail client
- invalid detail routes must show a human-readable fallback state
- missing optional data fields must not break header, footer, or hero rendering
- about/contact copy and shared contact values must have one canonical source
- homepage metrics must derive from the actual data collections
- critical first-screen pages must not depend on external AI image endpoints
- launch instructions must clearly separate public website files from internal spreadsheets, manifests, scripts, and review materials
- supplier review assets must not be exposed publicly unless usage rights and branding rules are explicitly cleared
- README and deployment docs must describe the site as it actually behaves after the fixes land
- production deployment must not depend on homepage fallback as the long-term 404 strategy
- navigation must remain usable on mobile and keyboard

- [ ] **Step 3: Commit the plan only**

```bash
git add docs/superpowers/plans/2026-06-04-powerlink-energy-fix-plan.md
git commit -m "docs: add website fix plan"
```

### Task 2: Restore static-first rendering for crawlability

**Files:**
- Modify: `index.html`
- Modify: `solutions/index.html`
- Modify: `products/index.html`
- Modify: `cases/index.html`
- Modify: `solutions/data-center-backup-power/index.html`
- Modify: `solutions/telecom-base-station-backup-power/index.html`
- Modify: `solutions/commercial-industrial-energy-storage/index.html`
- Modify: `solutions/residential-solar-storage/index.html`
- Modify: `solutions/edge-computing-power/index.html`
- Modify: `solutions/safety-monitoring-solutions/index.html`
- Modify: `products/ups-systems/index.html`
- Modify: `products/lithium-battery-systems/index.html`
- Modify: `products/hybrid-solar-inverters/index.html`
- Modify: `products/telecom-dc-power/index.html`
- Modify: `products/monitoring-industrial-cabling/index.html`
- Modify: `cases/small-data-center-backup-power/index.html`
- Modify: `cases/telecom-base-station-backup-power/index.html`
- Modify: `cases/commercial-industrial-energy-storage/index.html`
- Modify: `assets/js/site.js`
- Test: `tests/check_static_rendering.py`

- [ ] **Step 1: Add static HTML content to the homepage**

Replace empty homepage containers with server-delivered HTML for:

- shared header navigation
- hero title and summary
- applications list
- solution summary cards
- product category summary cards
- case/reference summary cards
- contact CTA strip
- shared footer contact block

Include a `<noscript>` notice and at least one crawlable navigation path even when JavaScript is unavailable.

Keep JavaScript enhancement limited to progressive improvements such as active states, richer cards, or optional visual replacement.

- [ ] **Step 2: Add static HTML content to overview pages**

Ensure `solutions/index.html`, `products/index.html`, and `cases/index.html` each ship with:

- visible H1
- explanatory body copy
- at least one full card list in HTML
- crawlable internal links to all detail routes
- static header/footer shell or an explicit no-JS fallback block

- [ ] **Step 3: Add static HTML content to detail pages**

Ensure every detail template ships with:

- visible H1
- category or context label
- one summary paragraph
- one section of bullet content or structured body copy
- contact CTA link back to `/contact/`
- no-JS readable body even if `assets/js/site.js` fails

- [ ] **Step 4: Reduce JavaScript to enhancement behavior**

Refactor `assets/js/site.js` so it:

- preserves existing static HTML when JS runs
- only fills optional blocks when placeholders exist
- does not blank out pre-rendered sections with `innerHTML = ""`

- [ ] **Step 5: Add a static-render verification test**

Create `tests/check_static_rendering.py` to assert these pages contain meaningful HTML before JS execution:

- `index.html`
- `solutions/index.html`
- `products/index.html`
- `cases/index.html`
- one detail page from each section

The test should verify presence of tags such as `h1`, body copy, and at least one route link.

- [ ] **Step 6: Commit**

```bash
git add index.html solutions products cases assets/js/site.js tests/check_static_rendering.py
git commit -m "fix: restore static-first rendering for core routes"
```

### Task 3: Replace the `mailto:` inquiry flow with a real submission path

**Files:**
- Modify: `contact/index.html`
- Modify: `assets/js/site.js`
- Modify: `assets/css/site.css`

- [ ] **Step 1: Select the submission strategy**

Choose one of these options before implementation:

- server-side form endpoint on the production domain
- third-party form handling service
- serverless function endpoint

Do not proceed until one option is explicitly chosen, because the HTML, JS, and UX differ by strategy.

- [ ] **Step 2: Update form UX requirements**

The final contact flow must include:

- required-field validation
- loading state
- success message in-page
- failure message in-page
- fallback contact copy with email and WhatsApp

- [ ] **Step 3: Remove submission coupling to local mail clients**

Delete the current JS behavior that forces:

- `event.preventDefault()`
- `window.location.href = "mailto:..."`

Replace it with one network submission path and one explicit fallback message.

- [ ] **Step 4: Add post-submit observability**

After implementation, the browser flow must reveal:

- success state if the endpoint returns success
- failure state if the endpoint rejects or times out
- no silent failure

- [ ] **Step 5: Commit**

```bash
git add contact/index.html assets/js/site.js assets/css/site.css
git commit -m "fix: replace mailto inquiry flow with real form submission"
```

### Task 4: Add route fallback and shared data resilience

**Files:**
- Modify: `assets/js/site.js`
- Modify: `assets/js/data.js`
- Modify: `assets/css/site.css`
- Test: `tests/check_route_data_alignment.py`

- [ ] **Step 1: Define safe defaults for shared data**

Guard these branches in `assets/js/site.js`:

- `data.site`
- `data.home`
- `data.solutions`
- `data.products`
- `data.cases`

Treat missing optional arrays as empty arrays and missing strings as empty strings or fallback labels.

- [ ] **Step 2: Add a visible fallback state for missing detail entries**

When `getEntry(collectionName, slug)` returns nothing, render a fallback section containing:

- "Content not found" headline
- short explanatory text
- link back to the parent list page
- link to `/contact/`

- [ ] **Step 3: Prevent shared shell crashes**

Header, footer, and hero rendering must not throw when any of these values are missing:

- `data.site.nav`
- `data.site.tagline`
- `data.site.email`
- `data.home.heroImage`
- `data.home.heroTitle`

- [ ] **Step 4: Add route and data alignment tests**

Create `tests/check_route_data_alignment.py` to verify:

- every detail HTML file uses a `data-slug` that exists in `assets/js/data.js`
- every slug in `assets/js/data.js` has a matching detail HTML file
- every collection name matches the expected route group

- [ ] **Step 5: Commit**

```bash
git add assets/js/site.js assets/js/data.js assets/css/site.css tests/check_route_data_alignment.py
git commit -m "fix: add detail fallback states and data guards"
```

### Task 5: Consolidate shared content sources and homepage metrics

**Files:**
- Modify: `about/index.html`
- Modify: `contact/index.html`
- Modify: `assets/js/data.js`
- Modify: `assets/js/site.js`

- [ ] **Step 1: Choose the canonical source for shared copy**

Decide one of these approaches and apply it consistently:

- keep About/Contact body copy primarily in HTML and remove duplicate unused blocks from `assets/js/data.js`
- move About/Contact body copy to `assets/js/data.js` and render it into the pages from one shared source

Do not keep the current mixed mode where the same business copy lives in both places without ownership.

- [ ] **Step 2: Normalize shared contact values**

Ensure email, WhatsApp, and domain exist in one canonical location and are consumed consistently by:

- shared footer
- homepage contact strip
- contact hero CTA
- contact details panel

- [ ] **Step 3: Replace hard-coded homepage metrics**

Stop rendering fixed values like `6 / 5 / 3 / 1` in `assets/js/site.js`. Derive visible counts from:

- `data.solutions.length`
- `data.products.length`
- `data.cases.length`

If one metric is intentionally editorial rather than computed, name it explicitly instead of presenting it as a count sourced from content.

- [ ] **Step 4: Commit**

```bash
git add about/index.html contact/index.html assets/js/data.js assets/js/site.js
git commit -m "fix: unify shared content sources and homepage metrics"
```

### Task 6: Reposition the Cases section and align content language

**Files:**
- Modify: `assets/js/data.js`
- Modify: `cases/index.html`
- Modify: `cases/small-data-center-backup-power/index.html`
- Modify: `cases/telecom-base-station-backup-power/index.html`
- Modify: `cases/commercial-industrial-energy-storage/index.html`
- Modify: `index.html`

- [ ] **Step 1: Decide the public naming**

Pick one content direction:

- keep the `/cases/` route but rename on-page copy to "Reference Frameworks"
- rename the route and all navigation labels to a non-case term

If the route stays as `/cases/`, every visible page must clarify that these are reference structures, not customer proof claims.

- [ ] **Step 2: Remove misleading wording**

Update homepage, overview, and detail copy so it does not imply:

- verified customer deployment
- named client endorsement
- production success claims unsupported by evidence

- [ ] **Step 3: Differentiate cases from solutions**

Adjust titles or subtitles so reference pages are not confused with solution pages that share similar names. Add context such as:

- framework
- reference structure
- planning reference
- deployment pattern

- [ ] **Step 4: Commit**

```bash
git add index.html cases assets/js/data.js
git commit -m "fix: align cases positioning with reference content"
```

### Task 7: Replace external image dependencies and harden deployment assumptions

**Files:**
- Modify: `assets/js/data.js`
- Modify: `about/index.html`
- Modify: `contact/index.html`
- Modify: `README.md`
- Modify: `docs/deployment/cloudflare-oss-launch.md`
- Create: `404.html`
- Test: `tests/check_deployment_assumptions.py`

- [ ] **Step 1: Replace critical external image URLs**

Remove `trae.ai` image URLs from critical first-screen content such as:

- homepage hero image
- about hero image
- contact hero image

Replace them with:

- repo-controlled static assets under the deployed site, or
- a production-approved stable CDN path under project ownership

- [ ] **Step 2: Define explicit 404 behavior**

Create `404.html` with:

- a visible not-found message
- link back to `/`
- link to `/contact/`

Update deployment guidance so homepage fallback is no longer the preferred steady-state behavior.

- [ ] **Step 3: Document the supported path strategy**

Choose and document one supported deployment model:

- root-path-only deployment, or
- path-agnostic deployment with relative URLs or configurable base path

Reflect the choice in both `README.md` and `docs/deployment/cloudflare-oss-launch.md`.

- [ ] **Step 4: Add a deployment assumption test**

The deployment-oriented test must not stop at 404 behavior. It must also protect the publication boundary.

Create `tests/check_deployment_assumptions.py` to verify:

- `404.html` exists
- `README.md` no longer presents the contact form as a mail-client flow once Task 3 is complete
- deployment docs mention the supported path strategy explicitly
- deployment docs prefer a real `404.html` over homepage fallback

- [ ] **Step 5: Commit**

```bash
git add assets/js/data.js about/index.html contact/index.html README.md docs/deployment/cloudflare-oss-launch.md 404.html tests/check_deployment_assumptions.py
git commit -m "fix: replace external hero assets and harden deployment guidance"
```

### Task 8: Harden publication package boundaries and supplier-asset compliance

**Files:**
- Modify: `README.md`
- Modify: `docs/deployment/cloudflare-oss-launch.md`
- Modify: `downloads/supplier_images/summary.md`
- Modify: `downloads/supplier_images/shortlist.md`
- Test: `tests/check_public_artifact_hygiene.py`

- [ ] **Step 1: Define the public deployment allowlist**

Document a strict allowlist for public deployment, limited to website runtime files such as:

- route HTML files
- `assets/`
- approved public assets under `downloads/` only if they are intentionally web-served
- `robots.txt`
- `sitemap.xml`
- `404.html`

Explicitly exclude from public upload:

- root-level `.xlsx`, `.docx`, `.log`, `.txt` business files
- `scripts/`
- internal review manifests and supplier sourcing notes
- test files and planning docs

- [ ] **Step 2: Mark supplier review materials as internal-only**

Update the supplier image documentation so it is unambiguous that:

- `summary.md`
- `shortlist.md`
- provenance metadata such as `manifest.csv`

are internal review artifacts and must not be deployed as part of the public website unless a separate approval process says otherwise.

- [ ] **Step 3: Align README claims with reality**

Make README statements consistent with the implemented site by clarifying:

- whether supplier or generated images are currently used
- what "official launch package" actually includes
- how to run the available smoke tests before release

- [ ] **Step 4: Add a publication hygiene test**

Create `tests/check_public_artifact_hygiene.py` to verify:

- `README.md` and deployment docs list the public allowlist or equivalent exclusion rules
- supplier review docs contain internal-use warnings
- the launch checklist does not imply uploading the whole repository blindly

- [ ] **Step 5: Commit**

```bash
git add README.md docs/deployment/cloudflare-oss-launch.md downloads/supplier_images/summary.md downloads/supplier_images/shortlist.md tests/check_public_artifact_hygiene.py
git commit -m "fix: harden public artifact boundaries and supplier asset guidance"
```

### Task 9: Improve SEO metadata, sitemap quality, and navigation accessibility

**Files:**
- Modify: `index.html`
- Modify: `about/index.html`
- Modify: `contact/index.html`
- Modify: `solutions/index.html`
- Modify: `products/index.html`
- Modify: `cases/index.html`
- Modify: detail pages under `solutions/`, `products/`, and `cases/`
- Modify: `assets/js/site.js`
- Modify: `assets/css/site.css`
- Modify: `sitemap.xml`
- Modify: `404.html`
- Test: `tests/check_sitemap_routes.py`

- [ ] **Step 1: Normalize page-level metadata**

For all index and detail pages, ensure:

- unique `<title>`
- unique description
- canonical URL
- Open Graph tags
- Twitter Card tags
- crawlable visible summary copy in the body

Add `noscript` fallback messaging where full parity is not possible, and add structured data only if the business facts are verifiable and stable.

- [ ] **Step 2: Review sitemap eligibility**

Keep only routes in `sitemap.xml` that meet both conditions:

- route exists as a real file
- route contains meaningful HTML content without requiring JS

- [ ] **Step 3: Improve mobile and keyboard navigation**

Update shared navigation behavior to support:

- `aria-controls`
- named navigation label
- `aria-current="page"` for the active route
- keyboard escape to close the menu
- click-outside close behavior
- stable active-nav matching without false positives on prefix collisions
- visible keyboard focus styles
- `<noscript>` fallback messaging on JS-heavy pages

- [ ] **Step 4: Improve image and motion accessibility/performance defaults**

For critical rendered images and hero media, add appropriate:

- `loading`
- `decoding`
- `fetchpriority` where justified
- explicit dimensions or aspect-ratio placeholders to reduce layout shift

Also add:

- `prefers-reduced-motion` handling for smooth scrolling and other motion-heavy behavior
- graceful degradation where `backdrop-filter` is unsupported or too expensive
- language consistency fixes for `404.html`

- [ ] **Step 5: Add sitemap verification test**

Create `tests/check_sitemap_routes.py` to verify:

- each `<loc>` maps to a real file in the repo
- each mapped file contains an `h1`
- each mapped file contains visible body copy

- [ ] **Step 6: Commit**

```bash
git add index.html about contact solutions products cases assets/js/site.js assets/css/site.css sitemap.xml 404.html tests/check_sitemap_routes.py
git commit -m "fix: improve crawlability sitemap quality and navigation accessibility"
```

### Task 10: Final validation and rollout checklist

**Files:**
- Verify: `index.html`
- Verify: `about/index.html`
- Verify: `contact/index.html`
- Verify: `solutions/**/index.html`
- Verify: `products/**/index.html`
- Verify: `cases/**/index.html`
- Verify: `assets/js/site.js`
- Verify: `assets/js/data.js`
- Verify: `assets/css/site.css`
- Verify: `sitemap.xml`
- Verify: `README.md`
- Verify: `docs/deployment/cloudflare-oss-launch.md`
- Verify: `404.html`
- Verify: `tests/check_static_rendering.py`
- Verify: `tests/check_route_data_alignment.py`
- Verify: `tests/check_sitemap_routes.py`
- Verify: `tests/check_deployment_assumptions.py`
- Verify: `tests/check_public_artifact_hygiene.py`
- Verify: `tests/check_home_advantage_cards.py`
- Verify: `tests/check_detail_card_system.py`
- Verify: `tests/check_cases_visual_system.py`
- Verify: `tests/check_contact_promise_cards.py`

- [ ] **Step 1: Run existing checks**

Run:

```bash
python tests/check_about_process_layout.py
python tests/check_about_contact_visual.py
python tests/check_home_advantage_cards.py
python tests/check_detail_card_system.py
python tests/check_cases_visual_system.py
python tests/check_contact_promise_cards.py
```

Expected: all existing checks pass.

- [ ] **Step 2: Run new regression checks**

Run:

```bash
python tests/check_static_rendering.py
python tests/check_route_data_alignment.py
python tests/check_sitemap_routes.py
python tests/check_deployment_assumptions.py
python tests/check_public_artifact_hygiene.py
```

Expected: all commands pass.

- [ ] **Step 3: Perform manual smoke testing**

Use a local static server and verify:

- home page renders meaningful HTML before JS enhancement
- contact page can submit without opening a mail client
- broken detail slug shows fallback state instead of blank content
- mobile nav opens, closes, and handles keyboard escape
- active navigation exposes `aria-current`
- keyboard focus remains visible across nav and buttons
- all sitemap routes are readable with JS disabled
- 404 route shows a real not-found page instead of the homepage
- launch package excludes internal spreadsheets, manifests, logs, and supplier review notes
- README and deployment docs match the implemented runtime behavior

- [ ] **Step 4: Commit**

```bash
git add index.html about contact solutions products cases assets/js assets/css sitemap.xml tests
git commit -m "fix: complete powerlink website repair pass"
```

---

## Self-Review

### Coverage

- Covers SEO crawlability, lead capture, detail-page fallback, shared-data resilience, content-source consolidation, external-resource cleanup, publication-package hygiene, deployment guidance, sitemap quality, and accessibility.
- Keeps the existing static architecture and avoids unnecessary framework migration.
- Adds targeted tests for the exact gaps found during review.

### Placeholder scan

- No `TODO` or `TBD`
- Each task lists exact files
- Each task ends with a concrete verification or commit step

### Risk notes

- Task 3 depends on a product decision for the real form submission path.
- Task 6 depends on a content decision about whether "Cases" remains the public route label.
- Task 7 depends on a deployment decision about whether root-path-only hosting is acceptable long term.
- Task 8 depends on an operational decision about where internal supplier-review assets should live if they remain in the repo.
- Script-level dependency hygiene for `scripts/collect_supplier_images.py` is still outside the main website-fix scope and may need a separate follow-up plan.
