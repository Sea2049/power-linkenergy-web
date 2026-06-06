# -*- coding: utf-8 -*-
"""Create a premium home-hero scene from the containerized ESS render."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
PRODUCTS_DIR = ROOT / "downloads/supplier_images/易事特集团股份有限公司/products"
SOURCE = PRODUCTS_DIR / "012-optimized.jpg"
OUTPUT = PRODUCTS_DIR / "012-hero-optimized.jpg"
HERO_SIZE = (1600, 1200)


def crop_hero_frame(image: Image.Image) -> Image.Image:
    width, height = image.size
    target_width = int(height * 4 / 3)
    left = max(0, min(int(width * 0.34), width - target_width))
    return image.crop((left, 0, left + target_width, height))


def apply_vignette(image: Image.Image, strength: float = 0.14) -> Image.Image:
    width, height = image.size
    mask = Image.new("L", (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((-width * 0.06, -height * 0.08, width * 1.06, height * 1.08), fill=int(255 * (1 - strength)))
    mask = mask.filter(ImageFilter.GaussianBlur(max(width, height) // 10))
    dark = Image.new("RGB", (width, height), (15, 27, 45))
    return Image.composite(image, dark, mask)


def optimize_home_hero(source: Path = SOURCE, output: Path = OUTPUT) -> Path:
    image = Image.open(source).convert("RGB")
    image = crop_hero_frame(image)
    image = image.resize(HERO_SIZE, Image.Resampling.LANCZOS)
    image = ImageEnhance.Contrast(image).enhance(1.08)
    image = ImageEnhance.Color(image).enhance(1.1)
    image = ImageEnhance.Sharpness(image).enhance(1.15)
    image = apply_vignette(image)
    image.save(output, format="JPEG", quality=90, optimize=True)
    return output


if __name__ == "__main__":
    path = optimize_home_hero()
    print(f"saved {path} ({path.stat().st_size} bytes)")
