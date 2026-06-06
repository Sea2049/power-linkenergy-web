from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_contains(text: str, needle: str, label: str) -> None:
    if needle not in text:
        raise AssertionError(f"missing {label}: {needle}")


def main() -> None:
    about = read("about/index.html")
    contact = read("contact/index.html")

    assert_contains(about, 'class="page-hero page-hero--visual"', "about visual hero")
    assert_contains(about, 'class="trust-grid"', "about trust grid")
    assert_contains(about, 'class="process-strip"', "about process strip")

    assert_contains(contact, 'class="page-hero page-hero--visual"', "contact visual hero")
    assert_contains(contact, 'class="contact-layout"', "contact layout")
    assert_contains(contact, 'class="response-promise"', "contact response promise")

    print("about/contact visual structure OK")


if __name__ == "__main__":
    main()
