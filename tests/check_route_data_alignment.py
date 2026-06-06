import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_JS = ROOT / "assets/js/data.js"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_section(text: str, section: str) -> str:
    match = re.search(rf'"{section}": \[(.*?)\n  \]', text, re.S)
    if not match:
        raise AssertionError(f"missing section in data.js: {section}")
    return match.group(1)


def extract_slugs(section_text: str) -> set[str]:
    return set(re.findall(r'"slug": "([^"]+)"', section_text))


def route_slugs(folder: str) -> set[str]:
    return {
        path.parent.name
        for path in (ROOT / folder).glob("*/index.html")
    }


def main() -> None:
    data = read(DATA_JS)

    expected = {
        "solutions": extract_slugs(extract_section(data, "solutions")),
        "products": extract_slugs(extract_section(data, "products")),
        "cases": extract_slugs(extract_section(data, "cases")),
    }
    actual = {
        "solutions": route_slugs("solutions"),
        "products": route_slugs("products"),
        "cases": route_slugs("cases"),
    }

    for name in expected:
        missing_files = expected[name] - actual[name]
        missing_data = actual[name] - expected[name]
        if missing_files:
            raise AssertionError(f"{name} missing route files for slugs: {sorted(missing_files)}")
        if missing_data:
            raise AssertionError(f"{name} missing data entries for route slugs: {sorted(missing_data)}")

    print("route and data slugs align")


if __name__ == "__main__":
    main()
