import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_data() -> dict:
    raw = read("assets/js/data.js")
    return json.loads(raw.split("=", 1)[1].rsplit(";", 1)[0].strip())


def main() -> None:
    data = load_data()
    robots = read("robots.txt")
    llms = read("llms.txt")
    sitemap = read("sitemap.xml")
    home = read("index.html")
    about = read("about/index.html")
    contact = read("contact/index.html")

    assert (ROOT / "llms.txt").exists(), "missing llms.txt"
    assert "Powerlink Energy" in llms, "llms.txt should name the company"
    assert "/solutions/" in llms, "llms.txt should list solutions"
    assert data["site"]["email"] in llms, "llms.txt should include contact email"

    assert "GPTBot" in robots and "Allow: /" in robots, "robots.txt should allow AI crawlers"
    assert "sitemap.xml" in robots, "robots.txt should reference sitemap"

    assert "<lastmod>" in sitemap, "sitemap should include lastmod"

    for page_name, html in [("home", home), ("about", about), ("contact", contact)]:
        assert "application/ld+json" in html, f"{page_name} missing JSON-LD"
        assert 'meta name="robots"' in html, f"{page_name} missing robots meta"

    assert '"@type":"FAQPage"' in home or '"@type": "FAQPage"' in home, "home should include FAQPage schema"
    assert 'id="home-faq"' in home, "home should render visible FAQ section"

    assert '"@type":"Organization"' in home or '"@type": "Organization"' in home, "home should include Organization schema"

    detail = read("solutions/data-center-backup-power/index.html")
    assert "BreadcrumbList" in detail, "detail page should include breadcrumb schema"
    assert "Service" in detail, "solution detail should include Service schema"

    print("geo assets OK")


if __name__ == "__main__":
    main()
