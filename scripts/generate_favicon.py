"""Generate Powerlink Energy favicon set.

Produces:
- favicon.ico (16, 32, 48 px multi-resolution)
- assets/images/favicon-32x32.png
- assets/images/favicon-16x16.png
- assets/images/apple-touch-icon.png (180 px)

Visual style matches the in-site brandmark: dark navy background,
white "P", small accent dot.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "assets" / "images"
ICO_PATH = ROOT / "favicon.ico"

BG_TOP = (15, 27, 45)
BG_BOTTOM = (29, 78, 216)
TEXT_COLOR = (255, 255, 255)
ACCENT = (124, 201, 255)

FONT_CANDIDATES = [
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/arialbd.ttf",
]


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def draw_gradient(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)
    w, h = canvas.size
    for y in range(h):
        ratio = y / max(h - 1, 1)
        r = int(BG_TOP[0] + (BG_BOTTOM[0] - BG_TOP[0]) * ratio)
        g = int(BG_TOP[1] + (BG_BOTTOM[1] - BG_TOP[1]) * ratio)
        b = int(BG_TOP[2] + (BG_BOTTOM[2] - BG_TOP[2]) * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def render_icon(size: int) -> Image.Image:
    canvas = Image.new("RGB", (size, size), BG_TOP)
    draw_gradient(canvas)
    draw = ImageDraw.Draw(canvas)

    font_size = int(size * 0.72)
    font = load_font(font_size)

    text = "P"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1] - int(size * 0.04)
    draw.text((x, y), text, font=font, fill=TEXT_COLOR)

    if size >= 32:
        dot_r = max(2, int(size * 0.08))
        cx = size - int(size * 0.22)
        cy = size - int(size * 0.22)
        draw.ellipse(
            (cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r),
            fill=ACCENT,
        )
    return canvas


def main() -> None:
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    sizes_png = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "apple-touch-icon.png": 180,
    }
    for filename, size in sizes_png.items():
        img = render_icon(size)
        out = IMG_DIR / filename
        img.save(out, format="PNG", optimize=True)
        print(f"wrote {out} ({out.stat().st_size} bytes)")

    ico_sizes = [16, 32, 48]
    ico_images = [render_icon(s) for s in ico_sizes]
    ico_images[0].save(
        ICO_PATH,
        format="ICO",
        sizes=[(s, s) for s in ico_sizes],
        append_images=ico_images[1:],
    )
    print(f"wrote {ICO_PATH} ({ICO_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
