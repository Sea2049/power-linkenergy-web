from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    readme = read("README.md")
    deployment = read("docs/deployment/cloudflare-oss-launch.md")
    page_404 = read("404.html")

    assert "<html lang=\"en\">" in page_404, "404 page language should match English site copy"
    assert "Form endpoint" in readme or "mailto" in readme, "README should describe the current contact submission model"
    assert "根路径" in readme, "README should state the supported deployment path strategy"
    assert "根路径" in deployment, "deployment guide should state the supported deployment path strategy"
    assert "generate_static_pages.py" in deployment, "deployment guide should document page generation"
    assert "`zh/`" in deployment, "deployment guide should document multilingual directories"
    assert "`404.html`" in deployment, "deployment guide should document the dedicated 404 file"
    assert "不要回退到 `index.html`" in deployment, "deployment guide should reject homepage fallback as long-term 404 behavior"

    print("deployment assumptions documented")


if __name__ == "__main__":
    main()
