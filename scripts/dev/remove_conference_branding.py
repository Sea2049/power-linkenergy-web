# -*- coding: utf-8 -*-
"""Remove EAST / political branding from conference room hero photo."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
PRODUCTS_DIR = ROOT / "downloads/supplier_images/易事特集团股份有限公司/products"
SOURCE = PRODUCTS_DIR / "003-optimized.jpg"
OUTPUT = PRODUCTS_DIR / "003-clean-optimized.jpg"


def soft_region_mask(size: tuple[int, int], boxes: list[tuple[int, int, int, int]], blur: int = 32) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    for box in boxes:
        draw.rectangle(box, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(blur))


def blur_regions(image: Image.Image, boxes: list[tuple[int, int, int, int]], radius: int = 18, feather: int = 34) -> Image.Image:
    blurred = image.filter(ImageFilter.GaussianBlur(radius))
    mask = soft_region_mask(image.size, boxes, feather)
    base = image.copy()
    base.paste(blurred, (0, 0), mask)
    return base


def build_branding_mask(arr: np.ndarray) -> np.ndarray:
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)

    red = (r > 140) & (g < 130) & (b < 130) & (r > g + 28)
    gold = (r > 160) & (g > 115) & (b < 130) & (r > b + 30)
    blue_logo = (b > 140) & (r < 125) & (g < 155) & (b > r + 20)

    mask = red | gold | blue_logo
    upper = np.zeros(mask.shape, dtype=bool)
    upper[: int(arr.shape[0] * 0.58), :] = True
    mask &= upper

    mask_img = Image.fromarray((mask.astype(np.uint8) * 255))
    mask_img = mask_img.filter(ImageFilter.MaxFilter(9))
    mask_img = mask_img.filter(ImageFilter.GaussianBlur(3))
    return np.array(mask_img) > 80


def inpaint_masked(arr: np.ndarray, mask: np.ndarray, radius: int = 16) -> np.ndarray:
    out = arr.copy()
    height, width = mask.shape
    for y, x in np.argwhere(mask):
        y1, y2 = max(0, y - radius), min(height, y + radius + 1)
        x1, x2 = max(0, x - radius), min(width, x + radius + 1)
        patch = arr[y1:y2, x1:x2]
        patch_mask = mask[y1:y2, x1:x2]
        valid = patch[~patch_mask]
        if valid.size:
            out[y, x] = valid.mean(axis=0).astype(np.uint8)
    return out


def remove_conference_branding(source: Path = SOURCE, output: Path = OUTPUT) -> Path:
    image = Image.open(source).convert("RGB")
    w, h = image.size

    regions = [
        (int(w * 0.08), int(h * 0.02), int(w * 0.82), int(h * 0.52)),
        (int(w * 0.72), int(h * 0.04), int(w * 0.98), int(h * 0.64)),
        (int(w * 0.82), int(h * 0.36), int(w * 0.97), int(h * 0.52)),
    ]
    image = blur_regions(image, regions, radius=20, feather=38)
    image = blur_regions(
        image,
        [(int(w * 0.80), int(h * 0.30), int(w * 0.98), int(h * 0.58))],
        radius=28,
        feather=24,
    )

    arr = np.array(image)
    cleaned = inpaint_masked(arr, build_branding_mask(arr), radius=14)
    result = Image.fromarray(cleaned)
    result = ImageEnhance.Contrast(result).enhance(1.02)
    result = ImageEnhance.Color(result).enhance(0.97)
    result.save(output, format="JPEG", quality=88, optimize=True)
    return output


if __name__ == "__main__":
    path = remove_conference_branding()
    print(f"saved {path} ({path.stat().st_size} bytes)")
