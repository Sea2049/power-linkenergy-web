import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://www.power-linkenergy.com"
DEFAULT_OG = f"{SITE_URL}/assets/images/og-share.jpg"
LOCALIZED_OG = {
    "en": DEFAULT_OG,
    "zh": f"{SITE_URL}/assets/images/og-share-zh.jpg",
    "fr": f"{SITE_URL}/assets/images/og-share-fr.jpg",
    "ru": f"{SITE_URL}/assets/images/og-share-ru.jpg",
    "ar": f"{SITE_URL}/assets/images/og-share-ar.jpg",
}
PAGES = {
    "en": [
        "index.html",
        "about/index.html",
        "contact/index.html",
        "solutions/index.html",
        "products/ups-systems/index.html",
        "cases/small-data-center-backup-power/index.html",
    ],
    "zh": [
        "zh/index.html",
        "zh/contact/index.html",
    ],
}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_og_bundle(html: str, label: str) -> None:
    assert 'property="og:image"' in html, f"{label} missing og:image"
    assert 'name="twitter:image"' in html, f"{label} missing twitter:image"
    assert 'property="og:image:width"' in html, f"{label} missing og:image:width"
    assert 'property="og:image:height"' in html, f"{label} missing og:image:height"
    assert 'property="og:locale"' in html, f"{label} missing og:locale"
    assert 'property="og:locale:alternate"' in html, f"{label} missing og:locale:alternate"

    og_match = re.search(r'property="og:image" content="([^"]+)"', html)
    assert og_match, f"{label} missing og:image content"
    og_url = og_match.group(1)
    assert og_url.startswith(SITE_URL), f"{label} og:image must be absolute: {og_url}"


def main() -> None:
    for filename in (
        "og-share.jpg",
        "og-share-zh.jpg",
        "og-share-fr.jpg",
        "og-share-ru.jpg",
        "og-share-ar.jpg",
    ):
        path = ROOT / "assets/images" / filename
        assert path.exists(), f"missing assets/images/{filename}"

    for page in PAGES["en"]:
        html = read(page)
        assert_og_bundle(html, page)

    home = read("index.html")
    assert DEFAULT_OG in home, "home page should use default branded og image"
    assert 'property="og:locale" content="en_US"' in home, "english home missing og:locale"

    zh_home = read("zh/index.html")
    assert LOCALIZED_OG["zh"] in zh_home, "chinese home should use localized og image"
    assert 'property="og:locale" content="zh_CN"' in zh_home, "chinese home missing og:locale"

    for locale, pages in PAGES.items():
        for page in pages:
            html = read(page)
            locale_match = re.search(r'property="og:locale" content="([^"]+)"', html)
            assert locale_match, f"{page} missing og:locale"

    contact = read("contact/index.html")
    assert 'class="hero-media"' in contact, "contact page missing hero-media image"
    assert "深圳索瑞德电子有限公司/products/010-optimized.jpg" in contact, "contact hero image path missing"

    detail = read("products/ups-systems/index.html")
    assert "products/025-lineup-optimized.jpg" in detail, "detail page should use category image in og:image"
    assert DEFAULT_OG not in detail, "detail page should not fall back to default og image"

    print("og social meta OK")


if __name__ == "__main__":
    main()
