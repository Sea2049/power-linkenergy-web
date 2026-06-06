import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCALES = ["en", "zh", "fr", "ru", "ar"]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    css = read("assets/css/site.css")
    assert ".skip-link" in css, "missing skip link styles"
    assert ":focus-visible" in css, "missing focus-visible styles"
    assert ".detail-breadcrumb" in css, "missing breadcrumb styles"
    assert ".detail-toc" in css, "missing detail toc styles"
    assert 'html[dir="rtl"]' in css, "missing rtl styles"

    for locale in LOCALES:
        data = json.loads(read(f"assets/locales/{locale}.json"))
        assert "a11y" in data["ui"], f"{locale} missing ui.a11y"
        assert "tocTitle" in data["ui"]["detail"], f"{locale} missing ui.detail.tocTitle"

    home = read("index.html")
    detail = read("cases/small-data-center-backup-power/index.html")
    zh_detail = read("zh/cases/small-data-center-backup-power/index.html")

    for page in (home, detail, zh_detail):
        assert 'class="skip-link" href="#main-content"' in page, "missing skip link"
        assert '<main id="main-content">' in page, "missing main landmark id"
        assert '"@type":"Organization"' in page, "missing JSON-LD Organization"

    assert 'class="detail-breadcrumb"' in detail, "missing detail breadcrumb"
    assert 'class="detail-toc"' in detail, "missing detail toc"
    assert 'id="overview"' in detail, "missing anchored detail section"
    assert re.search(r'href="#overview"', detail), "missing toc anchor link"

    ar_home = read("ar/index.html")
    assert '<html lang="ar" dir="rtl">' in ar_home, "missing ar rtl html attrs"

    print("a11y and seo enhancements OK")


if __name__ == "__main__":
    main()
