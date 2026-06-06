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
