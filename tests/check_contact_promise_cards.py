from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    contact = read("contact/index.html")
    css = read("assets/css/site.css")

    assert 'class="info-card promise-card"' in contact, "missing promise card class"
    assert 'class="promise-card__head"' in contact, "missing promise card head"
    assert 'class="process-step__icon"' in contact, "missing shared icon style hook"
    assert ".promise-card" in css, "missing promise card styles"
    assert ".promise-card__head" in css, "missing promise card head styles"

    print("contact promise cards hooks OK")


if __name__ == "__main__":
    main()
