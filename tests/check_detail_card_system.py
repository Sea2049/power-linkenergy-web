from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    site_js = read("assets/js/site.js")
    css = read("assets/css/site.css")

    assert "detail-info-card" in site_js, "missing detail info card renderer"
    assert "detail-cta" in site_js, "missing detail cta renderer"
    assert ".detail-info-card" in css, "missing detail info card styles"
    assert ".detail-cta" in css, "missing detail cta styles"
    assert ".detail-card-stack" in css, "missing detail card stack styles"

    print("detail card system hooks OK")


if __name__ == "__main__":
    main()
