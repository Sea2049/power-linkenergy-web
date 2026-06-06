import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def repo_path_from_url(url: str) -> Path:
    path = url.replace("https://www.power-linkenergy.com", "")
    if path == "/":
        return ROOT / "index.html"
    return ROOT / path.strip("/") / "index.html"


def main() -> None:
    sitemap = read("sitemap.xml")
    urls = re.findall(r"<loc>(.*?)</loc>", sitemap)
    if not urls:
        raise AssertionError("sitemap.xml has no loc entries")

    if 'xmlns:xhtml="http://www.w3.org/1999/xhtml"' not in sitemap:
        raise AssertionError("sitemap.xml missing xhtml namespace")
    if 'xhtml:link rel="alternate"' not in sitemap:
        raise AssertionError("sitemap.xml missing hreflang alternates")

    for url in urls:
        file_path = repo_path_from_url(url)
        if not file_path.exists():
            raise AssertionError(f"sitemap route file missing: {url}")
        html = file_path.read_text(encoding="utf-8")
        if "<h1>" not in html:
            raise AssertionError(f"sitemap route lacks static h1: {url}")
        if '<meta name="description"' not in html:
            raise AssertionError(f"sitemap route lacks description meta: {url}")
        if '<link rel="canonical"' not in html:
            raise AssertionError(f"sitemap route lacks canonical meta: {url}")

    print("sitemap routes OK")


if __name__ == "__main__":
    main()
