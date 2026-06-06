"""Deep-crawl supplier sites for poster assets: scene + product-collection images."""

from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "downloads" / "supplier_images" / "poster_assets"
CATALOG_PATH = OUTPUT_ROOT / "catalog.json"
MANIFEST_APPEND = ROOT / "downloads" / "supplier_images" / "poster_manifest.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
}

SUPPLIERS = [
    {
        "slug": "易事特集团股份有限公司",
        "pages": [
            "https://www.eastups.com/",
            "https://www.eastups.com/cn/Products/index.aspx",
            "https://www.eastups.com/cn/Products/UPS/index.aspx",
            "https://www.eastups.com/cn/Products/ESS/index.aspx",
            "https://www.eastups.com/cn/Solution/index.aspx",
            "https://www.eastups.com/cn/About/index.aspx",
        ],
    },
    {
        "slug": "深圳科士达科技股份有限公司",
        "pages": [
            "https://www.kstar.com/",
            "https://www.kstar.com/cn/product",
            "https://www.kstar.com/cn/product/ups",
            "https://www.kstar.com/cn/product/ess",
            "https://www.kstar.com/cn/solution",
            "https://www.kstar.com/cn/solution/data-center",
        ],
    },
    {
        "slug": "深圳索瑞德电子有限公司",
        "pages": [
            "https://www.soroups.com/",
            "https://www.soroups.com/product.html",
            "https://www.soroups.com/case.html",
            "https://www.soroups.com/about.html",
        ],
    },
    {
        "slug": "佛山市华葆电源设备有限公司",
        "pages": [
            "http://www.wahbou.com/",
            "http://www.wahbou.com/product/",
            "http://www.wahbou.com/solution/",
            "http://www.wahbou.com/about/",
        ],
    },
    {
        "slug": "山特电子（深圳）有限公司",
        "pages": [
            "https://www.santak.com.cn/",
        ],
    },
]

SKIP_HINTS = ("logo", "icon", "wechat", "qrcode", "qr", "avatar", "favicon", "loading", "blank")
SCENE_HINTS = (
    "solution", "case", "application", "project", "scene", "data-center", "datacenter",
    "telecom", "industrial", "energy", "solar", "wind", "storage", "station", "field",
    "方案", "案例", "应用", "场景", "储能", "数据中心", "基站", "光伏", "风电",
)
PRODUCT_COLLECTION_HINTS = (
    "product", "products", "series", "lineup", "ups", "battery", "inverter", "module",
    "cabinet", "rack", "power", "ess", "pv",
    "产品", "系列", "电源", "逆变", "电池",
)
BAD_SCENE_HINTS = ("meeting", "conference", "party", "certificate", "cert", "honor", "award", "会议", "党建")


def fetch_html(session: requests.Session, url: str) -> str | None:
    try:
        resp = session.get(url, timeout=12)
        resp.raise_for_status()
        if "text/html" not in resp.headers.get("content-type", ""):
            return None
        resp.encoding = resp.apparent_encoding or resp.encoding
        return resp.text
    except Exception:
        return None


def extract_images(page_url: str, html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    urls: list[str] = []
    for tag in soup.find_all(["img", "source"]):
        for attr in ("src", "data-src", "data-original", "data-lazy", "srcset"):
            val = tag.get(attr)
            if not val:
                continue
            if attr == "srcset":
                val = val.split(",")[0].strip().split()[0]
            absolute = urljoin(page_url, val.strip())
            lower = absolute.lower()
            if not lower.startswith(("http://", "https://")):
                continue
            if any(h in lower for h in SKIP_HINTS):
                continue
            urls.append(absolute)
    seen: set[str] = set()
    out: list[str] = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def classify(url: str, page_url: str, width: int, height: int) -> str:
    text = f"{url} {page_url}".lower()
    if any(h in text for h in BAD_SCENE_HINTS):
        return "skip"
    ratio = width / max(height, 1)
    is_wide = ratio >= 1.4
    is_large = width >= 800 and height >= 500

    scene_score = sum(1 for h in SCENE_HINTS if h in text)
    product_score = sum(1 for h in PRODUCT_COLLECTION_HINTS if h in text)

    if scene_score >= 2 or ("solution" in text or "案例" in text or "方案" in text):
        if is_large and not is_wide:
            return "scenes"
    if scene_score >= 1 and is_large and width >= 1000:
        return "scenes"

    if product_score >= 1 and is_wide and width >= 700:
        return "product_collections"
    if product_score >= 2:
        return "product_collections"
    if is_wide and width >= 900 and height >= 400:
        return "product_collections"

    if is_large and width >= 1200 and height >= 600:
        return "scenes"
    if is_wide:
        return "product_collections"
    return "other"


def download_one(
    session: requests.Session,
    supplier_slug: str,
    page_url: str,
    image_url: str,
    index: int,
) -> dict | None:
    try:
        resp = session.get(image_url, timeout=15)
        resp.raise_for_status()
        if "image" not in resp.headers.get("content-type", "").lower():
            return None
        img = Image.open(io.BytesIO(resp.content))
        width, height = img.size
        if width < 550 or height < 320:
            return None

        kind = classify(image_url, page_url, width, height)
        if kind == "skip":
            return None

        folder = OUTPUT_ROOT / supplier_slug / kind
        folder.mkdir(parents=True, exist_ok=True)
        out = folder / f"{index:03d}-optimized.jpg"
        if out.exists():
            return None

        rgb = img.convert("RGB")
        max_side = max(rgb.size)
        if max_side > 1920:
            scale = 1920 / max_side
            rgb = rgb.resize((int(rgb.width * scale), int(rgb.height * scale)), Image.Resampling.LANCZOS)
        rgb.save(out, format="JPEG", quality=88, optimize=True)

        rel = str(out.relative_to(ROOT)).replace("\\", "/")
        return {
            "supplier": supplier_slug,
            "kind": kind,
            "page_url": page_url,
            "image_url": image_url,
            "path": rel,
            "width": width,
            "height": height,
        }
    except Exception:
        return None


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update(HEADERS)

    rows: list[dict] = []
    counters: dict[str, int] = {}

    for supplier in SUPPLIERS:
        slug = supplier["slug"]
        counters[slug] = 0
        seen_urls: set[str] = set()

        for page_url in supplier["pages"]:
            html = fetch_html(session, page_url)
            if not html:
                print(f"SKIP page {page_url}", flush=True)
                continue
            images = extract_images(page_url, html)[:20]
            print(f"{slug}: {page_url} -> {len(images)} imgs", flush=True)
            for image_url in images:
                if image_url in seen_urls:
                    continue
                seen_urls.add(image_url)
                counters[slug] += 1
                row = download_one(session, slug, page_url, image_url, counters[slug])
                if row:
                    rows.append(row)
                    print(f"  + [{row['kind']}] {row['path']}", flush=True)
                if counters[slug] >= 40:
                    break
            if counters[slug] >= 40:
                break

    CATALOG_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    with MANIFEST_APPEND.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else ["path"])
        writer.writeheader()
        writer.writerows(rows)

    by_kind: dict[str, int] = {}
    for r in rows:
        by_kind[r["kind"]] = by_kind.get(r["kind"], 0) + 1
    print(f"\nTotal saved: {len(rows)}")
    print(f"By kind: {by_kind}")
    print(f"Catalog: {CATALOG_PATH}")


if __name__ == "__main__":
    main()
