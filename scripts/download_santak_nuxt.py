# -*- coding: utf-8 -*-
"""从山特官网 NUXT 数据中提取 OSS 图片并下载"""

import hashlib
import json
import re
from pathlib import Path

import requests

OUT = Path("E:/supplier_images/山特电子（深圳）有限公司")
TARGET = 200
HEADERS = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.santak.com.cn/"}

PAGES = [
    "https://www.santak.com.cn/",
    "https://www.santak.com.cn/product/list",
]

OSS_RE = re.compile(
    r"https:(?:\\u002F|\\/|/){2}osscn\.santak\.com\.cn(?:\\u002F|\\/|/)[^\"'\\,\s]+?\.(?:jpg|jpeg|png|webp|gif)(?:\?[^\"'\\,\s]*)?",
    re.I,
)


def normalize_url(raw: str) -> str:
    return raw.replace("\\u002F", "/").replace("\\/", "/")


def classify(url: str) -> str:
    t = url.lower()
    if any(k in t for k in ["轨交", "高速", "铁路", "教育", "医院", "半导体", "钢铁", "建筑", "银行", "保险", "证券", "电网", "新能源", "移动", "广电", "石油", "央采", "税务", "工业", "机器", "特种", "医疗", "风电", "安防", "hangye", "行业"]):
        return "case"
    if any(k in t for k in ["banner", "scene"]):
        return "scene"
    return "product"


def main():
    session = requests.Session()
    session.headers.update(HEADERS)
    urls = set()
    for page in PAGES:
        r = session.get(page, timeout=30)
        r.encoding = "utf-8"
        for u in OSS_RE.findall(r.text):
            try:
                urls.add(normalize_url(u))
            except Exception:
                pass

    print(f"found {len(urls)} urls from nuxt html")

    skip = ["导航栏", "logo", "icon", "footer", "wechat", "test.png"]
    counts = {"product": 0, "scene": 0, "case": 0}
    downloaded = 0

    for url in sorted(urls):
        if downloaded >= TARGET:
            break
        if any(s in url for s in skip):
            continue
        cat = classify(url)
        try:
            r = session.get(url, timeout=40)
            if r.status_code != 200 or len(r.content) < 5000:
                continue
            counts[cat] += 1
            h = hashlib.md5(url.encode()).hexdigest()[:8]
            ext = ".png" if ".png" in url.lower() else ".jpg"
            dest = OUT / cat / f"{cat}_{counts[cat]:03d}_{h}{ext}"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(r.content)
            downloaded += 1
        except Exception:
            pass

    print(json.dumps({"downloaded": downloaded, "counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
