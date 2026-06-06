# -*- coding: utf-8 -*-
"""Remove prominent EAST expo branding from supplier booth photos."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
PRODUCTS_DIR = ROOT / "downloads/supplier_images/易事特集团股份有限公司/products"
SOURCE = PRODUCTS_DIR / "001.jpg"
OUTPUT = PRODUCTS_DIR / "001-clean-optimized.jpg"


def build_logo_mask(arr: np.ndarray) -> np.ndarray:
    r = arr[:, :, 0].astype(np.int16)
    g = arr[:, :, 1].astype(np.int16)
    b = arr[:, :, 2].astype(np.int16)

    orange = (r > 155) & (g < 135) & (b < 95) & (r > g + 35) & (r > b + 60)
    red = (r > 165) & (g < 105) & (b < 105) & (r > g + 50)

    mask = orange | red
    region = np.zeros(mask.shape, dtype=bool)
    region[: int(arr.shape[0] * 0.52), :] = True
    mask &= region

    mask_img = Image.fromarray((mask.astype(np.uint8) * 255))
    mask_img = mask_img.filter(ImageFilter.MaxFilter(11))
    return np.array(mask_img) > 0


def inpaint_masked(arr: np.ndarray, mask: np.ndarray, radius: int = 14) -> np.ndarray:
    out = arr.copy()
    height, width = mask.shape
    coords = np.argwhere(mask)
    for y, x in coords:
        y1, y2 = max(0, y - radius), min(height, y + radius + 1)
        x1, x2 = max(0, x - radius), min(width, x + radius + 1)
        patch = arr[y1:y2, x1:x2]
        patch_mask = mask[y1:y2, x1:x2]
        valid = patch[~patch_mask]
        if valid.size:
            out[y, x] = valid.mean(axis=0).astype(np.uint8)
    return out


def remove_expo_logos(source: Path = SOURCE, output: Path = OUTPUT) -> Path:
    image = Image.open(source).convert("RGB")
    arr = np.array(image)
    cleaned = inpaint_masked(arr, build_logo_mask(arr), radius=14)
    result = Image.fromarray(cleaned)
    result = ImageEnhance.Contrast(result).enhance(1.02)
    result = ImageEnhance.Color(result).enhance(0.95)
    result.save(output, format="JPEG", quality=88, optimize=True)
    return output


if __name__ == "__main__":
    path = remove_expo_logos()
    print(f"saved {path} ({path.stat().st_size} bytes)")
