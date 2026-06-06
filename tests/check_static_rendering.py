from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_all(text: str, needles: list[str], label: str) -> None:
    for needle in needles:
        if needle not in text:
            raise AssertionError(f"{label} missing required static content: {needle}")


def main() -> None:
    home = read("index.html")
    solutions = read("solutions/index.html")
    products = read("products/index.html")
    cases = read("cases/index.html")
    detail = read("cases/small-data-center-backup-power/index.html")

    assert_all(
        home,
        [
            '<header class="site-header"',
            '<h1>Integrated Power Solutions for Critical Applications</h1>',
            'href="/solutions/"',
            '<noscript>'
        ],
        "home page",
    )
    assert_all(
        solutions,
        [
            '<header class="site-header"',
            '<h1>Scenario-Based Power Solutions</h1>',
            'href="/solutions/data-center-backup-power/"',
            '<noscript>'
        ],
        "solutions overview",
    )
    assert_all(
        products,
        [
            '<header class="site-header"',
            'href="/products/ups-systems/"',
            '<noscript>'
        ],
        "products overview",
    )
    assert_all(
        cases,
        [
            '<header class="site-header"',
            'Reference Frameworks',
            'href="/cases/small-data-center-backup-power/"',
            '<noscript>'
        ],
        "reference frameworks overview",
    )
    assert_all(
        detail,
        [
            '<header class="site-header"',
            '<h1>Small Data Center Backup Power</h1>',
            'href="/contact/"',
            '<noscript>'
        ],
        "detail page",
    )

    print("static rendering content OK")


if __name__ == "__main__":
    main()
