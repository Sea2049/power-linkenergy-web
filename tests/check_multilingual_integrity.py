import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCALES = ["en", "zh", "fr", "ru", "ar"]


def load_locale(locale: str) -> dict:
    return json.loads((ROOT / "assets/locales" / f"{locale}.json").read_text(encoding="utf-8"))


def main() -> None:
    issues: list[str] = []

    base_keys = None
    base_slugs: dict[str, list[str]] = {}
    for locale in LOCALES:
        data = load_locale(locale)
        keys = set(data.keys())
        if base_keys is None:
            base_keys = keys
        elif keys != base_keys:
            issues.append(f"locale key mismatch in {locale}: {sorted(keys ^ base_keys)}")

        ui_keys = set(data["ui"].keys())
        required_ui = {"notFound", "mailto", "a11y"}
        missing_ui = required_ui - ui_keys
        if missing_ui:
            issues.append(f"{locale} ui missing keys: {sorted(missing_ui)}")

        if "tocTitle" not in data["ui"].get("detail", {}):
            issues.append(f"{locale} ui.detail missing tocTitle")

        for section in ("solutions", "products", "cases"):
            slugs = [item["slug"] for item in data[section]]
            if locale == "en":
                base_slugs[section] = slugs
            elif slugs != base_slugs[section]:
                issues.append(f"slug mismatch in {locale}/{section}")

    for locale in LOCALES:
        prefix = "" if locale == "en" else locale
        base = ROOT / prefix if prefix else ROOT
        required = [
            "index.html",
            "about/index.html",
            "contact/index.html",
            "solutions/index.html",
            "products/index.html",
            "cases/index.html",
        ]
        not_found = base / "404.html"
        if not not_found.exists():
            issues.append(f"missing 404 page: {locale}")

        for rel in required:
            if not (base / rel).exists():
                issues.append(f"missing page: {locale}:{rel}")

        for section in ("solutions", "products", "cases"):
            folder = base / section
            count = len(list(folder.glob("*/index.html"))) if folder.exists() else 0
            if count != len(base_slugs[section]):
                issues.append(
                    f"{locale}/{section} detail pages={count}, expected={len(base_slugs[section])}"
                )

        contact = (base / "contact/index.html").read_text(encoding="utf-8")
        if 'data-mailto-subject="' not in contact:
            issues.append(f"{locale} contact page missing mailto subject attribute")
        if 'data-mailto-fields="' not in contact:
            issues.append(f"{locale} contact page missing mailto fields attribute")

    for locale in LOCALES[1:]:
        prefix = locale
        for html in (ROOT / prefix).rglob("index.html"):
            raw = html.read_text(encoding="utf-8")
            body_match = re.search(r"<body[^>]*>(.*)</body>", raw, re.S)
            if not body_match:
                continue
            text = body_match.group(1)
            text = re.sub(r'<div class="language-switcher">.*?</div>', "", text, flags=re.S)
            bad = []
            for match in re.finditer(r'href="(/[^"]*)"', text):
                href = match.group(1)
                if href.startswith(
                    (
                        f"/{prefix}/",
                        "/assets/",
                        "/downloads/",
                        "/mailto:",
                        "/https://",
                        "/#",
                    )
                ):
                    continue
                if href in (f"/{prefix}", f"/{prefix}/"):
                    continue
                if href.startswith("/zh/") or href.startswith("/fr/") or href.startswith("/ru/") or href.startswith("/ar/"):
                    continue
                if href in ("/", "/zh/", "/fr/", "/ru/", "/ar/"):
                    continue
                if re.match(r"^/(solutions|products|cases|about|contact)(/|$)", href):
                    bad.append(href)
            if bad:
                issues.append(
                    f"non-localized content links in {html.relative_to(ROOT)}: {bad[:3]}"
                )

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    urls = re.findall(r"<loc>(.*?)</loc>", sitemap)
    if len(urls) != 20 * len(LOCALES):
        issues.append(f"sitemap has {len(urls)} urls, expected {20 * len(LOCALES)}")
    if 'xmlns:xhtml="http://www.w3.org/1999/xhtml"' not in sitemap:
        issues.append("sitemap.xml missing xhtml namespace")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    deployment = (ROOT / "docs/deployment/cloudflare-oss-launch.md").read_text(encoding="utf-8")
    for needle in ("zh/", "generate_static_pages.py", "assets/locales"):
        if needle not in readme:
            issues.append(f"README missing multilingual note: {needle}")
        if needle not in deployment:
            issues.append(f"deployment doc missing multilingual note: {needle}")

    page_404 = (ROOT / "404.html").read_text(encoding="utf-8")
    if "language-switcher" not in page_404:
        issues.append("root 404.html missing language switcher")

    og_images = [
        "assets/images/og-share.jpg",
        "assets/images/og-share-zh.jpg",
        "assets/images/og-share-fr.jpg",
        "assets/images/og-share-ru.jpg",
        "assets/images/og-share-ar.jpg",
    ]
    for image_path in og_images:
        if not (ROOT / image_path).exists():
            issues.append(f"missing localized og image: {image_path}")

    if issues:
        raise AssertionError("multilingual integrity issues:\n" + "\n".join(f"- {item}" for item in issues))

    print("multilingual integrity OK")


if __name__ == "__main__":
    main()
