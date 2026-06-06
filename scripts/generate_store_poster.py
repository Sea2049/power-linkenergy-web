"""Generate print-ready store wall poster for Powerlink Energy (3000mm x 2750mm)."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "images"

# Physical size: 3000mm wide x 2750mm tall @ 100 DPI
PHYSICAL_MM = (3000, 2750)
DPI = 100
SIZE = (
    int(PHYSICAL_MM[0] / 25.4 * DPI),
    int(PHYSICAL_MM[1] / 25.4 * DPI),
)

COLORS = {
    "bg_top": (15, 27, 45),
    "bg_bottom": (23, 45, 90),
    "brand": (29, 78, 216),
    "brand_dark": (23, 62, 168),
    "accent": (15, 118, 110),
    "white": (255, 255, 255),
    "muted": (180, 200, 230),
    "card": (20, 40, 75),
    "card_border": (45, 90, 160),
}


def load_font(candidates: list[tuple[str, int]]) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path, size in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


FONTS = {
    "brand": load_font([("C:/Windows/Fonts/segoeuib.ttf", 220), ("C:/Windows/Fonts/arialbd.ttf", 220)]),
    "brand_energy": load_font([("C:/Windows/Fonts/segoeuib.ttf", 220), ("C:/Windows/Fonts/arialbd.ttf", 220)]),
    "title": load_font([("C:/Windows/Fonts/msyhbd.ttc", 180), ("C:/Windows/Fonts/simhei.ttf", 180)]),
    "subtitle": load_font([("C:/Windows/Fonts/msyh.ttc", 72), ("C:/Windows/Fonts/simhei.ttf", 72)]),
    "category": load_font([("C:/Windows/Fonts/msyhbd.ttc", 56), ("C:/Windows/Fonts/simhei.ttf", 56)]),
    "advantage_title": load_font([("C:/Windows/Fonts/msyhbd.ttc", 52), ("C:/Windows/Fonts/simhei.ttf", 52)]),
    "advantage_body": load_font([("C:/Windows/Fonts/msyh.ttc", 40), ("C:/Windows/Fonts/simhei.ttf", 40)]),
    "contact": load_font([("C:/Windows/Fonts/segoeui.ttf", 48), ("C:/Windows/Fonts/arial.ttf", 48)]),
    "contact_cn": load_font([("C:/Windows/Fonts/msyh.ttc", 44), ("C:/Windows/Fonts/simhei.ttf", 44)]),
}


def draw_gradient_bg(draw: ImageDraw.ImageDraw, w: int, h: int) -> None:
    for y in range(h):
        t = y / max(h - 1, 1)
        r = int(COLORS["bg_top"][0] + (COLORS["bg_bottom"][0] - COLORS["bg_top"][0]) * t)
        g = int(COLORS["bg_top"][1] + (COLORS["bg_bottom"][1] - COLORS["bg_top"][1]) * t)
        b = int(COLORS["bg_top"][2] + (COLORS["bg_bottom"][2] - COLORS["bg_top"][2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def draw_glow_lines(draw: ImageDraw.ImageDraw, w: int, h: int) -> None:
    for i in range(8):
        y = int(h * 0.45 + i * 90)
        draw.line([(0, y), (w, y + 120)], fill=(29, 78, 216, 40), width=2)
    draw.ellipse([w - 900, h // 2 - 500, w + 200, h // 2 + 700], outline=(29, 78, 216), width=3)
    draw.ellipse([w - 700, h // 2 - 300, w + 100, h // 2 + 500], outline=(15, 118, 110), width=2)


def text_width(font: ImageFont.ImageFont, text: str) -> int:
    bbox = font.getbbox(text)
    return bbox[2] - bbox[0]


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    y: int,
    text: str,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    w: int,
) -> None:
    tw = text_width(font, text)
    draw.text(((w - tw) // 2, y), text, font=font, fill=fill)


def draw_category_card(
    draw: ImageDraw.ImageDraw,
    x: int,
    y: int,
    w: int,
    h: int,
    label: str,
) -> None:
    r = 28
    draw.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=COLORS["card"], outline=COLORS["card_border"], width=3)
    icon_cx = x + w // 2
    icon_cy = y + h // 2 - 40
    draw.ellipse([icon_cx - 50, icon_cy - 50, icon_cx + 50, icon_cy + 50], outline=COLORS["brand"], width=4)
    draw.line([icon_cx - 25, icon_cy, icon_cx + 25, icon_cy], fill=COLORS["accent"], width=4)
    draw.line([icon_cx, icon_cy - 25, icon_cx, icon_cy + 25], fill=COLORS["accent"], width=4)
    tw = text_width(FONTS["category"], label)
    draw.text((x + (w - tw) // 2, y + h - 95), label, font=FONTS["category"], fill=COLORS["white"])


def draw_advantage(
    draw: ImageDraw.ImageDraw,
    cx: int,
    y: int,
    title: str,
    body: str,
) -> None:
    draw.ellipse([cx - 55, y - 55, cx + 55, y + 55], fill=COLORS["accent"])
    tw = text_width(FONTS["advantage_title"], title)
    draw.text((cx - tw // 2, y + 80), title, font=FONTS["advantage_title"], fill=COLORS["white"])
    bw = text_width(FONTS["advantage_body"], body)
    draw.text((cx - bw // 2, y + 150), body, font=FONTS["advantage_body"], fill=COLORS["muted"])


def build_poster() -> Image.Image:
    w, h = SIZE
    img = Image.new("RGB", SIZE, COLORS["bg_top"])
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, w, h)
    draw_glow_lines(draw, w, h)

    margin = 120
    y = 140

    brand_power = "Powerlink"
    brand_energy = "energy"
    pw = text_width(FONTS["brand"], brand_power)
    ew = text_width(FONTS["brand_energy"], brand_energy)
    total = pw + ew + 20
    bx = (w - total) // 2
    draw.text((bx, y), brand_power, font=FONTS["brand"], fill=COLORS["white"])
    draw.text((bx + pw + 20, y), brand_energy, font=FONTS["brand_energy"], fill=COLORS["accent"])

    y += 260
    draw_centered_text(draw, y, "关键应用一体化电源解决方案", FONTS["title"], COLORS["white"], w)

    y += 220
    draw_centered_text(
        draw,
        y,
        "数据中心 · 通信站点 · 工商业储能 · 户用光储 · 边缘计算",
        FONTS["subtitle"],
        COLORS["muted"],
        w,
    )

    y += 160
    categories = ["UPS系统", "锂电池储能", "混合逆变器", "通信直流电源", "监控工业线缆"]
    card_w = (w - margin * 2 - 4 * 40) // 5
    card_h = 280
    for i, label in enumerate(categories):
        cx = margin + i * (card_w + 40)
        draw_category_card(draw, cx, y, card_w, card_h, label)

    y += card_h + 120
    showcase_h = int(h * 0.28)
    draw.rounded_rectangle(
        [margin, y, w - margin, y + showcase_h],
        radius=36,
        fill=(12, 30, 58),
        outline=COLORS["brand"],
        width=4,
    )
    draw_centered_text(
        draw,
        y + showcase_h // 2 - 60,
        "UPS · 储能系统 · 通信电源 · 光储逆变 · 工业监控",
        FONTS["subtitle"],
        COLORS["white"],
        w,
    )
    draw_centered_text(
        draw,
        y + showcase_h // 2 + 40,
        "Integrated Power Solutions for Critical Applications",
        FONTS["contact"],
        COLORS["muted"],
        w,
    )

    footer_y = h - 420
    draw.rectangle([0, footer_y, w, h], fill=COLORS["brand"])
    contact = "www.power-linkenergy.com  |  Bob-Wang@power-linkenergy.com  |  WhatsApp: +86 13534190063"
    draw_centered_text(draw, footer_y + 45, contact, FONTS["contact"], COLORS["white"], w)

    adv_y = footer_y - 280
    advantages = [
        ("灵活起订量", "满足不同项目需求"),
        ("快速方案匹配", "专业团队 高效响应"),
        ("一站式集成", "产品齐全 无缝对接"),
        ("快速响应支持", "本地服务 全程保障"),
    ]
    spacing = w // 4
    for i, (title, body) in enumerate(advantages):
        draw_advantage(draw, spacing // 2 + i * spacing, adv_y, title, body)

    return img


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    poster = build_poster()
    out_path = OUTPUT_DIR / "store-poster-3000x2750mm-100dpi.jpg"
    poster.save(out_path, format="JPEG", quality=95, dpi=(DPI, DPI), optimize=True)
    png_path = OUTPUT_DIR / "store-poster-3000x2750mm-100dpi.png"
    poster.save(png_path, format="PNG", dpi=(DPI, DPI))
    print(f"Saved: {out_path}")
    print(f"Saved: {png_path}")
    print(f"Size: {poster.size[0]} x {poster.size[1]} px @ {DPI} DPI")
    print(f"Physical: {PHYSICAL_MM[0]}mm x {PHYSICAL_MM[1]}mm")


if __name__ == "__main__":
    main()
