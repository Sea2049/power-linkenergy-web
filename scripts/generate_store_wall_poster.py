"""Generate print-ready store wall posters for Powerlink Energy.

Default physical size: 3620mm (W) x 2750mm (H) @ 100 DPI
Store scenario set: 3000mm (W) x 2750mm (H) @ 100 DPI
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


Image.MAX_IMAGE_PIXELS = 300_000_000

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "images"
SUPPLIER_IMAGES = ROOT / "downloads" / "supplier_images"

WIDTH_MM = 3620
HEIGHT_MM = 2750
STORE_WIDTH_MM = 3000
STORE_HEIGHT_MM = 2750
DPI = 100

BACKDROP_IMAGES = [
    "易事特集团股份有限公司/products/012-optimized.jpg",
    "易事特集团股份有限公司/products/002-optimized.jpg",
    "易事特集团股份有限公司/products/011-optimized.jpg",
    "易事特集团股份有限公司/products/010-optimized.jpg",
    "易事特集团股份有限公司/products/013-optimized.jpg",
    "深圳科士达科技股份有限公司/other/014-optimized.jpg",
]

HEADLINE = "关键应用一体化电源解决方案"
SUBHEAD = "数据中心 · 通信站点 · 工商业储能 · 户用光储 · 边缘计算"
PRODUCTS = [
    ("UPS 系统", "不间断电源 · 高可靠备电"),
    ("储能系统", "锂电池 · 工商业储能"),
    ("通信电源", "DC 电源 · 基站备电"),
    ("光储逆变", "混合逆变 · 户用光储"),
    ("工业监控", "线缆 · 监控配件"),
]
ADVANTAGES = ["灵活起订量", "快速方案匹配", "一站式集成", "快速响应支持"]
WEBSITE = "www.power-linkenergy.com"
WHATSAPP = "WhatsApp: +86 13534190063"
EMAIL = "Bob-Wang@power-linkenergy.com"
TAGLINE = "专业电源方案 · 小批量供货 · 全球项目支持"


def mm_to_px(mm: float) -> int:
    return int(mm / 25.4 * DPI)


def font_scale(base_mm: float) -> int:
    return mm_to_px(base_mm * 0.58)


def load_font(candidates: list[tuple[str, int]]) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path, size in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def cn_font(bold: bool, mm: float) -> ImageFont.ImageFont:
    size = font_scale(mm)
    if bold:
        return load_font([
            ("C:/Windows/Fonts/msyhbd.ttc", size),
            ("C:/Windows/Fonts/simhei.ttf", size),
        ])
    return load_font([
        ("C:/Windows/Fonts/msyh.ttc", size),
        ("C:/Windows/Fonts/simhei.ttf", size),
    ])


def en_font(bold: bool, mm: float) -> ImageFont.ImageFont:
    size = font_scale(mm)
    if bold:
        return load_font([
            ("C:/Windows/Fonts/segoeuib.ttf", size),
            ("C:/Windows/Fonts/arialbd.ttf", size),
        ])
    return load_font([
        ("C:/Windows/Fonts/segoeui.ttf", size),
        ("C:/Windows/Fonts/arial.ttf", size),
    ])


def resolve_backdrop_paths() -> list[Path]:
    paths: list[Path] = []
    for rel in BACKDROP_IMAGES:
        path = SUPPLIER_IMAGES / rel.replace("/", "\\")
        if path.exists():
            paths.append(path)
    return paths


def cover_resize(image: Image.Image, target_w: int, target_h: int) -> Image.Image:
    scale = max(target_w / image.width, target_h / image.height)
    new_w = int(image.width * scale)
    new_h = int(image.height * scale)
    resized = image.resize((new_w, new_h), Image.Resampling.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def open_photo(index: int = 0) -> Image.Image:
    paths = resolve_backdrop_paths()
    if not paths:
        return Image.new("RGB", (1920, 1080), (30, 40, 60))
    with Image.open(paths[index % len(paths)]) as img:
        return img.convert("RGB")


def apply_scrim(
    canvas: Image.Image,
    *,
    left_strength: int = 0,
    right_strength: int = 0,
    bottom_strength: int = 0,
    top_strength: int = 0,
    overall: int = 0,
    color: tuple[int, int, int] = (15, 27, 45),
) -> None:
    rgba = canvas.convert("RGBA")
    if overall:
        layer = Image.new("RGBA", canvas.size, (*color, overall))
        rgba = Image.alpha_composite(rgba, layer)

    width, height = canvas.size
    for name, strength in (
        ("left", left_strength),
        ("right", right_strength),
        ("bottom", bottom_strength),
        ("top", top_strength),
    ):
        if not strength:
            continue
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)
        if name == "left":
            end = int(width * 0.65)
            for x in range(end + 1):
                alpha = int(strength * (1 - x / max(end, 1)) ** 0.8)
                draw.line([(x, 0), (x, height)], fill=(*color, alpha))
        elif name == "right":
            start = int(width * 0.35)
            for x in range(start, width):
                alpha = int(strength * ((x - start) / max(width - start, 1)) ** 0.8)
                draw.line([(x, 0), (x, height)], fill=(*color, alpha))
        elif name == "bottom":
            zone = int(height * 0.18)
            for y in range(height - zone, height):
                alpha = int(strength * (y - (height - zone)) / max(zone, 1))
                draw.line([(0, y), (width, y)], fill=(*color, alpha))
        elif name == "top":
            zone = int(height * 0.12)
            for y in range(zone):
                alpha = int(strength * (1 - y / max(zone, 1)))
                draw.line([(0, y), (width, y)], fill=(*color, alpha))
        rgba = Image.alpha_composite(rgba, layer)
    canvas.paste(rgba.convert("RGB"), (0, 0))


def draw_brand(draw: ImageDraw.ImageDraw, x: int, y: int, *, light: bool = False) -> None:
    logo = en_font(True, 88)
    sub = en_font(True, 88)
    power_color = "#ffffff" if light else "#0f1b2d"
    energy_color = "#7cc9ff" if light else "#1d4ed8"
    draw.text((x, y), "Powerlink", font=logo, fill=power_color)
    pw = draw.textlength("Powerlink", font=logo)
    draw.text((x + pw + mm_to_px(6), y), "energy", font=sub, fill=energy_color)


def draw_footer(
    canvas: Image.Image,
    *,
    dark: bool = True,
    accent: str = "#1d4ed8",
) -> None:
    width, height = canvas.size
    footer_h = mm_to_px(150)
    footer_y = height - footer_h
    draw = ImageDraw.Draw(canvas)
    bg = (21, 35, 56) if dark else (255, 255, 255)
    text_main = "#ffffff" if dark else "#0f1b2d"
    text_sub = "#b7c7dd" if dark else "#57657a"
    draw.rectangle((0, footer_y, width, height), fill=bg)
    draw.line([(mm_to_px(80), footer_y), (width - mm_to_px(80), footer_y)], fill=accent, width=mm_to_px(2))
    y = footer_y + mm_to_px(32)
    mx = mm_to_px(100)
    draw.text((mx, y), WEBSITE, font=cn_font(True, 30), fill=text_main)
    draw.text((mx + mm_to_px(820), y), WHATSAPP, font=cn_font(False, 22), fill=text_sub)
    draw.text((mx + mm_to_px(1450), y), EMAIL, font=cn_font(False, 22), fill=text_sub)
    draw.text((mx, y + mm_to_px(48)), TAGLINE, font=cn_font(False, 20), fill=text_sub)


def save_poster(canvas: Image.Image, filename: str) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / filename
    canvas.save(output, format="JPEG", quality=92, optimize=True, dpi=(DPI, DPI))
    preview = output.with_name(output.stem + "-preview.jpg")
    thumb = canvas.copy()
    thumb.thumbnail((1600, 1200), Image.Resampling.LANCZOS)
    thumb.save(preview, quality=90)
    return output


# ── Style 1: 企业极简 ──────────────────────────────────────────
def render_style01_minimal() -> Path:
    width, height = mm_to_px(WIDTH_MM), mm_to_px(HEIGHT_MM)
    canvas = Image.new("RGB", (width, height), "#f3f7fc")
    draw = ImageDraw.Draw(canvas)

    panel_w = int(width * 0.44)
    draw.rectangle((0, 0, panel_w, height), fill="#ffffff")
    draw.line([(panel_w, 0), (panel_w, height)], fill="#d5e0ef", width=mm_to_px(2))

    with open_photo(0) as photo:
        canvas.paste(cover_resize(photo, width - panel_w, height), (panel_w, 0))

    apply_scrim(canvas, left_strength=40, overall=15, color=(255, 255, 255))
    rgba = canvas.convert("RGBA")
    fade = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    fd = ImageDraw.Draw(fade)
    for x in range(panel_w - mm_to_px(80), panel_w + mm_to_px(60)):
        ratio = (x - (panel_w - mm_to_px(80))) / max(mm_to_px(140), 1)
        fd.line([(x, 0), (x, height)], fill=(255, 255, 255, int(220 * min(1, ratio))))
    canvas.paste(Image.alpha_composite(rgba, fade).convert("RGB"), (0, 0))

    draw = ImageDraw.Draw(canvas)
    mx, my = mm_to_px(90), mm_to_px(90)
    draw_brand(draw, mx, my, light=False)
    draw.rounded_rectangle(
        (mx, my + mm_to_px(105), mx + mm_to_px(200), my + mm_to_px(112)),
        radius=mm_to_px(4), fill="#1d4ed8",
    )

    hy = my + mm_to_px(150)
    draw.text((mx, hy), HEADLINE, font=cn_font(True, 58), fill="#0f1b2d")
    draw.text((mx, hy + mm_to_px(95)), SUBHEAD, font=cn_font(False, 24), fill="#57657a")

    cy = hy + mm_to_px(175)
    for title, sub in PRODUCTS:
        draw.rounded_rectangle(
            (mx, cy, mx + mm_to_px(10), cy + mm_to_px(52)),
            radius=mm_to_px(3), fill="#1d4ed8",
        )
        draw.text((mx + mm_to_px(24), cy), title, font=cn_font(True, 24), fill="#122033")
        draw.text((mx + mm_to_px(24), cy + mm_to_px(36)), sub, font=cn_font(False, 16), fill="#57657a")
        cy += mm_to_px(72)

    cy += mm_to_px(20)
    for adv in ADVANTAGES:
        draw.text((mx, cy), f"✓  {adv}", font=cn_font(False, 22), fill="#1d4ed8")
        cy += mm_to_px(42)

    draw_footer(canvas, dark=False, accent="#1d4ed8")
    return save_poster(canvas, "store-wall-poster-style01-minimal.jpg")


# ── Style 2: 深色科技 ──────────────────────────────────────────
def render_style02_dark_tech() -> Path:
    width, height = mm_to_px(WIDTH_MM), mm_to_px(HEIGHT_MM)
    canvas = Image.new("RGB", (width, height), "#0a1020")
    with open_photo(2) as photo:
        canvas.paste(cover_resize(photo, width, height), (0, 0))
    apply_scrim(canvas, left_strength=230, bottom_strength=200, overall=50)

    draw = ImageDraw.Draw(canvas)
    mx, my = mm_to_px(100), mm_to_px(80)
    draw_brand(draw, mx, my, light=True)

    for i in range(3):
        y = my + mm_to_px(120 + i * 18)
        draw.line([(mx, y), (mx + mm_to_px(60 + i * 40), y)], fill="#7cc9ff", width=mm_to_px(2))

    hy = my + mm_to_px(200)
    draw.text((mx, hy), HEADLINE, font=cn_font(True, 68), fill="#ffffff")
    draw.text((mx, hy + mm_to_px(105)), SUBHEAD, font=cn_font(False, 28), fill="#b7c7dd")

    cy = hy + mm_to_px(190)
    cw, ch, gap = mm_to_px(360), mm_to_px(120), mm_to_px(24)
    for idx, (title, sub) in enumerate(PRODUCTS):
        col, row = idx % 3, idx // 3
        if idx >= 3:
            col, row = idx - 3, 1
        x0 = mx + col * (cw + gap)
        y0 = cy + row * (ch + gap)
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle(
            (x0, y0, x0 + cw, y0 + ch), radius=mm_to_px(10),
            fill=(29, 78, 216, 60), outline=(124, 201, 255, 180), width=mm_to_px(1.5),
        )
        canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB"), (0, 0))
        draw = ImageDraw.Draw(canvas)
        draw.text((x0 + mm_to_px(20), y0 + mm_to_px(20)), title, font=cn_font(True, 26), fill="#ffffff")
        draw.text((x0 + mm_to_px(20), y0 + mm_to_px(62)), sub, font=cn_font(False, 17), fill="#b7c7dd")

    ay = cy + 2 * (ch + gap) + mm_to_px(30)
    for adv in ADVANTAGES:
        aw = draw.textlength(adv, font=cn_font(False, 24)) + mm_to_px(40)
        draw.rounded_rectangle(
            (mx, ay, mx + aw, ay + mm_to_px(50)), radius=mm_to_px(25),
            outline="#7cc9ff", width=mm_to_px(1.5),
        )
        draw.text((mx + mm_to_px(20), ay + mm_to_px(10)), adv, font=cn_font(False, 24), fill="#7cc9ff")
        mx += aw + mm_to_px(16)
        if mx > mm_to_px(1200):
            mx, ay = mm_to_px(100), ay + mm_to_px(62)

    draw_footer(canvas, dark=True, accent="#7cc9ff")
    return save_poster(canvas, "store-wall-poster-style02-dark-tech.jpg")


def open_photo_rel(rel: str) -> Image.Image:
    rel_path = rel.replace("/", "\\")
    path = SUPPLIER_IMAGES / rel_path
    if not path.exists():
        return Image.new("RGB", (1920, 1080), (30, 40, 60))
    with Image.open(path) as img:
        return img.convert("RGB")


def draw_text_stroke(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill: str,
    stroke_fill: str = "#000000",
    stroke_width: int = 2,
) -> None:
    draw.text(xy, text, font=font, fill=fill, stroke_width=stroke_width, stroke_fill=stroke_fill)


def paste_industrial_photos(
    canvas: Image.Image,
    scene_rel: str,
    product_rel: str,
    *,
    scene_label: str = "应用场景",
    product_label: str = "产品系列",
) -> None:
    """Right panel: top = representative scene, bottom = product collection."""
    width, height = canvas.size
    photo_w = int(width * 0.64)
    photo_x = width - photo_w
    footer_h = mm_to_px(140)
    gap = mm_to_px(10)
    usable_h = height - footer_h
    scene_h = int(usable_h * 0.58)
    product_h = usable_h - scene_h - gap

    scene = open_photo_rel(scene_rel)
    canvas.paste(cover_resize(scene, photo_w, scene_h), (photo_x, 0))
    product = open_photo_rel(product_rel)
    canvas.paste(cover_resize(product, photo_w, product_h), (photo_x, scene_h + gap))

    draw = ImageDraw.Draw(canvas)
    label_font = cn_font(True, 22)
    draw.rectangle((photo_x, 0, photo_x + mm_to_px(180), mm_to_px(52)), fill="#f59e0b")
    draw.text((photo_x + mm_to_px(16), mm_to_px(8)), scene_label, font=label_font, fill="#1a1a1a")
    draw.rectangle(
        (photo_x, scene_h + gap, photo_x + mm_to_px(180), scene_h + gap + mm_to_px(52)),
        fill="#f59e0b",
    )
    draw.text((photo_x + mm_to_px(16), scene_h + gap + mm_to_px(8)), product_label, font=label_font, fill="#1a1a1a")
    draw.line([(photo_x, scene_h), (photo_x + photo_w, scene_h)], fill="#f59e0b", width=mm_to_px(4))


def draw_industrial_left_panel(canvas: Image.Image) -> None:
    width, height = canvas.size
    apply_scrim(canvas, left_strength=160, overall=15, color=(20, 20, 20))
    stripe_pts = [
        (0, 0),
        (int(width * 0.38), 0),
        (int(width * 0.32), height - mm_to_px(140)),
        (0, height - mm_to_px(140)),
    ]
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).polygon(stripe_pts, fill=(18, 18, 18, 252))
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB"), (0, 0))


def draw_industrial_content(
    canvas: Image.Image,
    *,
    headline: str = HEADLINE,
    subhead: str = SUBHEAD,
    products: list[tuple[str, str]] | None = None,
    advantages: list[str] | None = None,
    hook: str | None = None,
) -> None:
    """Left-side typography — wall-distance readable."""
    product_rows = products or PRODUCTS
    advantage_rows = advantages or ADVANTAGES
    draw = ImageDraw.Draw(canvas)
    mx, my = mm_to_px(80), mm_to_px(70)

    bar_h = mm_to_px(120)
    draw.rectangle((mx - mm_to_px(16), my, mx + mm_to_px(18), my + bar_h), fill="#f59e0b")

    logo_font = en_font(True, 125)
    draw_text_stroke(draw, (mx + mm_to_px(32), my), "Powerlink", logo_font, "#ffffff", stroke_width=4)
    pw = draw.textlength("Powerlink", font=logo_font)
    draw_text_stroke(
        draw, (mx + mm_to_px(32) + pw + mm_to_px(12), my), "energy", logo_font, "#fbbf24", stroke_width=4,
    )

    hy = my + mm_to_px(165)
    headline_font = cn_font(True, 98)
    draw_text_stroke(draw, (mx, hy), headline, headline_font, "#ffffff", stroke_width=5)

    bar_y = hy + mm_to_px(125)
    draw.rectangle((mx, bar_y, mx + mm_to_px(460), bar_y + mm_to_px(16)), fill="#f59e0b")

    sub_font = cn_font(False, 40)
    draw_text_stroke(draw, (mx, bar_y + mm_to_px(40)), subhead, sub_font, "#f9fafb", stroke_width=3)

    if hook:
        hook_font = cn_font(True, 52)
        draw_text_stroke(
            draw,
            (mx, bar_y + mm_to_px(105)),
            hook,
            hook_font,
            "#fbbf24",
            stroke_width=4,
        )
        cy = bar_y + mm_to_px(190)
    else:
        cy = bar_y + mm_to_px(120)

    title_font = cn_font(True, 44)
    sub_font_sm = cn_font(False, 28)
    for title, sub in product_rows:
        draw.rectangle((mx, cy, mx + mm_to_px(12), cy + mm_to_px(76)), fill="#f59e0b")
        draw_text_stroke(draw, (mx + mm_to_px(32), cy), title, title_font, "#ffffff", stroke_width=3)
        draw.text((mx + mm_to_px(32), cy + mm_to_px(58)), sub, font=sub_font_sm, fill="#e5e7eb")
        cy += mm_to_px(98)

    cy += mm_to_px(12)
    adv_font = cn_font(True, 34)
    for adv in advantage_rows:
        draw_text_stroke(draw, (mx, cy), f"▸  {adv}", adv_font, "#fbbf24", stroke_width=3)
        cy += mm_to_px(52)


def draw_industrial_footer(canvas: Image.Image) -> None:
    width, height = canvas.size
    footer_h = mm_to_px(140)
    fy = height - footer_h
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, fy, width, height), fill="#f59e0b")
    mx = mm_to_px(90)
    draw.text((mx, fy + mm_to_px(24)), WEBSITE, font=cn_font(True, 42), fill="#1a1a1a")
    draw.text(
        (mx, fy + mm_to_px(76)),
        f"{WHATSAPP}  |  {EMAIL}",
        font=cn_font(False, 30),
        fill="#292524",
    )


def render_industrial_variant(
    filename: str,
    scene_rel: str,
    product_rel: str,
    *,
    width_mm: float = WIDTH_MM,
    height_mm: float = HEIGHT_MM,
    headline: str = HEADLINE,
    subhead: str = SUBHEAD,
    products: list[tuple[str, str]] | None = None,
    advantages: list[str] | None = None,
    hook: str | None = None,
    scene_label: str = "应用场景",
    product_label: str = "产品系列",
) -> Path:
    width, height = mm_to_px(width_mm), mm_to_px(height_mm)
    canvas = Image.new("RGB", (width, height), "#1a1a1a")
    paste_industrial_photos(
        canvas,
        scene_rel,
        product_rel,
        scene_label=scene_label,
        product_label=product_label,
    )
    draw_industrial_left_panel(canvas)
    draw_industrial_content(
        canvas,
        headline=headline,
        subhead=subhead,
        products=products,
        advantages=advantages,
        hook=hook,
    )
    draw_industrial_footer(canvas)
    return save_poster(canvas, filename)


# 工业硬朗 · 场景图 + 产品集合图（素材来自供应商官网深度抓取）
STORE_SCENARIO_POSTERS = [
    {
        "filename": "store-wall-poster-scenario01-data-center.jpg",
        "scene_rel": "深圳科士达科技股份有限公司/other/011-optimized.jpg",
        "product_rel": "易事特集团股份有限公司/products/011-optimized.jpg",
        "label": "数据中心备电",
        "scene_label": "应用场景 · 数据中心",
        "product_label": "核心产品 · UPS备电",
        "headline": "数据中心 · 关键备电不断档",
        "subhead": "机房 · 机柜 · IDC · 边缘节点",
        "hook": "停电不断 · 稳定运行",
        "products": [
            ("在线 UPS 系统", "机架式 / 塔式 · 高可靠备电"),
            ("锂电池备电系统", "扩容灵活 · 续航可配"),
            ("监控与工业线缆", "配电 · 传感 · 现场集成"),
        ],
        "advantages": ["现场看样选型", "灵活起订量", "一站式集成", "快速响应支持"],
    },
    {
        "filename": "store-wall-poster-scenario02-energy-storage.jpg",
        "scene_rel": "易事特集团股份有限公司/products/012-optimized.jpg",
        "product_rel": "易事特集团股份有限公司/products/002-optimized.jpg",
        "label": "工商业储能",
        "scene_label": "应用场景 · 工商业储能",
        "product_label": "核心产品 · 储能系统",
        "headline": "工商业储能 · 削峰填谷降本",
        "subhead": "备用电源 · 峰谷套利 · 能源管理",
        "hook": "降本增效 · 稳定供电",
        "products": [
            ("工商业储能系统", "机柜级 · 峰谷套利 · 备电"),
            ("光储混合逆变器", "光伏接入 · 自发自用"),
            ("电池与监控配件", "BMS · 配电 · 安全监控"),
        ],
        "advantages": ["方案快速匹配", "灵活起订量", "整包集成供货", "项目现场支持"],
    },
    {
        "filename": "store-wall-poster-scenario03-telecom-solar.jpg",
        "scene_rel": "深圳科士达科技股份有限公司/other/014-optimized.jpg",
        "product_rel": "易事特集团股份有限公司/products/013-optimized.jpg",
        "label": "通信与户用光储",
        "scene_label": "应用场景 · 通信 / 光储",
        "product_label": "核心产品 · 通信电源",
        "headline": "通信站点 · 户用光储全覆盖",
        "subhead": "基站备电 · 混合逆变 · 家庭储能",
        "hook": "全场景备电 · 即选即用",
        "products": [
            ("通信直流电源", "整流系统 · 基站备电"),
            ("户用光储逆变器", "混合逆变 · 家庭备电"),
            ("UPS 与电池系统", "分布式站点 · 稳定输出"),
        ],
        "advantages": ["品类一站配齐", "小批量可订", "快速报价响应", "全球项目支持"],
    },
]


def render_store_scenario_posters() -> list[Path]:
    outputs: list[Path] = []
    print(
        f"Generating 3 store scenario posters "
        f"({STORE_WIDTH_MM}mm x {STORE_HEIGHT_MM}mm @ {DPI} DPI)\n"
    )
    for cfg in STORE_SCENARIO_POSTERS:
        output = render_industrial_variant(
            cfg["filename"],
            cfg["scene_rel"],
            cfg["product_rel"],
            width_mm=STORE_WIDTH_MM,
            height_mm=STORE_HEIGHT_MM,
            headline=cfg["headline"],
            subhead=cfg["subhead"],
            products=cfg["products"],
            advantages=cfg["advantages"],
            hook=cfg["hook"],
            scene_label=cfg["scene_label"],
            product_label=cfg["product_label"],
        )
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"  [{cfg['label']}] {output.name} ({size_mb:.1f} MB)")
        outputs.append(output)
    return outputs


INDUSTRIAL_VARIANTS = [
    (
        "store-wall-poster-industrial-v01.jpg",
        "易事特集团股份有限公司/products/012-optimized.jpg",
        "poster_assets/深圳索瑞德电子有限公司/product_collections/032-optimized.jpg",
        "储能电站场景 + 索瑞德工商业产品系列",
    ),
    (
        "store-wall-poster-industrial-v02.jpg",
        "深圳科士达科技股份有限公司/other/011-optimized.jpg",
        "poster_assets/深圳索瑞德电子有限公司/product_collections/033-optimized.jpg",
        "数据中心场景 + 索瑞德产品系列",
    ),
    (
        "store-wall-poster-industrial-v03.jpg",
        "poster_assets/深圳索瑞德电子有限公司/product_collections/060-optimized.jpg",
        "poster_assets/易事特集团股份有限公司/product_collections/001-optimized.jpg",
        "光储充电场景 + 易事特产品矩阵",
    ),
    (
        "store-wall-poster-industrial-v04.jpg",
        "深圳科士达科技股份有限公司/other/014-optimized.jpg",
        "poster_assets/深圳索瑞德电子有限公司/product_collections/034-optimized.jpg",
        "光伏电站场景 + 索瑞德储能逆变系列",
    ),
    (
        "store-wall-poster-industrial-v05.jpg",
        "poster_assets/易事特集团股份有限公司/scenes/004-optimized.jpg",
        "poster_assets/深圳索瑞德电子有限公司/product_collections/035-optimized.jpg",
        "光储充电站场景 + 索瑞德电源产品系列",
    ),
]


def render_all_industrial_variants() -> list[Path]:
    outputs: list[Path] = []
    print(f"Generating 5 industrial variants ({WIDTH_MM}mm x {HEIGHT_MM}mm @ {DPI} DPI)\n")
    for filename, scene, product, label in INDUSTRIAL_VARIANTS:
        output = render_industrial_variant(filename, scene, product)
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"  [{label}] {output.name} ({size_mb:.1f} MB)")
        outputs.append(output)
    return outputs


def render_style03_industrial() -> Path:
    return render_industrial_variant(
        "store-wall-poster-style03-industrial.jpg",
        "易事特集团股份有限公司/products/012-optimized.jpg",
        "poster_assets/深圳索瑞德电子有限公司/product_collections/032-optimized.jpg",
    )


# ── Style 4: 电影大片 ──────────────────────────────────────────
def render_style04_cinematic() -> Path:
    width, height = mm_to_px(WIDTH_MM), mm_to_px(HEIGHT_MM)
    canvas = Image.new("RGB", (width, height), "#000000")
    with open_photo(0) as photo:
        canvas.paste(cover_resize(photo, width, height), (0, 0))
    apply_scrim(canvas, left_strength=240, bottom_strength=220, overall=40)

    draw = ImageDraw.Draw(canvas)
    bar_w = mm_to_px(14)
    draw.rectangle((0, 0, bar_w, height), fill="#1d4ed8")

    mx = mm_to_px(120)
    my = int(height * 0.12)
    draw_brand(draw, mx, my, light=True)

    hy = my + mm_to_px(180)
    hf = cn_font(True, 82)
    draw.text((mx, hy), HEADLINE, font=hf, fill="#ffffff")

    sy = hy + mm_to_px(130)
    draw.text((mx, sy), SUBHEAD, font=cn_font(False, 30), fill="#e8f0fb")

    cy = sy + mm_to_px(120)
    for i, (title, sub) in enumerate(PRODUCTS):
        num = f"{i + 1:02d}"
        draw.text((mx, cy), num, font=en_font(True, 36), fill="#7cc9ff")
        draw.text((mx + mm_to_px(70), cy), title, font=cn_font(True, 30), fill="#ffffff")
        draw.text((mx + mm_to_px(70), cy + mm_to_px(44)), sub, font=cn_font(False, 18), fill="#b7c7dd")
        draw.line([(mx, cy + mm_to_px(78)), (mx + mm_to_px(500), cy + mm_to_px(78))], fill=(124, 201, 255, 80), width=1)
        cy += mm_to_px(95)

    draw.text((mx, cy + mm_to_px(20)), "  ·  ".join(ADVANTAGES), font=cn_font(False, 24), fill="#7cc9ff")

    footer_h = mm_to_px(130)
    fy = height - footer_h
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).rectangle((0, fy, width, height), fill=(15, 27, 45, 200))
    canvas.paste(Image.alpha_composite(canvas.convert("RGBA"), layer).convert("RGB"), (0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.text((mx, fy + mm_to_px(30)), WEBSITE, font=cn_font(True, 32), fill="#ffffff")
    draw.text((mx + mm_to_px(900), fy + mm_to_px(30)), WHATSAPP, font=cn_font(False, 22), fill="#b7c7dd")
    draw.text((mx + mm_to_px(900), fy + mm_to_px(68)), EMAIL, font=cn_font(False, 22), fill="#b7c7dd")

    return save_poster(canvas, "store-wall-poster-style04-cinematic.jpg")


# ── Style 5: 杂志拼贴 ──────────────────────────────────────────
def render_style05_magazine() -> Path:
    width, height = mm_to_px(WIDTH_MM), mm_to_px(HEIGHT_MM)
    canvas = Image.new("RGB", (width, height), "#eef4fb")
    draw = ImageDraw.Draw(canvas)

    left_w = int(width * 0.36)
    draw.rectangle((0, 0, left_w, height - mm_to_px(150)), fill="#ffffff")

    gap = mm_to_px(8)
    main_x = left_w + gap
    main_w = width - main_x - gap
    main_h = int(height * 0.62)
    with open_photo(0) as p:
        canvas.paste(cover_resize(p, main_w, main_h), (main_x, gap))

    bot_y = main_h + gap * 2
    bot_h = height - bot_y - mm_to_px(150) - gap
    half_w = (main_w - gap) // 2
    with open_photo(4) as p:
        canvas.paste(cover_resize(p, half_w, bot_h), (main_x, bot_y))
    with open_photo(2) as p:
        canvas.paste(cover_resize(p, half_w, bot_h), (main_x + half_w + gap, bot_y))

    draw = ImageDraw.Draw(canvas)
    draw.line([(left_w, 0), (left_w, height - mm_to_px(150))], fill="#1d4ed8", width=mm_to_px(3))
    draw.line([(main_x, main_h + gap), (width - gap, main_h + gap)], fill="#ffffff", width=mm_to_px(4))

    mx, my = mm_to_px(60), mm_to_px(60)
    draw_brand(draw, mx, my, light=False)
    draw.text((mx, my + mm_to_px(120)), "POWER\nSOLUTIONS", font=en_font(True, 32), fill="#1d4ed8")

    hy = my + mm_to_px(220)
    draw.text((mx, hy), HEADLINE, font=cn_font(True, 48), fill="#0f1b2d")
    draw.line([(mx, hy + mm_to_px(105)), (left_w - mm_to_px(40), hy + mm_to_px(105))], fill="#d5e0ef", width=mm_to_px(2))
    draw.text((mx, hy + mm_to_px(120)), SUBHEAD, font=cn_font(False, 18), fill="#57657a")

    cy = hy + mm_to_px(190)
    for i, (title, sub) in enumerate(PRODUCTS):
        num = f"{i + 1:02d}"
        draw.text((mx, cy), num, font=en_font(True, 28), fill="#1d4ed8")
        draw.text((mx + mm_to_px(55), cy), title, font=cn_font(True, 22), fill="#122033")
        draw.text((mx + mm_to_px(55), cy + mm_to_px(34)), sub, font=cn_font(False, 14), fill="#57657a")
        cy += mm_to_px(68)

    cy += mm_to_px(10)
    for adv in ADVANTAGES:
        pill_w = draw.textlength(adv, font=cn_font(False, 18)) + mm_to_px(30)
        draw.rounded_rectangle(
            (mx, cy, mx + pill_w, cy + mm_to_px(38)), radius=mm_to_px(19),
            fill="#e8f0fb", outline="#1d4ed8", width=1,
        )
        draw.text((mx + mm_to_px(15), cy + mm_to_px(7)), adv, font=cn_font(False, 18), fill="#1d4ed8")
        mx += pill_w + mm_to_px(10)
        if mx > left_w - mm_to_px(120):
            mx, cy = mm_to_px(60), cy + mm_to_px(48)

    draw_footer(canvas, dark=False, accent="#1d4ed8")
    return save_poster(canvas, "store-wall-poster-style05-magazine.jpg")


STYLES = [
    ("01-企业极简", render_style01_minimal),
    ("02-深色科技", render_style02_dark_tech),
    ("03-工业硬朗", render_style03_industrial),
    ("04-电影大片", render_style04_cinematic),
    ("05-杂志拼贴", render_style05_magazine),
]


def main() -> None:
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "industrial":
        render_all_industrial_variants()
        print(f"\nPreviews saved in {OUTPUT_DIR}")
        return

    if len(sys.argv) > 1 and sys.argv[1] == "store3":
        render_store_scenario_posters()
        print(f"\nPreviews saved in {OUTPUT_DIR}")
        return

    print(f"Generating 5 poster styles ({WIDTH_MM}mm x {HEIGHT_MM}mm @ {DPI} DPI)\n")
    for label, render_fn in STYLES:
        output = render_fn()
        size_mb = output.stat().st_size / (1024 * 1024)
        print(f"  [{label}] {output.name} ({size_mb:.1f} MB)")
    print(f"\nPreviews saved alongside each poster in {OUTPUT_DIR}")
    print("Tip: run with 'industrial' to generate 5 industrial-style variants only.")


if __name__ == "__main__":
    main()
