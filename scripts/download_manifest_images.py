"""Download optimized supplier images listed in manifest.csv."""

from __future__ import annotations

import csv
from pathlib import Path

import requests
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "downloads" / "supplier_images" / "manifest.csv"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    )
}
MAX_EDGE = 1920
JPEG_QUALITY = 85


def optimize_image(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(source) as img:
        img = img.convert("RGB")
        width, height = img.size
        if max(width, height) > MAX_EDGE:
            scale = MAX_EDGE / max(width, height)
            img = img.resize(
                (int(width * scale), int(height * scale)),
                Image.Resampling.LANCZOS,
            )
        img.save(target, format="JPEG", quality=JPEG_QUALITY, optimize=True)


def download_row(image_url: str, optimized_rel: str) -> tuple[str, bool]:
    optimized_path = ROOT / optimized_rel.replace("\\", "/")
    if optimized_path.exists() and optimized_path.stat().st_size > 0:
        return optimized_rel, False

    original_path = optimized_path.with_name(
        optimized_path.name.replace("-optimized.jpg", ".jpg")
    )
    if not original_path.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        for suffix in (".png", ".webp", ".gif"):
            candidate = optimized_path.with_name(
                optimized_path.name.replace("-optimized.jpg", suffix)
            )
            if candidate.exists():
                original_path = candidate
                break

    optimized_path.parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(image_url, headers=HEADERS, timeout=45)
    response.raise_for_status()

    temp = optimized_path.with_suffix(".download")
    temp.write_bytes(response.content)

    try:
        optimize_image(temp, optimized_path)
    except Exception:
        if original_path.suffix.lower() in {".jpg", ".jpeg"}:
            original_path.write_bytes(response.content)
            optimize_image(original_path, optimized_path)
        else:
            with Image.open(temp) as img:
                rgb = img.convert("RGB")
                rgb.save(optimized_path, format="JPEG", quality=JPEG_QUALITY, optimize=True)
    finally:
        if temp.exists():
            temp.unlink()

    return optimized_rel, True


def main() -> None:
    if not MANIFEST.exists():
        raise SystemExit(f"manifest not found: {MANIFEST}")

    seen: set[str] = set()
    downloaded = 0
    skipped = 0
    failed: list[str] = []

    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            optimized_rel = row["optimized_path"].replace("\\", "/")
            if optimized_rel in seen:
                continue
            seen.add(optimized_rel)

            try:
                _, was_downloaded = download_row(row["image_url"], optimized_rel)
            except Exception as exc:  # noqa: BLE001 - collect all failures for summary
                failed.append(f"{optimized_rel}: {exc}")
                continue

            if was_downloaded:
                downloaded += 1
            else:
                skipped += 1

    print(f"downloaded={downloaded} skipped={skipped} failed={len(failed)}")
    for item in failed[:10]:
        print(f"FAIL {item}")
    if len(failed) > 10:
        print(f"... and {len(failed) - 10} more failures")


if __name__ == "__main__":
    main()
