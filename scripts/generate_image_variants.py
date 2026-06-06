"""Generate placeholder image variants referenced by HTML but missing on disk.

Three variants are derived from existing base images so HTML/data references no
longer 404. These are placeholders only — the original "hero/lineup/clean"
variants were one-off retouched images whose source workflow is not in the
repo. Replace these later if dedicated artwork is produced.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parents[1]
SUPPLIER_DIR = ROOT / "downloads/supplier_images/易事特集团股份有限公司/products"

VARIANTS = [
    {
        "source": SUPPLIER_DIR / "012-optimized.jpg",
        "target": SUPPLIER_DIR / "012-hero-optimized.jpg",
        "mode": "hero",
    },
    {
        "source": SUPPLIER_DIR / "008-optimized.jpg",
        "target": SUPPLIER_DIR / "025-lineup-optimized.jpg",
        "mode": "lineup",
    },
    {
        "source": SUPPLIER_DIR / "001-optimized.jpg",
        "target": SUPPLIER_DIR / "001-clean-optimized.jpg",
        "mode": "clean",
    },
]


def render_hero(source: Path) -> Image.Image:
    """16:9 hero crop with slight contrast lift."""
    with Image.open(source) as base:
        base = base.convert("RGB")
        target_ratio = 16 / 9
        w, h = base.size
        current_ratio = w / h
        if current_ratio > target_ratio:
            new_w = int(h * target_ratio)
            left = (w - new_w) // 2
            base = base.crop((left, 0, left + new_w, h))
        else:
            new_h = int(w / target_ratio)
            top = (h - new_h) // 2
            base = base.crop((0, top, w, top + new_h))
        base = base.resize((1600, 900), Image.Resampling.LANCZOS)
        return ImageOps.autocontrast(base, cutoff=2)


def render_lineup(source: Path) -> Image.Image:
    """Wide banner-style lineup placeholder built from the base image."""
    with Image.open(source) as base:
        base = base.convert("RGB")
        base = base.resize((1200, 675), Image.Resampling.LANCZOS)
        canvas = Image.new("RGB", (1600, 800), "#0f1b2d")
        canvas.paste(base, ((1600 - 1200) // 2, (800 - 675) // 2))
        overlay = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.rectangle((0, 0, canvas.width, canvas.height), fill=(15, 27, 45, 70))
        canvas = Image.alpha_composite(canvas.convert("RGBA"), overlay).convert("RGB")
        return canvas


def render_clean(source: Path) -> Image.Image:
    """Gentle smoothing pass as a stand-in for a 'clean' retouched version."""
    with Image.open(source) as base:
        base = base.convert("RGB")
        smoothed = base.filter(ImageFilter.SMOOTH_MORE)
        return ImageOps.autocontrast(smoothed, cutoff=1)


RENDERERS = {
    "hero": render_hero,
    "lineup": render_lineup,
    "clean": render_clean,
}


def main() -> None:
    for v in VARIANTS:
        src: Path = v["source"]
        dst: Path = v["target"]
        if not src.exists():
            print(f"SKIP: source missing for {dst.name} (no {src.name})")
            continue
        if dst.exists():
            print(f"KEEP: {dst.name} already exists")
            continue
        img = RENDERERS[v["mode"]](src)
        dst.parent.mkdir(parents=True, exist_ok=True)
        img.save(dst, format="JPEG", quality=86, optimize=True)
        print(f"WROTE: {dst} ({dst.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
