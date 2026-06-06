# -*- coding: utf-8 -*-
"""Build a premium UPS product lineup card image from supplier catalog art."""

from __future__ import annotations

import io
from pathlib import Path

import requests
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[2]
PRODUCTS_DIR = ROOT / "downloads/supplier_images/易事特集团股份有限公司/products"
SOURCE_URL = "https://www.eastups.com/u/cms/www/202309/15113836dd2o.jpg"
OUTPUT = PRODUCTS_DIR / "025-lineup-optimized.jpg"
CANVAS_SIZE = (1600, 1000)


def load_source_image() -> Image.Image:
    original = PRODUCTS_DIR / "025-source.jpg"
    if original.exists():
        return Image.open(original).convert("RGB")
    response = requests.get(
        SOURCE_URL,
        timeout=20,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content)).convert("RGB")
    image.save(original, format="JPEG", quality=95)
    return image


def clean_source(image: Image.Image) -> Image.Image:
    cleaned = image.copy()
    draw = ImageDraw.Draw(cleaned)
    bg = (252, 252, 252)
    for box in (
        (25, 95, 475, 285),
        (145, 1075, 355, 1105),
        (640, 548, 830, 592),
        (640, 898, 830, 938),
        (660, 1115, 815, 1145),
    ):
        draw.rectangle(box, fill=bg)
    return cleaned.crop((0, 0, image.width, 980))


def cutout_product(image: Image.Image, box: tuple[int, int, int, int], threshold: int = 236) -> Image.Image:
    crop = image.crop(box).convert("RGBA")
    pixels = crop.load()
    width, height = crop.size
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            if r >= threshold and g >= threshold and b >= threshold:
                pixels[x, y] = (r, g, b, 0)
            elif r >= threshold - 8 and g >= threshold - 8 and b >= threshold - 8:
                alpha = max(0, min(255, int((max(r, g, b) - (threshold - 8)) * 28)))
                pixels[x, y] = (r, g, b, 255 - alpha)
    return crop


def polish_sprite(sprite: Image.Image) -> Image.Image:
    rgb = ImageEnhance.Contrast(sprite.convert("RGB")).enhance(1.08)
    rgb = ImageEnhance.Color(rgb).enhance(0.96)
    rgb = ImageEnhance.Sharpness(rgb).enhance(1.12)
    alpha = sprite.split()[-1]
    return Image.merge("RGBA", (*rgb.split(), alpha))


def drop_shadow(sprite: Image.Image, blur: int = 28, offset: tuple[int, int] = (0, 22), opacity: int = 72) -> Image.Image:
    alpha = sprite.split()[-1]
    shadow = Image.new("RGBA", sprite.size, (15, 27, 45, 0))
    shadow.putalpha(alpha.point(lambda value: int(value * opacity / 255)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    canvas = Image.new("RGBA", (sprite.width + abs(offset[0]) + blur * 2, sprite.height + abs(offset[1]) + blur * 2), (0, 0, 0, 0))
    shadow_pos = (blur + max(offset[0], 0), blur + max(offset[1], 0))
    sprite_pos = (blur, blur)
    canvas.paste(shadow, shadow_pos, shadow)
    canvas.paste(sprite, sprite_pos, sprite)
    return canvas


def fit_sprite(sprite: Image.Image, max_width: int, max_height: int) -> Image.Image:
    ratio = min(max_width / sprite.width, max_height / sprite.height)
    size = (max(1, int(sprite.width * ratio)), max(1, int(sprite.height * ratio)))
    return sprite.resize(size, Image.Resampling.LANCZOS)


def studio_background(size: tuple[int, int]) -> Image.Image:
    width, height = size
    base = Image.new("RGB", size, "#eef4fb")
    draw = ImageDraw.Draw(base)
    for y in range(height):
        t = y / max(height - 1, 1)
        color = (
            int(220 + (238 - 220) * t),
            int(231 + (244 - 231) * t),
            int(247 + (251 - 247) * t),
        )
        draw.line([(0, y), (width, y)], fill=color)

    glow = Image.new("RGBA", size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    glow_draw.ellipse((width * 0.22, -height * 0.12, width * 0.88, height * 0.62), fill=(255, 255, 255, 72))
    glow_draw.ellipse((width * 0.58, height * 0.48, width * 1.02, height * 0.96), fill=(124, 201, 255, 16))
    base = Image.alpha_composite(base.convert("RGBA"), glow).convert("RGB")

    floor = Image.new("RGBA", size, (0, 0, 0, 0))
    floor_draw = ImageDraw.Draw(floor)
    floor_draw.ellipse((width * 0.12, height * 0.78, width * 0.9, height * 0.97), fill=(15, 27, 45, 22))
    base = Image.alpha_composite(base.convert("RGBA"), floor).convert("RGB")
    return base


def paste_sprite(canvas: Image.Image, sprite: Image.Image, center: tuple[int, int]) -> None:
    x = int(center[0] - sprite.width / 2)
    y = int(center[1] - sprite.height / 2)
    canvas.alpha_composite(sprite, (x, y))


def optimize_lineup_image(output: Path = OUTPUT) -> Path:
    source = clean_source(load_source_image())

    cabinet = polish_sprite(cutout_product(source, (40, 120, 470, 960)))
    module_large = polish_sprite(cutout_product(source, (545, 170, 1035, 560)))
    module_mid = polish_sprite(cutout_product(source, (560, 585, 1025, 900)))

    canvas = studio_background(CANVAS_SIZE).convert("RGBA")

    cabinet_sprite = drop_shadow(fit_sprite(cabinet, 500, 760))
    module_large_sprite = drop_shadow(fit_sprite(module_large, 560, 360))
    module_mid_sprite = drop_shadow(fit_sprite(module_mid, 500, 300))

    paste_sprite(canvas, cabinet_sprite, (420, 515))
    paste_sprite(canvas, module_large_sprite, (1120, 355))
    paste_sprite(canvas, module_mid_sprite, (1155, 715))

    result = ImageEnhance.Contrast(canvas.convert("RGB")).enhance(1.03)
    result = result.filter(ImageFilter.UnsharpMask(radius=1.2, percent=90, threshold=3))
    result.save(output, format="JPEG", quality=90, optimize=True)
    result.save(output.with_name("025.jpg"), format="JPEG", quality=92)
    return output


if __name__ == "__main__":
    path = optimize_lineup_image()
    print(f"saved {path} ({path.stat().st_size} bytes)")
