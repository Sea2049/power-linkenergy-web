# Powerlink Energy Cases Enhancement and Launch Package Design

## 1. Goal

This design covers the next delivery round for the Powerlink Energy official website with three linked objectives:

- strengthen the Cases overview hero so the section feels like a formal case center
- add real project image slots and reusable future case templates without making unverifiable project claims
- prepare a final launch package guide for Alibaba Cloud OSS + Cloudflare deployment

The direction remains trust-first. The site should look stronger and more complete while clearly separating real project assets from framework content.

## 2. Confirmed Decisions

### 2.1 Image Strategy

Use **real-image slots first**.

- Do not present supplier reference images as if they were completed customer projects
- Provide explicit image modules that can hold verified project photos later
- When no real project image is available, show a neutral empty-state treatment with honest explanatory copy

### 2.2 Working Direction

Use **Approach A: trust-first**.

- Improve visual hierarchy and professionalism
- Keep the verified detail card system and shared CTA system
- Expand Cases pages in a structured and maintainable way
- Deliver deployment guidance together with the page upgrade

## 3. Scope

This round includes:

- Cases overview hero enhancement
- Cases card image-slot support
- Cases detail hero media support
- Cases detail project-photos section
- reusable case data template updates
- launch package documentation for OSS + Cloudflare

This round does not include:

- publishing fake project stories
- creating a large real-case library
- adding a CMS
- changing the global information architecture

## 4. Design Principles

- **Trust before decoration**: visual upgrades cannot weaken credibility
- **Reuse before rebuild**: keep the existing visual system where it already works
- **Template-first content**: future case pages should be addable with structured data and minimal file duplication
- **Deployment-ready delivery**: the documentation should support practical go-live steps

## 5. Cases Overview Page Design

### 5.1 Hero Upgrade

Replace the current simple text hero with a richer structured hero that still fits the existing brand system.

The hero should include:

- main title and supporting description
- a short positioning statement explaining that Cases are expandable reference frameworks and future real projects
- a compact visual information block on the right side
- lightweight proof points such as:
  - Scenario-led
  - Expandable
  - Project-ready

### 5.2 Right-Side Hero Support Block

The right side of the hero should not depend on real customer photos. It should instead use structured visual content, such as:

- application tags for key verticals
- a methods-style information card
- a mini overview of how Powerlink Energy builds practical project references

This gives the hero more weight without creating asset risk.

### 5.3 Case Card Rules

The existing unified case card style remains the base component.

Each card should support:

- optional image area at the top
- region label
- application tag
- summary text
- details link

If an image is not present, the card should render a neutral visual placeholder instead of leaving an awkward gap.

## 6. Cases Detail Page Design

### 6.1 Hero Media Support

The case detail hero should support an optional media panel with the following priority:

1. real project hero image
2. neutral scenario illustration or structured placeholder
3. empty-state presentation with honest descriptive text

This keeps detail pages visually balanced even before verified project images are collected.

### 6.2 Body Content

The existing detail card stack remains unchanged as the primary information structure:

- Project Overview
- Customer Challenge
- Solution Design
- Main Configuration
- Delivery and Support
- Results

The shared detail CTA remains in place and should not be replaced with a case-only CTA pattern.

### 6.3 Project Photos Section

Add a dedicated section below the main detail cards for verified project visuals.

The section should support:

- 1 to 3 project photos
- optional caption or short note
- an empty state when photos are not yet available

Suggested empty-state messaging:

- Project photos will be added as verified project assets become available
- Contact us if you want a similar application structure for your market

## 7. Template and Data Model

The case content model should be extended with optional fields that allow both present and future use.

Suggested fields:

- `heroImage`
- `heroImageAlt`
- `gallery`
- `galleryNote`
- `projectStatus`
- `imageMode`

### 7.1 Field Intent

- `heroImage`: main detail hero asset
- `heroImageAlt`: accessibility text for the hero image
- `gallery`: array of project images for the project-photos section
- `galleryNote`: short trust-oriented note under the gallery or empty state
- `projectStatus`: labels such as `Reference Framework` or `Verified Project`
- `imageMode`: controls how the renderer behaves when no verified image exists

### 7.2 Rendering Rules

- if `heroImage` exists, show it in the detail hero
- if `gallery` contains images, render the gallery grid
- if no images exist, render structured empty-state blocks
- the overview page cards follow the same optional image-slot logic

## 8. Launch Package Design

### 8.1 Delivery Artifacts

The final launch package should include:

- complete static website files
- deployment notes for OSS
- Cloudflare connection and cache notes
- content maintenance notes for adding new Cases

### 8.2 OSS Deployment Guide

The deployment notes should explain:

- which folder contents are uploaded to OSS
- how to set the default index page
- how to configure the error page fallback
- how to replace files during later updates

### 8.3 Cloudflare Guide

The deployment notes should explain:

- how the `www.power-linkenergy.com` hostname points through Cloudflare
- how Cloudflare proxies traffic to OSS
- how to enable HTTPS and basic performance settings
- how to clear cache after content updates

### 8.4 Maintenance Notes

The launch package should include a short “how to add a new case” section covering:

- duplicate detail page template or add new detail folder
- add the case object in structured data
- add verified images later by filling optional image fields
- verify page rendering locally before upload

## 9. Implementation Boundaries

### 9.1 Files Likely Affected

- `cases/index.html`
- `cases/*/index.html`
- `assets/js/data.js`
- `assets/js/site.js`
- `assets/css/site.css`
- `README.md` or a dedicated deployment document

### 9.2 Files Not Required

- no build-system migration
- no backend integration
- no CMS wiring

## 10. Validation Plan

This work should be validated by:

- a focused test for the new Cases media/template hooks
- browser verification for the Cases overview page
- browser verification for one representative case detail page
- a quick review of deployment documentation completeness

## 11. Acceptance Criteria

- Cases overview hero looks more complete and more official
- Cases cards support image slots without pretending unverified images are real projects
- Case detail pages support hero media and a project-photos section
- the empty state is honest and visually intentional
- future Cases can be added with structured template fields
- deployment documentation is sufficient for OSS + Cloudflare go-live

## 12. Risks and Mitigations

### Risk: fake-project impression

Mitigation:

- keep reference-framework labeling explicit
- use neutral placeholders when verified photos are unavailable

### Risk: visual inconsistency

Mitigation:

- reuse the existing detail cards, CTA, spacing, and component language

### Risk: future maintenance friction

Mitigation:

- make image support data-driven and optional
- keep the new template fields small and well-defined
