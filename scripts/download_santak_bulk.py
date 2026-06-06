# -*- coding: utf-8 -*-
import hashlib
import json
import re
import time
from pathlib import Path
from urllib.parse import urljoin

import requests

OUT = Path("E:/supplier_images/山特电子（深圳）有限公司")
TARGET = 200
HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.santak.com.cn/"}

PAGES = [
    "https://www.santak.com.cn/",
    "https://www.santak.com.cn/product/list",
    "https://www.santak.com.cn/solution/list",
    "https://www.santak.com.cn/case/list",
    "https://www.santak.com.cn/news/list",
    "https://www.santak.com.cn/about",
]

OSS_RE = re.compile(r"https://osscn\.santak\.com\.cn/[^\"'\\<>\s]+?\.(?:jpg|jpeg|png|webp|gif)(?:\?[^\"'\\<>\s]*)?", re.I)


def classify(url: str) -> str:
    t = url.lower()
    if any(k in t for k in ["case", "案例", "hangye", "行业", "solution", "方案"]):
        return "case"
    if any(k in t for k in ["banner", "scene", "场景"]):
        return "scene"
    return "product"


def existing():
    return len(list(OUT.rglob("*.*"))) if OUT.exists() else 0


def main():
    session = requests.Session()
    session.headers.update(HEADERS)
    seen = set()
    counts = {"product": 0, "scene": 0, "case": 0}
    start = existing()

    all_urls = set()
    for page in PAGES:
        try:
            r = session.get(page, timeout=25)
            r.encoding = "utf-8"
            for u in OSS_RE.findall(r.text):
                all_urls.add(u.split("\\")[0])
            # 产品详情链接
            for m in re.finditer(r'href="(/product/detail/[^"]+)"', r.text):
                detail = urljoin(page, m.group(1))
                try:
                    dr = session.get(detail, timeout=20)
                    for u in OSS_RE.findall(dr.text):
                        all_urls.add(u)
                except Exception:
                    pass
                time.sleep(0.3)
        except Exception as e:
            print("page error", page, e)

    print(f"found {len(all_urls)} oss urls")

    downloaded = 0
    for url in sorted(all_urls):
        if existing() - start >= TARGET:
            break
        low = url.lower()
        if any(x in low for x in ["导航栏", "logo", "icon", "footer", "wechat", "svg"]):
            continue
        if url in seen:
            continue
        seen.add(url)
        cat = classify(url)
        try:
            r = session.get(url, timeout=30)
            if r.status_code != 200 or len(r.content) < 5000:
                continue
            counts[cat] = counts.get(cat, 0) + 1
            h = hashlib.md5(url.encode()).hexdigest()[:8]
            ext = ".png" if ".png" in low else ".jpg"
            dest = OUT / cat / f"{cat}_{counts[cat]:03d}_{h}{ext}"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.content)
            downloaded += 1
        except Exception:
            pass

    total = existing()
    print(json.dumps({"added": total - start, "total": total, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
