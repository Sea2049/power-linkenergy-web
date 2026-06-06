from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    about = read("about/index.html")
    css = read("assets/css/site.css")

    assert 'class="card card--process"' in about, "missing dedicated process card class"
    assert 'class="process-step__icon"' in about, "missing process step icons"
    assert ".card--process" in css, "missing process card styles"
    assert ".card--process .process-strip" in css, "missing process-strip override"
    assert ".content-split--about" in css, "missing about split layout"
    assert ".process-step::after" in css, "missing horizontal connector"
    assert ".process-step__icon" in css, "missing icon styles"

    print("about process layout hooks OK")


if __name__ == "__main__":
    main()
