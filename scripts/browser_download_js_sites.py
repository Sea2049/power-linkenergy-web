# -*- coding: utf-8 -*-
"""使用 Playwright 抓取 JS 渲染站点的图片（需先安装 playwright 和 chromium）"""

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

# E盘依赖
sys.path.insert(0, r"E:\python_packages")
os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", r"E:\playwright_browsers")

OUTPUT_ROOT = Path("E:/supplier_images")
TARGET = 200

JS_SITES = [
    {"name": "山特电子（深圳）有限公司", "urls": [
        "https://www.santak.com.cn",
        "https://www.santak.com.cn/product",
        "https://www.santak.com.cn/case",
        "https://www.santak.com.cn/solution",
    ]},
    {"name": "珠海瓦特电力设备有限公司", "urls": [
        "http://www.gdwatt.com",
        "http://www.gdwatt.com/Products.html",
        "http://www.gdwatt.com/Case.html",
    ]},
    {"name": "广东普罗斯塔新能源科技有限公司", "urls": [
        "https://www.prostar-es.com",
        "https://www.prostarpower.com",
    ]},
    {"name": "Shanpu Technology (Guangdong) Co., Ltd.", "urls": [
        "https://www.gdshanpu.com",
        "http://www.gdshanpu.com",
    ]},
    {"name": "东莞市全一电气有限公司", "urls": [
        "http://www.dgqydy.com",
        "http://dgqydy.com",
    ]},
]


def classify(url: str, page: str) -> str:
    t = f"{url} {page}".lower()
    if any(k in t for k in ["case", "project", "案例", "工程"]):
        return "case"
    if any(k in t for k in ["scene", "gallery", "场景", "现场"]):
        return "scene"
    return "product"


def count_existing(out_dir: Path) -> int:
    if not out_dir.exists():
        return 0
    return len(list(out_dir.rglob("*.*")))


def safe_dirname(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', "_", name).strip()[:60]


async def extract_images_from_page(page, page_url: str) -> list[str]:
    await page.goto(page_url, wait_until="networkidle", timeout=60000)
    await page.wait_for_timeout(2000)
    urls = await page.evaluate("""
        () => {
            const urls = new Set();
            document.querySelectorAll('img').forEach(img => {
                ['src','data-src','data-original','data-lazy-src'].forEach(a => {
                    const v = img.getAttribute(a);
                    if (v && !v.startsWith('data:')) urls.add(v);
                });
            });
            document.querySelectorAll('[style*="background"]').forEach(el => {
                const m = el.style.backgroundImage.match(/url\\(["']?([^"')]+)["']?\\)/);
                if (m) urls.add(m[1]);
            });
            return [...urls];
        }
    """)
    full_urls = []
    for u in urls:
        full = urljoin(page_url, u)
        low = full.lower()
        if any(x in low for x in ["logo", "icon", "qrcode", "wechat", "avatar", "1x1", "blank"]):
            continue
        full_urls.append(full)
    return full_urls


async def download_with_playwright(site: dict):
    from playwright.async_api import async_playwright
    import requests

    out_dir = OUTPUT_ROOT / safe_dirname(site["name"])
    existing = count_existing(out_dir)
    if existing >= TARGET:
        print(f"跳过 {site['name']}: 已有 {existing} 张")
        return existing

    need = TARGET - existing
    downloaded = 0
    seen = set()
    session = requests.Session()
    session.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
            locale="zh-CN",
        )
        page = await context.new_page()

        for page_url in site["urls"]:
            if downloaded >= need:
                break
            try:
                img_urls = await extract_images_from_page(page, page_url)
                # 收集页面内链接
                links = await page.evaluate("""
                    () => [...document.querySelectorAll('a[href]')].map(a => a.href).slice(0, 50)
                """)
                for link in links:
                    if downloaded >= need:
                        break
                    low = link.lower()
                    if any(k in low for k in ["product", "case", "solution", "案例", "产品", "应用", "project"]):
                        try:
                            more = await extract_images_from_page(page, link)
                            img_urls.extend(more)
                        except Exception:
                            pass

                for img_url in img_urls:
                    if downloaded >= need or img_url in seen:
                        continue
                    seen.add(img_url)
                    cat = classify(img_url, page_url)
                    cat_dir = out_dir / cat
                    cat_dir.mkdir(parents=True, exist_ok=True)
                    n = len(list(cat_dir.glob("*"))) + 1
                    h = hashlib.md5(img_url.encode()).hexdigest()[:8]
                    try:
                        r = session.get(img_url, timeout=20)
                        if len(r.content) < 5000:
                            continue
                        ext = ".jpg"
                        if ".png" in img_url.lower():
                            ext = ".png"
                        elif ".webp" in img_url.lower():
                            ext = ".webp"
                        dest = cat_dir / f"{cat}_{n:03d}_{h}{ext}"
                        dest.write_bytes(r.content)
                        downloaded += 1
                    except Exception:
                        pass
            except Exception as e:
                print(f"  页面失败 {page_url}: {e}")

        await browser.close()

    total = count_existing(out_dir)
    print(f"{site['name']}: 新增 {downloaded}, 共 {total}")
    return total


async def main():
    results = []
    for site in JS_SITES:
        try:
            total = await download_with_playwright(site)
            results.append({"name": site["name"], "total": total})
        except Exception as e:
            print(f"失败 {site['name']}: {e}")
            results.append({"name": site["name"], "error": str(e)})

    out = OUTPUT_ROOT / "browser_download_report.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
