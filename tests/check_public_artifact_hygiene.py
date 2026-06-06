from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> None:
    readme = read("README.md")
    deployment = read("docs/deployment/cloudflare-oss-launch.md")
    summary = read("downloads/supplier_images/summary.md")
    shortlist = read("downloads/supplier_images/shortlist.md")

    assert "不要上传" in deployment, "deployment guide should list excluded artifacts"
    assert ".xlsx" in deployment, "deployment guide should explicitly exclude spreadsheets"
    assert "scripts/" in deployment, "deployment guide should explicitly exclude scripts"
    assert "scripts/dev/" in deployment, "deployment guide should explicitly exclude dev scripts"
    assert "internal review" in summary.lower(), "supplier summary should stay marked as internal review"
    assert "must not be deployed" in shortlist.lower() or "internal" in shortlist.lower(), "supplier shortlist should clarify it is not a public deployment artifact"
    assert "上线包" in readme, "README should describe launch package boundaries"
    assert "`zh/`" in readme, "README should list multilingual directories in launch package"
    assert "assets/locales" in deployment, "deployment guide should exclude locale source files"

    print("public artifact hygiene OK")


if __name__ == "__main__":
    main()
