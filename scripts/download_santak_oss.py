# -*- coding: utf-8 -*-
"""从山特 OSS CDN 及多页面抓取图片"""

import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

OUT = Path("E:/supplier_images/山特电子（深圳）有限公司")
TARGET = 200
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
    "Referer": "https://www.santak.com.cn/",
}

PAGES = [
    "https://www.santak.com.cn",
    "https://www.santak.com.cn/product",
    "https://www.santak.com.cn/case",
    "https://www.santak.com.cn/solution",
    "https://www.santak.com.cn/about",
    "https://www.santak.com.cn/news",
]

# 已知山特产品/案例图 OSS 路径模式
OSS_PREFIX = "https://osscn.santak.com.cn/"


def classify(url: str) -> str:
    t = url.lower()
    if any(k in t for k in ["case", "案例", "hangye", "行业", "客户", "news"]):
        return "case"
    if any(k in t for k in ["banner", "scene", "场景", "现场"]):
        return "scene"
    return "product"


def existing_count() -> int:
    if not OUT.exists():
        return 0
    return len(list(OUT.rglob("*.*")))


def download(session, url: str, dest: Path) -> bool:
    try:
        r = session.get(url, timeout=20)
        r.raise_for_status()
        if len(r.content) < 5000:
            return False
        ext = ".jpg"
        for e in [".png", ".webp", ".gif"]:
            if e in url.lower():
                ext = e
                break
        dest = dest.with_suffix(ext)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(r.content)
        return True
    except Exception:
        return False


def extract_from_html(html: str, base: str) -> list[str]:
    urls = set()
    for m in re.finditer(r'https?://osscn\.santak\.com\.cn/[^\s"\'<>\\]+\.(?:jpg|jpeg|png|webp|gif)[^\s"\'<>\\]*', html, re.I):
        urls.add(m.group(0).split("\\")[0])
    for m in re.finditer(r'["\']([^"\']*osscn\.santak\.com\.cn[^"\']+)["\']', html, re.I):
        urls.add(m.group(1))
    soup = BeautifulSoup(html, "lxml")
    for img in soup.find_all("img"):
        for a in ("src", "data-src", "data-original"):
            v = img.get(a)
            if v:
                urls.add(urljoin(base, v))
    return list(urls)


def main():
    session = requests.Session()
    session.headers.update(HEADERS)
    seen = set()
    counts = {"product": 0, "scene": 0, "case": 0, "other": 0}
    start = existing_count()

    # 从首页 HTML（含内嵌 JSON）提取
    for page in PAGES:
        if existing_count() - start >= TARGET:
            break
        try:
            r = session.get(page, timeout=20)
            r.encoding = "utf-8"
            for url in extract_from_html(r.text, page):
                if url in seen:
                    continue
                low = url.lower()
                if any(x in low for x in ["logo", "icon", "svg", "wechat", "footer", "qrcode", ".m4v"]):
                    continue
                seen.add(url)
                cat = classify(url)
                counts[cat] = counts.get(cat, 0) + 1
                h = hashlib.md5(url.encode()).hexdigest()[:8]
                dest = OUT / cat / f"{cat}_{counts[cat]:03d}_{h}"
                if download(session, url, dest):
                    pass
                if existing_count() - start >= TARGET:
                    break
        except Exception as e:
            print(f"page fail {page}: {e}")
        time.sleep(0.5)

    # 尝试 OSS 目录列举（部分公开资源）
    # 从产品页 API 抓取
    api_urls = [
        "https://www.santak.com.cn/api/product/list",
        "https://www.santak.com.cn/api/case/list",
    ]
    for api in api_urls:
        try:
            r = session.get(api, timeout=15)
            if r.status_code == 200:
                for url in extract_from_html(r.text, api):
                    if url in seen or existing_count() - start >= TARGET:
                        continue
                    low = url.lower()
                    if any(x in low for x in ["logo", "icon", "svg", "wechat"]):
                        continue
                    seen.add(url)
                    cat = classify(url)
                    counts[cat] = counts.get(cat, 0) + 1
                    h = hashlib.md5(url.encode()).hexdigest()[:8]
                    dest = OUT / cat / f"{cat}_{counts[cat]:03d}_{h}"
                    download(session, url, dest)
        except Exception:
            pass

    total = existing_count()
    print(json.dumps({"added": total - start, "total": total, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
