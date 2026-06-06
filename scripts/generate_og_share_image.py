"""Generate localized Open Graph share images for Powerlink Energy."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "images"
SIZE = (1200, 630)
BACKDROP = ROOT / "downloads/supplier_images/易事特集团股份有限公司/products/003-optimized.jpg"

LOCALE_COPY = {
    "en": {
        "filename": "og-share.jpg",
        "line1": "Integrated Power Solutions",
        "line2": "for Critical Applications",
        "line3": "UPS · Energy Storage · Telecom Power · Solar · Monitoring",
        "fonts": {
            "title": [("C:/Windows/Fonts/segoeuib.ttf", 64), ("C:/Windows/Fonts/arialbd.ttf", 64)],
            "body": [("C:/Windows/Fonts/segoeui.ttf", 30), ("C:/Windows/Fonts/arial.ttf", 30)],
            "small": [("C:/Windows/Fonts/segoeui.ttf", 24), ("C:/Windows/Fonts/arial.ttf", 24)],
        },
    },
    "zh": {
        "filename": "og-share-zh.jpg",
        "line1": "关键应用一体化电源解决方案",
        "line2": "数据中心 · 通信 · 储能 · 逆变 · 监控",
        "line3": "UPS · 储能系统 · 通信电源 · 光储 · 工业监控",
        "fonts": {
            "title": [("C:/Windows/Fonts/msyhbd.ttc", 58), ("C:/Windows/Fonts/simhei.ttf", 58)],
            "body": [("C:/Windows/Fonts/msyh.ttc", 28), ("C:/Windows/Fonts/simhei.ttf", 28)],
            "small": [("C:/Windows/Fonts/msyh.ttc", 22), ("C:/Windows/Fonts/simhei.ttf", 22)],
        },
    },
    "fr": {
        "filename": "og-share-fr.jpg",
        "line1": "Solutions d'alimentation intégrées",
        "line2": "pour applications critiques",
        "line3": "UPS · Stockage · Télécom · Solaire · Supervision",
        "fonts": {
            "title": [("C:/Windows/Fonts/segoeuib.ttf", 58), ("C:/Windows/Fonts/arialbd.ttf", 58)],
            "body": [("C:/Windows/Fonts/segoeui.ttf", 28), ("C:/Windows/Fonts/arial.ttf", 28)],
            "small": [("C:/Windows/Fonts/segoeui.ttf", 22), ("C:/Windows/Fonts/arial.ttf", 22)],
        },
    },
    "ru": {
        "filename": "og-share-ru.jpg",
        "line1": "Интегрированные силовые решения",
        "line2": "для критичных приложений",
        "line3": "UPS · Накопление · Телеком · Solar · Мониторинг",
        "fonts": {
            "title": [("C:/Windows/Fonts/segoeuib.ttf", 54), ("C:/Windows/Fonts/arialbd.ttf", 54)],
            "body": [("C:/Windows/Fonts/segoeui.ttf", 26), ("C:/Windows/Fonts/arial.ttf", 26)],
            "small": [("C:/Windows/Fonts/segoeui.ttf", 22), ("C:/Windows/Fonts/arial.ttf", 22)],
        },
    },
    "ar": {
        "filename": "og-share-ar.jpg",
        "line1": "حلول طاقة متكاملة",
        "line2": "للتطبيقات الحرجة",
        "line3": "UPS · تخزين · اتصالات · شمسي · مراقبة",
        "fonts": {
            "title": [("C:/Windows/Fonts/arialbd.ttf", 52), ("C:/Windows/Fonts/segoeuib.ttf", 52)],
            "body": [("C:/Windows/Fonts/arial.ttf", 26), ("C:/Windows/Fonts/segoeui.ttf", 26)],
            "small": [("C:/Windows/Fonts/arial.ttf", 22), ("C:/Windows/Fonts/segoeui.ttf", 22)],
        },
    },
}


def load_font(candidates: list[tuple[str, int]]) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path, size in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def draw_gradient(canvas: Image.Image) -> None:
    draw = ImageDraw.Draw(canvas)
    width, height = canvas.size
    for y in range(height):
        ratio = y / max(height - 1, 1)
        red = int(15 + (29 - 15) * ratio)
        green = int(27 + (78 - 27) * ratio)
        blue = int(45 + (216 - 45) * ratio)
        draw.line([(0, y), (width, y)], fill=(red, green, blue))
    overlay = Image.new("RGBA", canvas.size, (15, 27, 45, 120))
    canvas.paste(overlay, (0, 0), overlay)


def paste_backdrop(canvas: Image.Image) -> None:
    if not BACKDROP.exists():
        return
    with Image.open(BACKDROP) as photo:
        photo = photo.convert("RGB")
        target_height = canvas.height
        scale = target_height / photo.height
        target_width = int(photo.width * scale)
        photo = photo.resize((target_width, target_height), Image.Resampling.LANCZOS)
        if target_width > canvas.width * 0.62:
            crop_left = target_width - int(canvas.width * 0.62)
            photo = photo.crop((crop_left, 0, target_width, target_height))

        mask = Image.new("L", photo.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rectangle((0, 0, int(photo.width * 0.35), photo.height), fill=0)
        for x in range(int(photo.width * 0.35), photo.width):
            ratio = (x - photo.width * 0.35) / max(photo.width * 0.65, 1)
            mask_draw.line([(x, 0), (x, photo.height)], fill=int(255 * ratio))

        x_offset = canvas.width - photo.width
        canvas.paste(photo, (x_offset, 0), mask)


def render_locale_image(locale: str, copy: dict) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / copy["filename"]

    canvas = Image.new("RGB", SIZE, "#0f1b2d")
    draw_gradient(canvas)
    paste_backdrop(canvas)

    title_font = load_font(copy["fonts"]["title"])
    body_font = load_font(copy["fonts"]["body"])
    small_font = load_font(copy["fonts"]["small"])
    draw = ImageDraw.Draw(canvas)

    draw.text((72, 118), "Powerlink", font=title_font, fill="#ffffff")
    draw.text((72, 188), "energy", font=title_font, fill="#7cc9ff")
    draw.text((72, 286), copy["line1"], font=body_font, fill="#e8f0fb")
    draw.text((72, 340), copy["line2"], font=body_font, fill="#e8f0fb")
    draw.text((72, 430), copy["line3"], font=small_font, fill="#b7c7dd")
    draw.text((72, 500), "www.power-linkenergy.com", font=small_font, fill="#ffffff")

    accent = Image.new("RGBA", SIZE, (0, 0, 0, 0))
    accent_draw = ImageDraw.Draw(accent)
    accent_draw.rounded_rectangle((72, 548, 360, 556), radius=4, fill=(124, 201, 255, 220))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), accent).convert("RGB")
    canvas.save(output, format="JPEG", quality=88, optimize=True)
    return output


def main() -> None:
    for locale, copy in LOCALE_COPY.items():
        output = render_locale_image(locale, copy)
        print(f"wrote {output} ({output.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
