from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    site_js = read("assets/js/site.js")
    data_js = read("assets/js/data.js")
    css = read("assets/css/site.css")

    assert "home-advantage-card" in site_js, "missing home advantage card renderer"
    assert "home-advantage-card__head" in site_js, "missing home advantage card head"
    assert '"icon":' in data_js, "missing advantage icon data"
    assert ".home-advantage-card" in css, "missing home advantage card styles"
    assert ".home-advantage-card__head" in css, "missing home advantage card head styles"

    print("home advantage card hooks OK")


if __name__ == "__main__":
    main()
