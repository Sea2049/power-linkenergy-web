from __future__ import annotations

import csv
import io
import re
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
EXCEL_PATH = ROOT / "广东省UPS供应商-已联系.xlsx"
OUTPUT_ROOT = ROOT / "downloads" / "supplier_images"
MANIFEST_PATH = OUTPUT_ROOT / "manifest.csv"
SUMMARY_PATH = OUTPUT_ROOT / "summary.md"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    )
}

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp")
SKIP_IMAGE_HINTS = (
    "logo",
    "icon",
    "wechat",
    "qrcode",
    "qr",
    "avatar",
    "banner-small",
    "favicon",
    "loading",
)
PRODUCT_HINTS = (
    "product",
    "ups",
    "battery",
    "inverter",
    "module",
    "cabinet",
    "rack",
    "power",
)
CERT_HINTS = (
    "cert",
    "certificate",
    "certification",
    "honor",
    "award",
    "iso",
    "ul",
    "ce",
    "rohs",
    "tuv",
)
SCENE_HINTS = (
    "solution",
    "case",
    "application",
    "project",
    "data-center",
    "telecom",
    "industrial",
    "energy-storage",
    "solar",
)


def slugify(text: str) -> str:
    text = re.sub(r"[^\w\u4e00-\u9fff-]+", "-", str(text)).strip("-").lower()
    return text or "item"


def ensure_dirs() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]
    return df


def split_links(value: object) -> list[str]:
    if pd.isna(value):
        return []
    raw = str(value).replace("\n", " | ")
    parts = [part.strip() for part in raw.split("|")]
    return [part for part in parts if part.startswith(("http://", "https://"))]


def select_suppliers(limit: int = 6) -> list[dict]:
    xls = pd.ExcelFile(EXCEL_PATH)
    suppliers: list[dict] = []
    pool_order = {"主供池": 0, "补位池": 1}

    for sheet_name in xls.sheet_names:
        df = normalize_columns(pd.read_excel(EXCEL_PATH, sheet_name=sheet_name))
        for _, row in df.iterrows():
            website = row.get("官网")
            company = row.get("公司名称")
            priority = str(row.get("推荐优先级", "")).strip()
            if pd.isna(website) or pd.isna(company):
                continue
            website = str(website).strip()
            if not website.startswith(("http://", "https://")):
                continue
            if priority and priority != "A":
                continue

            suppliers.append(
                {
                    "pool": str(row.get("分池", sheet_name)).strip(),
                    "company": str(company).strip(),
                    "website": website,
                    "priority": priority or "A",
                    "source_links": split_links(row.get("来源链接")),
                }
            )

    suppliers.sort(key=lambda item: (pool_order.get(item["pool"], 99), item["company"]))
    return suppliers[:limit]


def collect_page_urls(supplier: dict) -> list[str]:
    pages = [supplier["website"]]
    for link in supplier["source_links"]:
        if len(pages) >= 3:
            break
        pages.append(link)
    seen = set()
    result = []
    for url in pages:
        if url not in seen:
            seen.add(url)
            result.append(url)
    return result


def fetch_html(session: requests.Session, url: str) -> str | None:
    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
        if "text/html" not in response.headers.get("content-type", ""):
            return None
        response.encoding = response.apparent_encoding or response.encoding
        return response.text
    except Exception:
        return None


def extract_image_urls(page_url: str, html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls = []
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("data-original")
        if not src:
            continue
        absolute = urljoin(page_url, src.strip())
        lower = absolute.lower()
        if any(hint in lower for hint in SKIP_IMAGE_HINTS):
            continue
        if lower.startswith(("http://", "https://")):
            urls.append(absolute)
    # de-duplicate but keep order
    seen = set()
    unique = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    return unique


def categorize(image_url: str, page_url: str) -> str:
    text = f"{image_url} {page_url}".lower()
    if any(hint in text for hint in CERT_HINTS):
        return "certificates"
    if any(hint in text for hint in SCENE_HINTS):
        return "scenes"
    if any(hint in text for hint in PRODUCT_HINTS):
        return "products"
    return "other"


def extension_from_url(url: str, content_type: str) -> str:
    parsed = urlparse(url)
    suffix = Path(parsed.path).suffix.lower()
    if suffix in IMAGE_EXTENSIONS:
        return suffix
    if "png" in content_type:
        return ".png"
    if "webp" in content_type:
        return ".webp"
    if "gif" in content_type:
        return ".gif"
    return ".jpg"


def download_image(
    session: requests.Session,
    supplier_slug: str,
    page_url: str,
    image_url: str,
    index: int,
) -> dict | None:
    try:
        response = session.get(image_url, timeout=30)
        response.raise_for_status()
        content_type = response.headers.get("content-type", "").lower()
        if "image" not in content_type:
            return None

        image = Image.open(io.BytesIO(response.content))
        width, height = image.size
        if width < 500 or height < 300:
            return None

        category = categorize(image_url, page_url)
        folder = OUTPUT_ROOT / supplier_slug / category
        folder.mkdir(parents=True, exist_ok=True)

        ext = extension_from_url(image_url, content_type)
        filename = f"{index:03d}{ext}"
        original_path = folder / filename
        optimized_path = folder / f"{index:03d}-optimized.jpg"

        original_path.write_bytes(response.content)

        processed = image.convert("RGB")
        max_side = max(processed.size)
        if max_side > 1800:
            scale = 1800 / max_side
            processed = processed.resize(
                (int(processed.width * scale), int(processed.height * scale))
            )
        processed.save(optimized_path, format="JPEG", quality=86, optimize=True)

        return {
            "supplier": supplier_slug,
            "category": category,
            "page_url": page_url,
            "image_url": image_url,
            "original_path": str(original_path.relative_to(ROOT)),
            "optimized_path": str(optimized_path.relative_to(ROOT)),
            "width": width,
            "height": height,
            "bytes": len(response.content),
        }
    except Exception:
        return None


def write_manifest(rows: Iterable[dict]) -> None:
    rows = list(rows)
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "supplier",
                "category",
                "page_url",
                "image_url",
                "original_path",
                "optimized_path",
                "width",
                "height",
                "bytes",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def write_summary(rows: list[dict], suppliers: list[dict]) -> None:
    grouped: dict[str, dict[str, int]] = {}
    for row in rows:
        grouped.setdefault(row["supplier"], {})
        grouped[row["supplier"]][row["category"]] = grouped[row["supplier"]].get(row["category"], 0) + 1

    lines = [
        "# Supplier Image Collection Summary",
        "",
        "> Note: Images are downloaded from supplier official public pages for internal review. Do not remove supplier watermarks or logos without permission.",
        "",
        f"- Source workbook: `{EXCEL_PATH.name}`",
        f"- Suppliers processed: {len(suppliers)}",
        f"- Images downloaded: {len(rows)}",
        "",
        "## Suppliers",
        "",
    ]

    for supplier in suppliers:
        slug = slugify(supplier["company"])
        counts = grouped.get(slug, {})
        parts = ", ".join(f"{key}: {value}" for key, value in sorted(counts.items())) or "no images saved"
        lines.append(f"- {supplier['company']} ({supplier['website']}) -> {parts}")

    lines += [
        "",
        "## Output",
        "",
        f"- Manifest: `{MANIFEST_PATH.relative_to(ROOT)}`",
        f"- Root folder: `{OUTPUT_ROOT.relative_to(ROOT)}`",
        "",
        "## Compliance",
        "",
        "- This workflow does not remove logos or watermarks from supplier images.",
        "- Use downloaded assets only after confirming brand and usage permissions.",
    ]
    SUMMARY_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    suppliers = select_suppliers()
    session = requests.Session()
    session.headers.update(HEADERS)

    rows: list[dict] = []
    for supplier in suppliers:
        slug = slugify(supplier["company"])
        image_urls: list[tuple[str, str]] = []
        for page_url in collect_page_urls(supplier):
            html = fetch_html(session, page_url)
            if not html:
                continue
            for image_url in extract_image_urls(page_url, html):
                image_urls.append((page_url, image_url))

        seen = set()
        deduped = []
        for page_url, image_url in image_urls:
            if image_url in seen:
                continue
            seen.add(image_url)
            deduped.append((page_url, image_url))

        for index, (page_url, image_url) in enumerate(deduped[:24], start=1):
            row = download_image(session, slug, page_url, image_url, index)
            if row:
                rows.append(row)

    write_manifest(rows)
    write_summary(rows, suppliers)
    print(f"suppliers={len(suppliers)} images={len(rows)} manifest={MANIFEST_PATH}")


if __name__ == "__main__":
    main()
