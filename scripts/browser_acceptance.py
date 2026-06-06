"""Lightweight browser acceptance checks for the static site."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
BASE = "http://127.0.0.1:8877"
SHOT_DIR = ROOT / "brainstorm" / "acceptance-screenshots"
PAGES = [
    ("home", "/"),
    ("contact", "/contact/"),
    ("about", "/about/"),
    ("solutions-overview", "/solutions/"),
    ("solution-detail", "/solutions/data-center-backup-power/"),
    ("product-detail", "/products/ups-systems/"),
    ("case-detail", "/cases/small-data-center-backup-power/"),
]


def broken_images(page) -> list[str]:
    return page.evaluate(
        """() => Array.from(document.images)
          .filter((img) => !img.complete || img.naturalWidth === 0)
          .map((img) => img.currentSrc || img.src)"""
    )


def social_meta(page) -> dict[str, str]:
    return page.evaluate(
        """() => ({
          ogImage: document.querySelector('meta[property="og:image"]')?.content || '',
          twitterImage: document.querySelector('meta[name="twitter:image"]')?.content || '',
          ogWidth: document.querySelector('meta[property="og:image:width"]')?.content || '',
        })"""
    )


def main() -> int:
    SHOT_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        for label, route in PAGES:
            url = f"{BASE}{route}"
            response = page.goto(url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_timeout(800)
            status = response.status if response else 0
            if status != 200:
                failures.append(f"{label}: HTTP {status} for {url}")
                continue

            broken = broken_images(page)
            if broken:
                failures.append(f"{label}: broken images -> {broken[:3]}")

            meta = social_meta(page)
            if not meta["ogImage"] or not meta["twitterImage"]:
                failures.append(f"{label}: missing og/twitter image meta")

            if label == "contact":
                if not page.locator(".hero-media img").count():
                    failures.append(f"{label}: missing contact hero image")
                elif "products/008-optimized.jpg" not in page.locator(".hero-media img").first.get_attribute("src"):
                    failures.append(f"{label}: contact hero image not updated")

            if label == "home":
                if not page.locator(".hero-media img").count():
                    failures.append(f"{label}: missing home hero image")
                elif "products/013-optimized.jpg" not in page.locator(".hero-media img").first.get_attribute("src"):
                    failures.append(f"{label}: home hero image not updated")

            if label.endswith("detail") and not page.locator(".hero-media--detail img, .card-media img").count():
                failures.append(f"{label}: missing detail hero/card image")

            page.screenshot(path=SHOT_DIR / f"{label}.png", full_page=False)

        browser.close()

    report = {
        "base": BASE,
        "pages_checked": len(PAGES),
        "screenshots": [str(SHOT_DIR / f"{label}.png") for label, _ in PAGES],
        "failures": failures,
        "passed": not failures,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
