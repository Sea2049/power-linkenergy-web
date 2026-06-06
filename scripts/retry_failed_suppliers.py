# -*- coding: utf-8 -*-
"""补充下载失败或不足200张的供应商图片"""

import hashlib
import json
import re
import time
from collections import deque
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

OUTPUT_ROOT = Path("E:/supplier_images")
REPORT_PATH = OUTPUT_ROOT / "download_report.json"
TARGET = 200
MIN_IMAGE_BYTES = 5000

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# 备用域名/镜像
ALT_URLS = {
    "https://www.santak.com.cn": ["https://www.santak.com.cn/product", "https://www.santak.com.cn/case", "https://osscn.santak.com.cn"],
    "http://www.gdwatt.com": ["https://www.gdwatt.com", "http://www.gdwatt.com/Products.html", "http://www.gdwatt.com/Case.html"],
    "https://www.prostarpower.com": ["https://www.prostar-es.com", "https://www.prostarpower.com/en", "http://www.prostarpower.com"],
    "https://www.gdshanpu.com": ["http://www.gdshanpu.com", "https://gdshanpu.com"],
    "https://www.dgqydy.com": ["http://www.dgqydy.com", "http://dgqydy.com"],
    "https://www.gdxindun.com": ["https://www.xindunpower.cn", "http://www.gdxindun.com"],
    "http://www.szladis.com.cn": ["http://www.ladis.com.cn", "https://www.ladis.com.cn"],
    "https://www.upsen.net": ["http://www.upsen.net", "https://www.upsen.net/products"],
    "http://www.chinaupspower.com": ["https://www.chinaupspower.com", "http://chinaupspower.com"],
    "https://www.mustpower.cn": ["https://www.mustsolar.cn", "http://www.mustpower.cn"],
    "https://www.skepower.com": ["https://www.skepower.cn", "http://www.skepower.com"],
    "http://www.champion-battery.com.cn": ["https://www.champion-battery.com.cn", "http://champion-battery.com.cn"],
    "https://www.shanshuopower.cn": ["http://shanshuopower.cn", "http://www.shanshuopower.cn"],
    "https://www.dalybms.cn": ["http://www.dalybms.cn", "https://www.dalybms.com"],
    "https://www.desaybattery.com": ["https://www.desay.com", "http://www.desaybattery.com"],
    "http://aerto.cn": ["https://aerto.cn", "http://www.aerto.com.cn"],
    "https://www.andesups.com": ["http://www.andesups.com", "https://andesups.com/case"],
}


def count_existing(out_dir: Path) -> int:
    if not out_dir.exists():
        return 0
    return len(list(out_dir.rglob("*.*")))


def classify(url: str, page: str, alt: str = "") -> str:
    t = f"{url} {page} {alt}".lower()
    if any(k in t for k in ["case", "project", "案例", "工程", "客户"]):
        return "case"
    if any(k in t for k in ["scene", "gallery", "场景", "现场", "datacenter"]):
        return "scene"
    if any(k in t for k in ["product", "ups", "产品", "系列", "battery", "power"]):
        return "product"
    return "other"


def extract_all_images(html: str, base: str) -> list[tuple[str, str]]:
    results = []
    seen = set()
    soup = BeautifulSoup(html, "lxml")
    for img in soup.find_all("img"):
        for attr in ("data-src", "data-original", "data-lazy-src", "data-lazyload", "src", "data-url"):
            v = img.get(attr)
            if not v or v.startswith("data:"):
                continue
            full = urljoin(base, v.strip())
            if full not in seen:
                seen.add(full)
                results.append((full, img.get("alt", "") or ""))
    for m in re.finditer(r'["\']([^"\']+\.(?:jpg|jpeg|png|webp|gif)(?:\?[^"\']*)?)["\']', html, re.I):
        full = urljoin(base, m.group(1))
        if full not in seen and not full.startswith("data:"):
            seen.add(full)
            results.append((full, ""))
    for m in re.finditer(r'url\(["\']?([^"\')\s]+\.(?:jpg|jpeg|png|webp|gif)[^"\')\s]*)["\']?\)', html, re.I):
        full = urljoin(base, m.group(1))
        if full not in seen:
            seen.add(full)
            results.append((full, ""))
    return results


def download(session, url: str, dest: Path) -> bool:
    try:
        r = session.get(url, timeout=25, stream=True)
        r.raise_for_status()
        data = r.content
        if len(data) < MIN_IMAGE_BYTES:
            return False
        ct = r.headers.get("Content-Type", "")
        if "image" not in ct and not re.search(r'\.(jpe?g|png|webp|gif)', url, re.I):
            return False
        ext = ".jpg"
        for e in [".png", ".webp", ".gif", ".jpeg"]:
            if e in url.lower():
                ext = e if e != ".jpeg" else ".jpg"
                break
        if "png" in ct:
            ext = ".png"
        elif "webp" in ct:
            ext = ".webp"
        dest = dest.with_suffix(ext)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def crawl_more(session, base_urls: list[str], out_dir: Path, need: int) -> int:
    downloaded = 0
    seen_urls = set()
    visited = set()
    queue = deque(base_urls)
    cat_counts = {"product": 0, "scene": 0, "case": 0, "other": 0}

    # count existing per category
    for cat in cat_counts:
        cat_dir = out_dir / cat
        if cat_dir.exists():
            cat_counts[cat] = len(list(cat_dir.glob("*")))

    while queue and downloaded < need and len(visited) < 100:
        page = queue.popleft()
        if page in visited:
            continue
        visited.add(page)
        try:
            time.sleep(0.4)
            r = session.get(page, timeout=25, allow_redirects=True)
            if r.status_code >= 400:
                continue
            r.encoding = r.apparent_encoding or "utf-8"
            html = r.text
        except Exception:
            continue

        for img_url, alt in extract_all_images(html, page):
            if downloaded >= need:
                break
            if img_url in seen_urls:
                continue
            low = img_url.lower()
            if any(x in low for x in ["logo", "icon", "qrcode", "wechat", "avatar", "1x1", "blank"]):
                continue
            cat = classify(img_url, page, alt)
            cat_counts[cat] += 1
            h = hashlib.md5(img_url.encode()).hexdigest()[:8]
            dest = out_dir / cat / f"{cat}_{cat_counts[cat]:03d}_{h}"
            if download(session, img_url, dest):
                seen_urls.add(img_url)
                downloaded += 1

        soup = BeautifulSoup(html, "lxml")
        base_host = urlparse(page).netloc.replace("www.", "")
        for a in soup.find_all("a", href=True):
            href = urljoin(page, a["href"]).split("#")[0]
            h = urlparse(href).netloc.replace("www.", "")
            if h and (h == base_host or h.endswith("." + base_host)):
                if href not in visited and href not in queue:
                    queue.append(href)

    return downloaded


def main():
    report = json.loads(REPORT_PATH.read_text(encoding="utf-8"))
    session = requests.Session()
    session.headers.update(HEADERS)

    retry_log = []
    for item in report:
        out_dir = Path(item["dir"])
        existing = count_existing(out_dir)
        if existing >= TARGET:
            continue
        need = TARGET - existing
        base = item["url"]
        alt = ALT_URLS.get(base, [])
        urls = [base] + alt
        print(f"补充 {item['name']}: 已有{existing}, 需补{need}", flush=True)
        added = crawl_more(session, urls, out_dir, need)
        new_total = count_existing(out_dir)
        entry = {"name": item["name"], "before": existing, "added": added, "after": new_total}
        retry_log.append(entry)
        print(f"  -> 新增{added}, 现共{new_total}", flush=True)

    retry_path = OUTPUT_ROOT / "retry_report.json"
    retry_path.write_text(json.dumps(retry_log, ensure_ascii=False, indent=2), encoding="utf-8")
    total = sum(len(list(d.rglob("*.*"))) for d in OUTPUT_ROOT.iterdir() if d.is_dir())
    print(f"补充完成，总图片: {total}", flush=True)


if __name__ == "__main__":
    main()
