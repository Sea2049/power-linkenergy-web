# -*- coding: utf-8 -*-
"""从广东省UPS供应商官网下载产品图、场景图、案例图"""

import hashlib
import json
import os
import re
import sys
import time
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse, unquote

import pandas as pd
import requests
from bs4 import BeautifulSoup

# 配置
EXCEL_PATH = Path(__file__).resolve().parent.parent / "广东省UPS供应商分池版.xlsx"
OUTPUT_ROOT = Path("E:/supplier_images")
IMAGES_PER_SUPPLIER = 200
MAX_PAGES_PER_SITE = 80
REQUEST_TIMEOUT = 20
DELAY_BETWEEN_REQUESTS = 0.5
MIN_IMAGE_BYTES = 8000  # 过滤小图标
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# 优先爬取的页面关键词（产品/场景/案例）
PRIORITY_KEYWORDS = [
    "product", "products", "case", "cases", "solution", "solutions",
    "application", "applications", "project", "projects", "gallery",
    "scene", "scenes", "news", "about", "show", "portfolio",
    "产品", "案例", "解决方案", "应用", "项目", "场景", "新闻", "展示",
    "ups", "battery", "storage", "power", "inverter", "solar",
    "bess", "ess", "micro", "modular", "industrial",
]

SKIP_EXTENSIONS = {
    ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".zip", ".rar",
    ".mp4", ".avi", ".mov", ".wmv", ".mp3", ".svg",
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp"}


def safe_dirname(name: str, url: str) -> str:
    """生成安全的目录名"""
    slug = re.sub(r'[<>:"/\\|?*]', "_", name).strip()[:60]
    if not slug or slug == "nan":
        domain = urlparse(url).netloc.replace("www.", "")
        slug = domain
    return slug


def is_same_domain(base_url: str, link: str) -> bool:
    base = urlparse(base_url)
    target = urlparse(urljoin(base_url, link))
    if not target.netloc:
        return True
    base_host = base.netloc.replace("www.", "")
    target_host = target.netloc.replace("www.", "")
    return base_host == target_host or base_host.endswith("." + target_host) or target_host.endswith("." + base_host)


def should_skip_url(url: str) -> bool:
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in SKIP_EXTENSIONS)


def classify_image(url: str, page_url: str, alt: str = "") -> str:
    """分类：product / scene / case / other"""
    text = f"{url} {page_url} {alt}".lower()
    case_kw = ["case", "project", "application", "solution", "客户", "案例", "项目", "应用", "工程"]
    scene_kw = ["scene", "gallery", "show", "exhibition", "datacenter", "场景", "展示", "现场", "机房", "数据中心"]
    product_kw = ["product", "ups", "battery", "inverter", "solar", "bess", "modular", "series",
                  "产品", "型号", "系列", "电源", "储能", "模块"]

    if any(k in text for k in case_kw):
        return "case"
    if any(k in text for k in scene_kw):
        return "scene"
    if any(k in text for k in product_kw):
        return "product"
    return "other"


def extract_image_urls(soup: BeautifulSoup, page_url: str) -> list[tuple[str, str]]:
    """从页面提取图片 URL 及 alt 文本"""
    results = []
    seen = set()

    for img in soup.find_all("img"):
        for attr in ("data-src", "data-original", "data-lazy-src", "data-lazyload", "src"):
            src = img.get(attr)
            if not src:
                continue
            src = src.strip()
            if src.startswith("data:"):
                continue
            full = urljoin(page_url, src)
            if full not in seen:
                seen.add(full)
                results.append((full, img.get("alt", "") or ""))

    # background-image in style
    for tag in soup.find_all(style=True):
        style = tag.get("style", "")
        for match in re.finditer(r'url\(["\']?([^"\')\s]+)["\']?\)', style):
            full = urljoin(page_url, match.group(1))
            if full not in seen and not full.startswith("data:"):
                seen.add(full)
                results.append((full, ""))

    # og:image
    for meta in soup.find_all("meta", property="og:image"):
        content = meta.get("content")
        if content:
            full = urljoin(page_url, content)
            if full not in seen:
                seen.add(full)
                results.append((full, "og:image"))

    return results


def extract_links(soup: BeautifulSoup, page_url: str) -> list[str]:
    links = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("#") or href.startswith("javascript:") or href.startswith("mailto:"):
            continue
        full = urljoin(page_url, href)
        if should_skip_url(full):
            continue
        if is_same_domain(page_url, full):
            links.append(full.split("#")[0])
    return links


def link_priority(url: str) -> int:
    url_lower = url.lower()
    score = 0
    for i, kw in enumerate(PRIORITY_KEYWORDS):
        if kw in url_lower:
            score += (len(PRIORITY_KEYWORDS) - i) * 2
    return score


def get_extension(url: str, content_type: str = "") -> str:
    path = urlparse(url).path.lower()
    for ext in IMAGE_EXTENSIONS:
        if path.endswith(ext):
            return ext
    if "jpeg" in content_type or "jpg" in content_type:
        return ".jpg"
    if "png" in content_type:
        return ".png"
    if "webp" in content_type:
        return ".webp"
    if "gif" in content_type:
        return ".gif"
    return ".jpg"


def download_image(session: requests.Session, url: str, dest: Path) -> bool:
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT, stream=True)
        resp.raise_for_status()
        content_type = resp.headers.get("Content-Type", "")
        if "image" not in content_type and not any(url.lower().endswith(e) for e in IMAGE_EXTENSIONS):
            return False
        data = resp.content
        if len(data) < MIN_IMAGE_BYTES:
            return False
        ext = get_extension(url, content_type)
        dest = dest.with_suffix(ext)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def crawl_supplier(session: requests.Session, name: str, base_url: str, output_dir: Path) -> dict:
    """爬取单个供应商网站"""
    stats = {"product": 0, "scene": 0, "case": 0, "other": 0, "failed_pages": 0, "total_downloaded": 0}
    downloaded_urls = set()
    visited_pages = set()
    page_queue = deque()

    # 起始页面
    start_urls = [base_url]
    parsed = urlparse(base_url)
    for path in ["/products", "/product", "/cases", "/case", "/solutions", "/solution",
                 "/applications", "/application", "/news", "/about", "/gallery",
                 "/en/products", "/cn/products", "/product-list"]:
        start_urls.append(f"{parsed.scheme}://{parsed.netloc}{path}")

    for u in start_urls:
        page_queue.append(u)

    while page_queue and len(visited_pages) < MAX_PAGES_PER_SITE:
        total = sum(stats[k] for k in ("product", "scene", "case", "other"))
        if total >= IMAGES_PER_SUPPLIER:
            break

        page_url = page_queue.popleft()
        if page_url in visited_pages:
            continue
        visited_pages.add(page_url)

        try:
            time.sleep(DELAY_BETWEEN_REQUESTS)
            resp = session.get(page_url, timeout=REQUEST_TIMEOUT)
            resp.raise_for_status()
            if "text/html" not in resp.headers.get("Content-Type", "text/html"):
                continue
            resp.encoding = resp.apparent_encoding or "utf-8"
            soup = BeautifulSoup(resp.text, "lxml")
        except Exception:
            stats["failed_pages"] += 1
            continue

        # 提取并下载图片
        for img_url, alt in extract_image_urls(soup, page_url):
            total = sum(stats[k] for k in ("product", "scene", "case", "other"))
            if total >= IMAGES_PER_SUPPLIER:
                break
            if img_url in downloaded_urls:
                continue
            # 跳过明显无关的图片
            img_lower = img_url.lower()
            skip_patterns = ["logo", "icon", "avatar", "banner-ad", "qrcode", "qr-code", "wechat", "weixin", "facebook", "twitter", "linkedin", "youtube", "placeholder", "loading", "spacer", "blank.gif", "1x1"]
            if any(p in img_lower for p in skip_patterns):
                continue

            category = classify_image(img_url, page_url, alt)
            idx = stats[category] + 1
            url_hash = hashlib.md5(img_url.encode()).hexdigest()[:8]
            filename = f"{category}_{idx:03d}_{url_hash}"
            dest = output_dir / category / filename

            if download_image(session, img_url, dest):
                downloaded_urls.add(img_url)
                stats[category] += 1
                stats["total_downloaded"] += 1

        # 添加更多链接
        links = extract_links(soup, page_url)
        links.sort(key=link_priority, reverse=True)
        for link in links:
            if link not in visited_pages and link not in page_queue:
                page_queue.append(link)

    return stats


def load_suppliers() -> list[dict]:
    xl = pd.ExcelFile(EXCEL_PATH)
    suppliers = []
    for sheet in xl.sheet_names:
        if "说明" in sheet:
            continue
        df = pd.read_excel(EXCEL_PATH, sheet_name=sheet)
        url_col = name_col = None
        for c in df.columns:
            cs = str(c)
            if "官网" in cs:
                url_col = c
            if "公司" in cs:
                name_col = c
        if not url_col:
            continue
        for _, row in df.iterrows():
            url = str(row.get(url_col, "")).strip()
            name = str(row.get(name_col, "")).strip() if name_col else ""
            if url.startswith("http"):
                suppliers.append({"name": name, "url": url.rstrip("/"), "pool": sheet})
    return suppliers


def main():
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    suppliers = load_suppliers()
    print(f"共 {len(suppliers)} 家供应商待处理", flush=True)

    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"})

    summary = []
    for i, sup in enumerate(suppliers, 1):
        dirname = safe_dirname(sup["name"], sup["url"])
        out_dir = OUTPUT_ROOT / dirname
        print(f"\n[{i}/{len(suppliers)}] {sup['name']} - {sup['url']}", flush=True)
        try:
            stats = crawl_supplier(session, sup["name"], sup["url"], out_dir)
            record = {**sup, "dir": str(out_dir), **stats}
            summary.append(record)
            print(f"  完成: 产品{stats['product']} 场景{stats['scene']} 案例{stats['case']} 其他{stats['other']} 共{stats['total_downloaded']}", flush=True)
        except Exception as e:
            print(f"  失败: {e}", flush=True)
            summary.append({**sup, "error": str(e)})

    report_path = OUTPUT_ROOT / "download_report.json"
    report_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n报告已保存: {report_path}", flush=True)

    total_imgs = sum(r.get("total_downloaded", 0) for r in summary)
    print(f"全部完成，共下载 {total_imgs} 张图片", flush=True)


if __name__ == "__main__":
    main()
