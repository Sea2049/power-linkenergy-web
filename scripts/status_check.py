# -*- coding: utf-8 -*-
import json
from pathlib import Path

root = Path("E:/supplier_images")
report = json.loads((root / "download_report.json").read_text(encoding="utf-8")) if (root / "download_report.json").exists() else []
rows = []
for item in report:
    d = Path(item["dir"])
    actual = len(list(d.rglob("*.*"))) if d.exists() else 0
    rows.append((item["name"], actual, item.get("pool", "")))
rows.sort(key=lambda x: -x[1])
total = sum(r[1] for r in rows)
full = sum(1 for r in rows if r[1] >= 200)
partial = sum(1 for r in rows if 0 < r[1] < 200)
zero = sum(1 for r in rows if r[1] == 0)
size_mb = sum(f.stat().st_size for f in root.rglob("*.*") if f.is_file()) / 1024 / 1024
print(f"供应商: {len(rows)} | 满200: {full} | 部分: {partial} | 失败: {zero} | 总图: {total} | 大小: {size_mb:.1f}MB")
print()
for name, actual, pool in rows:
    tag = "满额" if actual >= 200 else ("部分" if actual > 0 else "失败")
    print(f"{tag:4} {actual:3d} | {name}")
