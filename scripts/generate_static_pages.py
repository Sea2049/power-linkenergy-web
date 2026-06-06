from __future__ import annotations

from html import escape
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_URL = "https://www.power-linkenergy.com"

LOCALES = {
    "en": {"prefix": "", "htmlLang": "en", "hreflang": "en", "dir": "ltr"},
    "zh": {"prefix": "zh", "htmlLang": "zh-CN", "hreflang": "zh-Hans", "dir": "ltr"},
    "fr": {"prefix": "fr", "htmlLang": "fr", "hreflang": "fr", "dir": "ltr"},
    "ru": {"prefix": "ru", "htmlLang": "ru", "hreflang": "ru", "dir": "ltr"},
    "ar": {"prefix": "ar", "htmlLang": "ar", "hreflang": "ar", "dir": "rtl"},
}

LOCALE_LABELS = {
    "en": "EN",
    "zh": "中文",
    "fr": "FR",
    "ru": "RU",
    "ar": "العربية",
}

OG_LOCALE = {
    "en": "en_US",
    "zh": "zh_CN",
    "fr": "fr_FR",
    "ru": "ru_RU",
    "ar": "ar_SA",
}

PROCESS_SVG_ABOUT = [
    (
        '<svg viewBox="0 0 24 24" fill="none">'
        '<path d="M7 5.75H17A1.25 1.25 0 0 1 18.25 7V17A1.25 1.25 0 0 1 17 18.25H7A1.25 1.25 0 0 1 5.75 17V7A1.25 1.25 0 0 1 7 5.75Z" />'
        '<path d="M8.75 9H15.25" /><path d="M8.75 12H15.25" /><path d="M8.75 15H12.5" />'
        "</svg>"
    ),
    (
        '<svg viewBox="0 0 24 24" fill="none">'
        '<path d="M8 8H16" /><path d="M8 16H16" /><path d="M9.5 12H14.5" />'
        '<path d="M6.75 12L4.75 10V14L6.75 12Z" /><path d="M17.25 12L19.25 10V14L17.25 12Z" />'
        '<path d="M7 5.75H17A1.25 1.25 0 0 1 18.25 7V17A1.25 1.25 0 0 1 17 18.25H7A1.25 1.25 0 0 1 5.75 17V7A1.25 1.25 0 0 1 7 5.75Z" />'
        "</svg>"
    ),
    (
        '<svg viewBox="0 0 24 24" fill="none">'
        '<path d="M7 7.25H17A1.25 1.25 0 0 1 18.25 8.5V15.5A1.25 1.25 0 0 1 17 16.75H7A1.25 1.25 0 0 1 5.75 15.5V8.5A1.25 1.25 0 0 1 7 7.25Z" />'
        '<path d="M7 9L12 12.75L17 9" /><path d="M8 18.25H16" />'
        "</svg>"
    ),
]

PROCESS_SVG_CONTACT = [
    PROCESS_SVG_ABOUT[0],
    PROCESS_SVG_ABOUT[2],
    (
        '<svg viewBox="0 0 24 24" fill="none">'
        '<path d="M12 5.75V12L16.25 14.5" />'
        '<path d="M12 18.25A6.25 6.25 0 1 0 12 5.75A6.25 6.25 0 0 0 12 18.25Z" />'
        "</svg>"
    ),
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8", newline="\n")


def load_locale(locale: str) -> dict:
    return json.loads(read(f"assets/locales/{locale}.json"))


def locale_url(locale: str, path: str) -> str:
    if not path.startswith("/"):
        path = "/" + path
    prefix = LOCALES[locale]["prefix"]
    if prefix:
        if path == "/":
            return f"/{prefix}/"
        return f"/{prefix}{path}"
    return path


def repo_path(locale: str, logical_path: str) -> str:
    prefix = LOCALES[locale]["prefix"]
    if logical_path == "/":
        return "index.html" if not prefix else f"{prefix}/index.html"
    stripped = logical_path.strip("/")
    if prefix:
        return f"{prefix}/{stripped}/index.html"
    return f"{stripped}/index.html"


def canonical(path: str) -> str:
    return f"{SITE_URL}{path}"


def html_attrs(locale: str) -> str:
    cfg = LOCALES[locale]
    attrs = f'lang="{escape(cfg["htmlLang"])}"'
    if cfg.get("dir"):
        attrs += f' dir="{escape(cfg["dir"])}"'
    return attrs


def absolute_asset(path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    return f"{SITE_URL}{path}"


def resolve_og_image(site: dict, item: dict | None = None) -> tuple[str, str, int, int]:
    page_image = None
    page_alt = None
    if item:
        page_image = item.get("heroImage") or item.get("image")
        page_alt = item.get("heroImageAlt") or item.get("imageAlt") or item.get("title")

    image_path = page_image or site.get("ogImage") or "/assets/images/og-share.jpg"
    image_alt = page_alt or site.get("ogImageAlt") or site.get("tagline", "Powerlink Energy")
    width = int(site.get("ogImageWidth", 1200))
    height = int(site.get("ogImageHeight", 630))
    return image_path, image_alt, width, height


def render_hreflang_alternates(logical_path: str) -> str:
    lines = []
    for loc, cfg in LOCALES.items():
        url = canonical(locale_url(loc, logical_path))
        lines.append(
            f'  <link rel="alternate" hreflang="{escape(cfg["hreflang"])}" href="{escape(url)}">'
        )
    default_url = canonical(locale_url("en", logical_path))
    lines.append(f'  <link rel="alternate" hreflang="x-default" href="{escape(default_url)}">')
    return "\n".join(lines) + "\n"


def render_json_ld_organization(locale: str, site: dict) -> str:
    org_url = canonical(locale_url(locale, "/"))
    payload = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Powerlink Energy",
        "url": org_url,
        "email": site["email"],
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "contactType": "customer support",
                "email": site["email"],
                "telephone": site["whatsapp"].replace(" ", ""),
            }
        ],
    }
    json_text = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return f'  <script type="application/ld+json">{json_text}</script>\n'


def render_social_meta(
    locale: str,
    path: str,
    title: str,
    description: str,
    image_path: str,
    image_alt: str,
    width: int,
    height: int,
) -> str:
    url = canonical(path)
    image_url = absolute_asset(image_path)
    return (
        '  <meta property="og:type" content="website">\n'
        '  <meta property="og:site_name" content="Powerlink Energy">\n'
        f'  <meta property="og:locale" content="{OG_LOCALE[locale]}">\n'
        + "".join(
            f'  <meta property="og:locale:alternate" content="{og_code}">\n'
            for alt_locale, og_code in OG_LOCALE.items()
            if alt_locale != locale
        )
        + f'  <meta property="og:title" content="{escape(title)}">\n'
        f'  <meta property="og:description" content="{escape(description)}">\n'
        f'  <meta property="og:url" content="{escape(url)}">\n'
        f'  <meta property="og:image" content="{escape(image_url)}">\n'
        f'  <meta property="og:image:alt" content="{escape(image_alt)}">\n'
        f'  <meta property="og:image:width" content="{width}">\n'
        f'  <meta property="og:image:height" content="{height}">\n'
        '  <meta name="twitter:card" content="summary_large_image">\n'
        f'  <meta name="twitter:title" content="{escape(title)}">\n'
        f'  <meta name="twitter:description" content="{escape(description)}">\n'
        f'  <meta name="twitter:image" content="{escape(image_url)}">\n'
        f'  <meta name="twitter:image:alt" content="{escape(image_alt)}">\n'
    )


def head(
    locale: str,
    logical_path: str,
    title: str,
    description: str,
    site: dict,
    item: dict | None = None,
) -> str:
    path = locale_url(locale, logical_path)
    url = canonical(path)
    image_path, image_alt, width, height = resolve_og_image(site, item)
    return (
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f"  <title>{escape(title)}</title>\n"
        f'  <meta name="description" content="{escape(description)}">\n'
        f'  <link rel="canonical" href="{escape(url)}">\n'
        + render_hreflang_alternates(logical_path)
        + render_social_meta(
            locale,
            path,
            title,
            description,
            image_path,
            image_alt,
            width,
            height,
        )
        + render_json_ld_organization(locale, site)
        + '  <link rel="icon" href="/favicon.ico" sizes="any">\n'
        '  <link rel="icon" type="image/png" sizes="32x32" href="/assets/images/favicon-32x32.png">\n'
        '  <link rel="icon" type="image/png" sizes="16x16" href="/assets/images/favicon-16x16.png">\n'
        '  <link rel="apple-touch-icon" sizes="180x180" href="/assets/images/apple-touch-icon.png">\n'
        '  <link rel="stylesheet" href="/assets/css/site.css">\n'
        "</head>"
    )


def render_skip_link(data: dict) -> str:
    label = data["ui"]["a11y"]["skipToMain"]
    return f'  <a class="skip-link" href="#main-content">{escape(label)}</a>\n'


def render_language_switcher(locale: str, logical_path: str) -> str:
    links = []
    for loc, cfg in LOCALES.items():
        href = locale_url(loc, logical_path)
        active = ' class="is-active"' if loc == locale else ""
        current = ' aria-current="true"' if loc == locale else ""
        links.append(
            f'<a href="{escape(href)}" hreflang="{escape(cfg["hreflang"])}" '
            f'lang="{escape(cfg["htmlLang"])}"{active}{current}>{escape(LOCALE_LABELS[loc])}</a>'
        )
    return '<div class="language-switcher">' + "".join(links) + "</div>"


def render_header(
    data: dict,
    locale: str,
    logical_path: str,
    switcher_path: str | None = None,
) -> str:
    ui = data["ui"]
    site = data["site"]
    language_path = switcher_path if switcher_path is not None else logical_path
    links = []
    for item in site["nav"]:
        href = locale_url(locale, item["href"])
        active = (item["href"] == "/" and logical_path == "/") or (
            item["href"] != "/" and logical_path.startswith(item["href"])
        )
        class_attr = ' class="is-active"' if active else ""
        current_attr = ' aria-current="page"' if active else ""
        links.append(
            f'<li><a href="{escape(href)}"{class_attr}{current_attr}>{escape(item["label"])}</a></li>'
        )

    return (
        '<header class="site-header">'
        '<div class="container site-header__inner">'
        f'<a class="brandmark" href="{escape(locale_url(locale, "/"))}">'
        '<span class="brandmark-power">Powerlink</span>'
        '<span class="brandmark-energy">energy</span></a>'
        f'<button class="nav-toggle" type="button" aria-expanded="false" '
        f'aria-controls="site-nav-menu" aria-label="{escape(ui["nav"]["toggleAria"])}">'
        f'{escape(ui["nav"]["menu"])}</button>'
        f'<nav class="site-nav" id="site-nav-menu" aria-label="{escape(ui["nav"]["primaryAria"])}"><ul>'
        + "".join(links)
        + "</ul></nav>"
        + render_language_switcher(locale, language_path)
        + "</div></header>"
    )


def render_footer(data: dict, locale: str) -> str:
    ui = data["ui"]
    site = data["site"]
    return (
        '<footer class="site-footer"><div class="container footer-grid"><div>'
        f'<p class="eyebrow">{escape(ui["footer"]["brand"])}</p>'
        f"<h2>{escape(site['tagline'])}</h2>"
        f"<p>{escape(ui['footer']['tagline'])}</p>"
        "</div><div>"
        f'<p class="eyebrow">{escape(ui["footer"]["directContact"])}</p>'
        f'<p><a href="mailto:{escape(site["email"])}">{escape(site["email"])}</a></p>'
        f'<p><a href="https://wa.me/8613534190063">{escape(site["whatsapp"])}</a></p>'
        f'<p><a href="https://{escape(site["domain"])}">{escape(site["domain"])}</a></p>'
        "</div></div></footer>"
    )


def render_visual_panel() -> str:
    return (
        '<div class="visual-panel" aria-hidden="true">'
        '<span class="rack"></span><span class="chip"></span><span class="line"></span>'
        "</div>"
    )


def render_hero_media(src: str, alt: str, modifier: str = "") -> str:
    class_name = "hero-media"
    if modifier:
        class_name += f" {modifier}"
    return (
        f'<div class="{escape(class_name)}">'
        + image_tag(src, alt, eager=True)
        + "</div>"
    )


def render_detail_visual(data: dict, item: dict, collection_name: str) -> str:
    ui = data["ui"]
    src = item.get("heroImage") or item.get("image")
    if src:
        alt = item.get("heroImageAlt") or item.get("imageAlt") or item["title"]
        return render_hero_media(src, alt, "hero-media--detail")
    if collection_name == "cases":
        note = item.get("galleryNote") or ui["cards"]["verifiedMediaFallback"]
        return (
            '<div class="visual-panel visual-panel--case case-empty-state">'
            f'<p class="eyebrow">{escape(ui["cards"]["verifiedProjectAssets"])}</p>'
            f"<h3>{escape(ui['cards']['projectVisualsLater'])}</h3>"
            f"<p>{escape(note)}</p></div>"
        )
    return render_visual_panel()


def render_noscript(data: dict) -> str:
    return (
        "<noscript>"
        f'<div class="noscript-banner">{escape(data["ui"]["noscript"])}</div>'
        "</noscript>"
    )


def section_head(eyebrow: str, title: str, body: str = "") -> str:
    body_html = f"<p>{escape(body)}</p>" if body else ""
    return (
        '<div class="section-head">'
        f'<p class="eyebrow">{escape(eyebrow)}</p>'
        f"<h2>{escape(title)}</h2>"
        f"{body_html}</div>"
    )


def image_tag(src: str, alt: str, eager: bool = False) -> str:
    attrs = ' loading="eager" fetchpriority="high" decoding="async"' if eager else ' loading="lazy" decoding="async"'
    return f'<img src="{escape(src)}" alt="{escape(alt)}"{attrs}>'


def render_solution_card(data: dict, locale: str, item: dict, action: str | None = None) -> str:
    ui = data["ui"]
    action_label = action or ui["buttons"]["learnMore"]
    media = '<div class="card-media card-media--placeholder" aria-hidden="true"></div>'
    if item.get("image"):
        media = (
            '<div class="card-media">'
            + image_tag(item["image"], item.get("imageAlt") or item["title"])
            + "</div>"
        )
    href = locale_url(locale, f'/solutions/{item["slug"]}/')
    return (
        '<article class="card card--solution">'
        + media
        + f'<div class="card-copy"><p class="eyebrow">{escape(ui["cards"]["solution"])}</p>'
        f"<h3>{escape(item['title'])}</h3>"
        f"<p>{escape(item['summary'])}</p>"
        f'<a class="route-link" href="{escape(href)}">{escape(action_label)}</a>'
        "</div></article>"
    )


def render_simple_card(
    data: dict,
    locale: str,
    kind: str,
    item: dict,
    logical_href: str,
    body: str,
) -> str:
    ui = data["ui"]
    media = ""
    if item.get("image"):
        media = (
            '<div class="card-media">'
            + image_tag(item["image"], item.get("imageAlt") or item["title"])
            + "</div>"
        )
    href = locale_url(locale, logical_href)
    return (
        '<article class="card">'
        + media
        + f'<p class="eyebrow">{escape(kind)}</p>'
        f"<h3>{escape(item['title'])}</h3>"
        f"<p>{escape(body)}</p>"
        f'<a class="route-link" href="{escape(href)}">{escape(ui["buttons"]["learnMore"])}</a>'
        "</article>"
    )


def render_case_card(data: dict, locale: str, item: dict) -> str:
    ui = data["ui"]
    note = item.get("galleryNote") or ui["cards"]["verifiedMediaFallback"]
    tag = item.get("projectStatus") or item.get("region", ui["collectionLabels"]["cases"])
    if item.get("heroImage"):
        media = (
            '<div class="card-media card-media--case">'
            + image_tag(item["heroImage"], item.get("heroImageAlt") or item["title"])
            + "</div>"
        )
    else:
        media = (
            '<div class="card-media card-media--case case-empty-state">'
            f'<p class="eyebrow">{escape(ui["cards"]["verifiedProjectAssets"])}</p>'
            f"<h3>{escape(ui['cards']['projectVisualsLater'])}</h3>"
            f"<p>{escape(note)}</p></div>"
        )
    href = locale_url(locale, f'/cases/{item["slug"]}/')
    return (
        '<article class="card case-framework-card">'
        + media
        + '<div class="case-framework-card__body"><div class="case-framework-card__head">'
        f'<p class="eyebrow">{escape(tag)}</p>'
        f'<span class="case-framework-card__tag">{escape(item["application"])}</span>'
        "</div>"
        f"<h3>{escape(item['title'])}</h3>"
        f"<p>{escape(item['summary'])}</p>"
        f'<a class="route-link" href="{escape(href)}">{escape(ui["buttons"]["viewDetails"])}</a>'
        "</div></article>"
    )


def render_detail_card(
    eyebrow: str,
    title: str,
    body: str = "",
    items: list[str] | None = None,
    section_id: str | None = None,
) -> str:
    items_html = ""
    if items:
        items_html = '<ul class="check-list detail-list">' + "".join(
            f"<li>{escape(item)}</li>" for item in items
        ) + "</ul>"
    body_html = f"<p>{escape(body)}</p>" if body else ""
    id_attr = f' id="{escape(section_id)}"' if section_id else ""
    return (
        f'<article class="card detail-info-card"{id_attr}>'
        '<div class="detail-info-card__head">'
        f'<p class="eyebrow">{escape(eyebrow)}</p>'
        f"<h2>{escape(title)}</h2>"
        f"</div>{body_html}{items_html}</article>"
    )


def build_detail_cards_from_specs(
    specs: list[tuple[str, str, str, str | None, list[str] | None]],
) -> tuple[str, list[tuple[str, str]]]:
    sections: list[tuple[str, str]] = []
    parts: list[str] = []
    for section_id, eyebrow, title, body, items in specs:
        sections.append((section_id, title))
        parts.append(
            render_detail_card(
                eyebrow,
                title,
                body or "",
                items,
                section_id=section_id,
            )
        )
    return "".join(parts), sections


def render_detail_breadcrumb(
    data: dict,
    locale: str,
    collection_name: str,
    page_title: str,
) -> str:
    ui = data["ui"]
    home_label = data["site"]["nav"][0]["label"]
    collection_label = ui["collectionLabels"][collection_name]
    home_href = locale_url(locale, "/")
    collection_href = locale_url(locale, f"/{collection_name}/")
    return (
        f'<nav class="detail-breadcrumb" aria-label="{escape(ui["a11y"]["breadcrumb"])}">'
        "<ol>"
        f'<li><a href="{escape(home_href)}">{escape(home_label)}</a></li>'
        f'<li><a href="{escape(collection_href)}">{escape(collection_label)}</a></li>'
        f'<li aria-current="page">{escape(page_title)}</li>'
        "</ol></nav>"
    )


def render_detail_toc(data: dict, sections: list[tuple[str, str]]) -> str:
    ui = data["ui"]
    items = "".join(
        f'<li><a href="#{escape(section_id)}">{escape(title)}</a></li>'
        for section_id, title in sections
    )
    return (
        f'<nav class="detail-toc" aria-label="{escape(ui["a11y"]["pageContents"])}">'
        f'<p class="detail-toc__label">{escape(ui["detail"]["tocTitle"])}</p>'
        f"<ol>{items}</ol></nav>"
    )


def render_detail_cta(data: dict, locale: str, collection_name: str) -> str:
    ui = data["ui"]
    site = data["site"]
    label = ui["collectionLabels"][collection_name]
    back_label = ui["buttons"]["backTo"].replace("{label}", label)
    return (
        f'<aside class="info-card detail-cta"><p class="eyebrow">{escape(ui["detail"]["ctaEyebrow"])}</p>'
        f"<h3>{escape(ui['detail']['ctaTitle'])}</h3>"
        f"<p>{escape(ui['detail']['ctaBody'])}</p>"
        '<div class="contact-strip">'
        f'<span>{escape(ui["labels"]["email"])} <a href="mailto:{escape(site["email"])}">{escape(site["email"])}</a></span>'
        f'<span>{escape(ui["labels"]["whatsapp"])} <a href="https://wa.me/8613534190063">{escape(site["whatsapp"])}</a></span>'
        f'<span>{escape(ui["labels"]["website"])} <a href="https://{escape(site["domain"])}">{escape(site["domain"])}</a></span>'
        "</div><div class=\"button-row\">"
        f'<a class="button button--primary" href="{escape(locale_url(locale, "/contact/"))}">{escape(ui["buttons"]["getQuote"])}</a>'
        f'<a class="button button--secondary" href="{escape(locale_url(locale, f"/{collection_name}/"))}">{escape(back_label)}</a>'
        "</div></aside>"
    )


def render_process_step(index: int, title: str, body: str, svg: str) -> str:
    return (
        '<div class="process-step">'
        '<div class="process-step__head">'
        f'<span class="process-step__index">{index}</span>'
        f'<span class="process-step__icon" aria-hidden="true">{svg}</span>'
        "</div>"
        f"<h3>{escape(title)}</h3>"
        f"<p>{escape(body)}</p>"
        "</div>"
    )


def render_promise_card(index: int, title: str, body: str, svg: str) -> str:
    return (
        '<div class="info-card promise-card">'
        '<div class="promise-card__head">'
        f'<span class="process-step__index">{index}</span>'
        f'<span class="process-step__icon" aria-hidden="true">{svg}</span>'
        "</div>"
        f"<h3>{escape(title)}</h3>"
        f"<p>{escape(body)}</p>"
        "</div>"
    )


def render_mailto_attrs(data: dict) -> str:
    mailto = data["ui"]["mailto"]
    fields_json = json.dumps(mailto["fields"], ensure_ascii=False, separators=(",", ":"))
    return (
        f'data-mailto-subject="{escape(mailto["subject"])}" '
        f'data-mailto-message-heading="{escape(mailto["messageHeading"])}" '
        f'data-mailto-fields="{escape(fields_json)}"'
    )


def not_found_head(locale: str, data: dict) -> str:
    not_found = data["ui"]["notFound"]
    return (
        "<head>\n"
        '  <meta charset="utf-8">\n'
        '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'  <title>{escape(not_found["pageTitle"])}</title>\n'
        f'  <meta name="description" content="{escape(not_found["pageDescription"])}">\n'
        '  <meta name="robots" content="noindex,follow">\n'
        '  <link rel="stylesheet" href="/assets/css/site.css">\n'
        "</head>"
    )


def build_not_found(data: dict, locale: str) -> str:
    ui = data["ui"]
    not_found = ui["notFound"]
    return (
        '    <section class="page-hero page-hero--404">\n'
        '      <div class="container not-found">\n'
        f'        <p class="eyebrow">{escape(not_found["eyebrow"])}</p>\n'
        f'        <h1>{escape(not_found["title"])}</h1>\n'
        f'        <p>{escape(not_found["body"])}</p>\n'
        '        <div class="button-row">\n'
        f'          <a class="button button--primary" href="{escape(locale_url(locale, "/"))}">{escape(not_found["primaryButton"])}</a>\n'
        f'          <a class="button button--ghost" href="{escape(locale_url(locale, "/solutions/"))}">{escape(not_found["solutionsButton"])}</a>\n'
        f'          <a class="button button--ghost" href="{escape(locale_url(locale, "/contact/"))}">{escape(not_found["contactButton"])}</a>\n'
        "        </div>\n"
        '        <div class="not-found__note">\n'
        f'          <p>{escape(not_found["note"])}</p>\n'
        "        </div>\n"
        "      </div>\n"
        "    </section>"
    )


def not_found_shell(locale: str, data: dict) -> str:
    return (
        "<!doctype html>\n"
        f"<html {html_attrs(locale)}>\n"
        f"{not_found_head(locale, data)}\n"
        f'<body data-locale="{escape(locale)}" data-page="not-found">\n'
        f"{render_skip_link(data)}"
        f'  <div data-site-header>{render_header(data, locale, "/404/", switcher_path="/")}</div>\n'
        f"  {render_noscript(data)}\n"
        '  <main id="main-content">\n'
        f"{build_not_found(data, locale)}\n"
        "  </main>\n"
        f'  <div data-site-footer>{render_footer(data, locale)}</div>\n'
        '  <script src="/assets/js/data.js"></script>\n'
        '  <script src="/assets/js/site.js"></script>\n'
        "</body>\n"
        "</html>\n"
    )


def repo_path_404(locale: str) -> str:
    prefix = LOCALES[locale]["prefix"]
    if prefix:
        return f"{prefix}/404.html"
    return "404.html"


def write_not_found_pages() -> None:
    for locale in LOCALES:
        data = load_locale(locale)
        write(repo_path_404(locale), not_found_shell(locale, data))


def page_shell(
    locale: str,
    logical_path: str,
    title: str,
    description: str,
    body_attrs: str,
    main_html: str,
    data: dict,
    item: dict | None = None,
) -> str:
    body_open = f'<body data-locale="{escape(locale)}" {body_attrs}>'
    return (
        "<!doctype html>\n"
        f"<html {html_attrs(locale)}>\n"
        f"{head(locale, logical_path, title, description, data['site'], item)}\n"
        f"{body_open}\n"
        f"{render_skip_link(data)}"
        f'  <div data-site-header>{render_header(data, locale, logical_path)}</div>\n'
        f"  {render_noscript(data)}\n"
        '  <main id="main-content">\n'
        f"{main_html}\n"
        "  </main>\n"
        f'  <div data-site-footer>{render_footer(data, locale)}</div>\n'
        '  <script src="/assets/js/data.js"></script>\n'
        '  <script src="/assets/js/site.js"></script>\n'
        "</body>\n"
        "</html>\n"
    )


def build_home(data: dict, locale: str) -> str:
    ui = data["ui"]
    home = data["home"]
    site = data["site"]
    metrics = [
        (len(data["solutions"]), ui["metrics"]["solutionScenarios"]),
        (len(data["products"]), ui["metrics"]["productCategories"]),
        (len(data["cases"]), ui["metrics"]["referenceFrameworks"]),
        (1, ui["metrics"]["integratedSupplyPath"]),
    ]
    metric_html = '<div class="metric-grid">' + "".join(
        f'<div class="metric"><strong>{count}</strong><span>{escape(label)}</span></div>'
        for count, label in metrics
    ) + "</div>"
    advantages = "".join(
        '<article class="info-card home-advantage-card">'
        '<div class="home-advantage-card__head">'
        f'<span class="process-step__index">{index}</span>'
        '<span class="process-step__icon" aria-hidden="true"></span>'
        "</div>"
        f"<h3>{escape(item['title'])}</h3>"
        f"<p>{escape(item['body'])}</p>"
        "</article>"
        for index, item in enumerate(home["advantages"], start=1)
    )
    return (
        '    <section class="hero">\n'
        '      <div class="container hero-grid">\n'
        '        <div class="hero-copy">\n'
        f'          <p class="eyebrow">{escape(ui["home"]["eyebrow"])}</p>\n'
        f"          <h1>{escape(home['heroTitle'])}</h1>\n"
        f"          <p>{escape(home['heroBody'])}</p>\n"
        '          <div class="button-row">'
        f'<a class="button button--primary" href="{escape(locale_url(locale, "/solutions/"))}">{escape(ui["buttons"]["exploreSolutions"])}</a>'
        f'<a class="button button--ghost" href="{escape(locale_url(locale, "/contact/"))}">{escape(ui["buttons"]["getQuote"])}</a></div>\n'
        f"          {metric_html}\n"
        "        </div>\n"
        + (
            f"        {render_hero_media(home['heroImage'], home.get('heroImageAlt') or home['heroTitle'])}\n"
            if home.get("heroImage")
            else f"        {render_visual_panel()}\n"
        )
        + "      </div>\n"
        "    </section>\n"
        '    <section class="section"><div class="container" id="home-applications">'
        + section_head(
            ui["home"]["applications"]["eyebrow"],
            ui["home"]["applications"]["title"],
            ui["home"]["applications"]["body"],
        )
        + '<ul class="badge-row">'
        + "".join(f'<li class="badge">{escape(item)}</li>' for item in home["applications"])
        + "</ul></div></section>\n"
        '    <section class="section section--alt"><div class="container" id="home-solutions">'
        + section_head(
            ui["home"]["solutions"]["eyebrow"],
            ui["home"]["solutions"]["title"],
            ui["home"]["solutions"]["body"],
        )
        + '<div class="stack-grid">'
        + "".join(
            render_solution_card(data, locale, item, ui["buttons"]["exploreSolution"])
            for item in data["solutions"]
        )
        + "</div></div></section>\n"
        '    <section class="section"><div class="container" id="home-products">'
        + section_head(
            ui["home"]["products"]["eyebrow"],
            ui["home"]["products"]["title"],
            ui["home"]["products"]["body"],
        )
        + '<div class="grid-3">'
        + "".join(
            render_simple_card(
                data,
                locale,
                ui["cards"]["product"],
                item,
                f'/products/{item["slug"]}/',
                item["summary"],
            )
            for item in data["products"]
        )
        + "</div></div></section>\n"
        '    <section class="section section--alt"><div class="container" id="home-cases">'
        + section_head(
            ui["home"]["cases"]["eyebrow"],
            ui["home"]["cases"]["title"],
            ui["home"]["cases"]["body"],
        )
        + '<div class="grid-3">'
        + "".join(render_case_card(data, locale, item) for item in data["cases"])
        + "</div></div></section>\n"
        '    <section class="section"><div class="container" id="home-contact"><div class="card">'
        + section_head(
            ui["home"]["advantages"]["eyebrow"],
            ui["home"]["advantages"]["title"],
        )
        + f'<div class="grid-2">{advantages}</div><div style="height:24px"></div>'
        + section_head(
            ui["home"]["contact"]["eyebrow"],
            ui["home"]["contact"]["title"],
            ui["home"]["contact"]["body"],
        )
        + '<div class="contact-strip">'
        f'<span>{escape(ui["labels"]["email"])} <a href="mailto:{escape(site["email"])}">{escape(site["email"])}</a></span>'
        f'<span>{escape(ui["labels"]["whatsapp"])} <a href="https://wa.me/8613534190063">{escape(site["whatsapp"])}</a></span>'
        f'<span>{escape(ui["labels"]["website"])} <a href="https://{escape(site["domain"])}">{escape(site["domain"])}</a></span>'
        "</div></div></div></section>"
    )


def build_overview(data: dict, locale: str, collection_name: str, title: str, description: str) -> str:
    ui = data["ui"]
    eyebrow = ui["collectionLabels"][collection_name]
    if collection_name == "solutions":
        cards = "".join(render_solution_card(data, locale, item) for item in data[collection_name])
    elif collection_name == "products":
        cards = "".join(
            render_simple_card(
                data,
                locale,
                ui["cards"]["product"],
                item,
                f'/products/{item["slug"]}/',
                item["summary"],
            )
            for item in data[collection_name]
        )
    else:
        cards = "".join(render_case_card(data, locale, item) for item in data[collection_name])

    if collection_name == "cases":
        hero_ui = ui["casesHero"]
        pills = "".join(f"<li>{escape(pill)}</li>" for pill in hero_ui["pills"])
        hero = (
            '    <section class="page-hero page-hero--cases"><div class="container" id="cases-hero">'
            '<div class="cases-hero"><div class="cases-hero__copy">'
            f'<p class="eyebrow">{escape(hero_ui["eyebrow"])}</p>'
            f"<h1>{escape(hero_ui['title'])}</h1>"
            f"<p>{escape(hero_ui['body'])}</p>"
            f'<ul class="pill-list">{pills}</ul>'
            "</div><aside class=\"cases-hero__panel info-card\">"
            f'<p class="eyebrow">{escape(hero_ui["panelEyebrow"])}</p>'
            f"<h3>{escape(hero_ui['panelTitle'])}</h3>"
            f"<p>{escape(hero_ui['panelBody'])}</p>"
            "</aside></div></div></section>\n"
        )
    else:
        hero = (
            '    <section class="page-hero"><div class="container">'
            f'<p class="eyebrow">{escape(eyebrow)}</p>'
            f"<h1>{escape(title)}</h1>"
            f"<p>{escape(description)}</p>"
            "</div></section>\n"
        )

    return hero + (
        f'    <section class="section"><div class="container" id="{escape(collection_name)}-list">'
        + section_head(eyebrow, title, description)
        + f'<div class="grid-3">{cards}</div></div></section>'
    )


def render_case_gallery(data: dict, item: dict) -> str:
    ui = data["ui"]
    gallery = item.get("gallery") or []
    if not gallery:
        return ""

    items = "".join(
        '<figure class="case-gallery__item">'
        + image_tag(entry["src"], entry.get("alt") or item["title"])
        + "</figure>"
        for entry in gallery
    )
    note = item.get("galleryNote") or ""
    note_html = f'<p class="case-gallery__note">{escape(note)}</p>' if note else ""
    return (
        '    <section class="section section--alt"><div class="container" id="case-gallery">'
        + section_head(
            ui["gallery"]["eyebrow"],
            ui["gallery"]["title"],
            ui["gallery"]["body"],
        )
        + f'<div class="case-gallery">{items}</div>{note_html}</div></section>\n'
    )


def build_detail(data: dict, locale: str, collection_name: str, item: dict) -> str:
    ui = data["ui"]
    detail = ui["detail"]
    subtitle = item.get("summary") or item.get("application") or ""
    if collection_name == "solutions":
        eyebrow = detail["solutionEyebrow"]
        pills = "".join(f"<li>{escape(pill)}</li>" for pill in detail["solutionPills"])
        hero_visual = render_detail_visual(data, item, collection_name)
        cards_ui = detail["solutionCards"]
        cards, toc_sections = build_detail_cards_from_specs(
            [
                (
                    "overview",
                    cards_ui["overviewEyebrow"],
                    cards_ui["overviewTitle"],
                    item["intro"],
                    None,
                ),
                (
                    "challenges",
                    cards_ui["challengesEyebrow"],
                    cards_ui["challengesTitle"],
                    None,
                    item["challenges"],
                ),
                (
                    "configuration",
                    cards_ui["configurationEyebrow"],
                    cards_ui["configurationTitle"],
                    None,
                    item["configuration"],
                ),
                (
                    "benefits",
                    cards_ui["benefitsEyebrow"],
                    cards_ui["benefitsTitle"],
                    None,
                    item["benefits"],
                ),
                (
                    "support",
                    cards_ui["supportEyebrow"],
                    cards_ui["supportTitle"],
                    item["support"],
                    None,
                ),
            ]
        )
    elif collection_name == "products":
        eyebrow = detail["productEyebrow"]
        pills = "".join(f"<li>{escape(pill)}</li>" for pill in detail["productPills"])
        hero_visual = render_detail_visual(data, item, collection_name)
        cards_ui = detail["productCards"]
        cards, toc_sections = build_detail_cards_from_specs(
            [
                (
                    "overview",
                    cards_ui["overviewEyebrow"],
                    cards_ui["overviewTitle"],
                    item["intro"],
                    None,
                ),
                (
                    "applications",
                    cards_ui["applicationsEyebrow"],
                    cards_ui["applicationsTitle"],
                    None,
                    item["applications"],
                ),
                (
                    "scope",
                    cards_ui["scopeEyebrow"],
                    cards_ui["scopeTitle"],
                    None,
                    item["includes"],
                ),
                (
                    "benefits",
                    cards_ui["benefitsEyebrow"],
                    cards_ui["benefitsTitle"],
                    None,
                    item["benefits"],
                ),
            ]
        )
    else:
        eyebrow = item.get("projectStatus") or item.get("region", ui["collectionLabels"]["cases"])
        pills = (
            f"<li>{escape(eyebrow)}</li>"
            f"<li>{escape(item['application'])}</li>"
        )
        hero_visual = render_detail_visual(data, item, collection_name)
        cards_ui = detail["caseCards"]
        cards, toc_sections = build_detail_cards_from_specs(
            [
                (
                    "overview",
                    cards_ui["overviewEyebrow"],
                    cards_ui["overviewTitle"],
                    item["overview"],
                    None,
                ),
                (
                    "need",
                    cards_ui["needEyebrow"],
                    cards_ui["needTitle"],
                    item["challenge"],
                    None,
                ),
                (
                    "design",
                    cards_ui["designEyebrow"],
                    cards_ui["designTitle"],
                    item["solutionDesign"],
                    None,
                ),
                (
                    "configuration",
                    cards_ui["configurationEyebrow"],
                    cards_ui["configurationTitle"],
                    None,
                    item["mainConfiguration"],
                ),
                (
                    "support",
                    cards_ui["supportEyebrow"],
                    cards_ui["supportTitle"],
                    item["deliverySupport"],
                    None,
                ),
                (
                    "outcome",
                    cards_ui["outcomeEyebrow"],
                    cards_ui["outcomeTitle"],
                    None,
                    item["results"],
                ),
            ]
        )

    breadcrumb = render_detail_breadcrumb(data, locale, collection_name, item["title"])
    toc = render_detail_toc(data, toc_sections)

    return (
        '    <section class="detail-hero-wrap"><div class="container" id="detail-hero"><div class="split-hero">'
        '<div class="detail-hero">'
        f'<p class="eyebrow">{escape(eyebrow)}</p>'
        f"<h1>{escape(item['title'])}</h1>"
        f"<p>{escape(subtitle)}</p>"
        f'<ul class="pill-list">{pills}</ul>'
        "</div>"
        f"{hero_visual}</div></div></section>\n"
        '    <section class="section"><div class="container">'
        f"{breadcrumb}\n"
        '      <div class="detail-layout" id="detail-body">\n'
        '        <div class="detail-main">\n'
        f"          {toc}\n"
        f'          <div class="detail-card-stack">{cards}</div>\n'
        "        </div>\n"
        f"        {render_detail_cta(data, locale, collection_name)}\n"
        "      </div></div></section>\n"
        + (render_case_gallery(data, item) if collection_name == "cases" else "")
    )


def build_about(data: dict, locale: str) -> str:
    about = data["about"]
    ui = data["ui"]
    hero = about["hero"]
    why = about["why"]
    what = about["whatWeDo"]
    choose = about["whyChooseUs"]
    work = about["howWeWork"]
    cta = about["cta"]

    trust_cards = "".join(
        '<article class="trust-card">'
        f'<p class="eyebrow">{escape(card["index"])}</p>'
        f"<h3>{escape(card['title'])}</h3>"
        f"<p>{escape(card['body'])}</p>"
        "</article>"
        for card in why["cards"]
    )

    categories = "".join(f"<li>{escape(item)}</li>" for item in what["categories"])

    contact_points = "".join(
        '<div class="contact-point">'
        f"<strong>{escape(point['label'])}</strong> {escape(point['value'])}"
        "</div>"
        for point in choose["points"]
    )

    process_steps = "".join(
        render_process_step(index, step["title"], step["body"], PROCESS_SVG_ABOUT[index - 1])
        for index, step in enumerate(work["steps"], start=1)
    )

    return (
        '    <section class="page-hero page-hero--visual">\n'
        '      <div class="container page-hero__grid">\n'
        '        <div class="page-hero__copy">\n'
        f'          <p class="eyebrow">{escape(hero["eyebrow"])}</p>\n'
        f"          <h1>{escape(hero['title'])}</h1>\n"
        f"          <p>{escape(hero['body'])}</p>\n"
        '          <div class="button-row">\n'
        f'            <a class="button button--primary" href="{escape(locale_url(locale, "/solutions/"))}">{escape(hero["primaryButton"])}</a>\n'
        f'            <a class="button button--ghost" href="{escape(locale_url(locale, "/contact/"))}">{escape(hero["secondaryButton"])}</a>\n'
        "          </div>\n"
        "        </div>\n"
        '        <div class="page-hero__visual page-hero__visual--illustrated">\n'
        f"          {render_hero_media(hero['image'], hero.get('imageAlt') or hero['title'])}\n"
        '          <div class="page-hero__overlay">\n'
        f'            <p class="eyebrow">{escape(hero["overlayEyebrow"])}</p>\n'
        f"            <h3>{escape(hero['overlayTitle'])}</h3>\n"
        f"            <p>{escape(hero['overlayBody'])}</p>\n"
        "          </div>\n"
        "        </div>\n"
        "      </div>\n"
        "    </section>\n"
        '    <section class="section">\n'
        '      <div class="container">\n'
        + section_head(why["eyebrow"], why["title"], why["body"])
        + f'        <div class="trust-grid">{trust_cards}</div>\n'
        "      </div>\n"
        "    </section>\n"
        '    <section class="section section--alt">\n'
        '      <div class="container">\n'
        '        <div class="content-split content-split--about">\n'
        '          <article class="card">\n'
        f'            <p class="eyebrow">{escape(what["eyebrow"])}</p>\n'
        f"            <h2>{escape(what['title'])}</h2>\n"
        f"            <p>{escape(what['body1'])}</p>\n"
        f"            <p>{escape(what['body2'])}</p>\n"
        f'            <ul class="check-list">{categories}</ul>\n'
        "          </article>\n"
        '          <article class="card">\n'
        f'            <p class="eyebrow">{escape(choose["eyebrow"])}</p>\n'
        f"            <h2>{escape(choose['title'])}</h2>\n"
        f"            <p>{escape(choose['body'])}</p>\n"
        f'            <div class="contact-points">{contact_points}</div>\n'
        "          </article>\n"
        '          <article class="card card--process">\n'
        f'            <p class="eyebrow">{escape(work["eyebrow"])}</p>\n'
        f"            <h2>{escape(work['title'])}</h2>\n"
        f"            <p>{escape(work['body'])}</p>\n"
        f'            <div class="process-strip">{process_steps}</div>\n'
        "          </article>\n"
        "        </div>\n"
        "      </div>\n"
        "    </section>\n"
        '    <section class="section">\n'
        '      <div class="container">\n'
        '        <div class="card cta-panel">\n'
        f'          <p class="eyebrow">{escape(cta["eyebrow"])}</p>\n'
        f"          <h2>{escape(cta['title'])}</h2>\n"
        f"          <p>{escape(cta['body'])}</p>\n"
        '          <div class="button-row">\n'
        f'            <a class="button button--primary" href="{escape(locale_url(locale, "/contact/"))}">{escape(cta["primaryButton"])}</a>\n'
        f'            <a class="button button--secondary" href="{escape(locale_url(locale, "/solutions/"))}">{escape(cta["secondaryButton"])}</a>\n'
        "          </div>\n"
        "        </div>\n"
        "      </div>\n"
        "    </section>"
    )


def build_contact(data: dict, locale: str) -> str:
    contact = data["contact"]
    site = data["site"]
    labels = contact["formLabels"]

    promise_cards = "".join(
        render_promise_card(index, step["title"], step["body"], PROCESS_SVG_CONTACT[index - 1])
        for index, step in enumerate(contact["promiseSteps"], start=1)
    )

    form_fields = (
        f'<label><span>{escape(labels["name"])}</span><input type="text" name="name" required></label>\n'
        f'              <label><span>{escape(labels["company"])}</span><input type="text" name="company"></label>\n'
        f'              <label><span>{escape(labels["country"])}</span><input type="text" name="country"></label>\n'
        f'              <label><span>{escape(labels["email"])}</span><input type="email" name="email" required></label>\n'
        f'              <label><span>{escape(labels["whatsapp"])}</span><input type="text" name="whatsapp"></label>\n'
        f'              <label><span>{escape(labels["application"])}</span><input type="text" name="application" required></label>\n'
        f'              <label><span>{escape(labels["productInterest"])}</span><input type="text" name="product-interest"></label>\n'
        f'              <label><span>{escape(labels["message"])}</span><textarea name="message" rows="6" required></textarea></label>\n'
    )

    return (
        '    <section class="page-hero page-hero--visual">\n'
        '      <div class="container page-hero__grid">\n'
        '        <div class="page-hero__copy">\n'
        f'          <p class="eyebrow">{escape(contact["eyebrow"])}</p>\n'
        f"          <h1>{escape(contact['title'])}</h1>\n"
        f"          <p>{escape(contact['heroBody'])}</p>\n"
        '          <div class="button-row">\n'
        f'            <a class="button button--primary" href="mailto:{escape(site["email"])}">{escape(contact["emailButton"])}</a>\n'
        f'            <a class="button button--ghost" href="https://wa.me/8613534190063">{escape(contact["whatsappButton"])}</a>\n'
        "          </div>\n"
        "        </div>\n"
        '        <div class="page-hero__visual page-hero__visual--illustrated">\n'
        f"          {render_hero_media(contact['heroImage'], contact.get('heroImageAlt') or contact['title'])}\n"
        '          <div class="page-hero__overlay">\n'
        f'            <p class="eyebrow">{escape(contact["overlayEyebrow"])}</p>\n'
        f"            <h3>{escape(contact['overlayTitle'])}</h3>\n"
        f"            <p>{escape(contact['overlayBody'])}</p>\n"
        "          </div>\n"
        "        </div>\n"
        "      </div>\n"
        "    </section>\n"
        '    <section class="section">\n'
        '      <div class="container">\n'
        '        <div class="contact-layout">\n'
        '          <div class="contact-panel">\n'
        '            <article class="contact-card">\n'
        f'              <p class="eyebrow">{escape(contact["directContactEyebrow"])}</p>\n'
        f"              <h2>{escape(contact['directContactTitle'])}</h2>\n"
        f"              <p>{escape(contact['directContactBody'])}</p>\n"
        '              <div class="contact-points">\n'
        '                <div class="contact-point">'
        f"<strong>{escape(contact['emailLabel'])}</strong><br>"
        f'<a href="mailto:{escape(site["email"])}">{escape(site["email"])}</a></div>\n'
        '                <div class="contact-point">'
        f"<strong>{escape(contact['whatsappLabel'])}</strong><br>"
        f'<a href="https://wa.me/8613534190063">{escape(site["whatsapp"])}</a></div>\n'
        '                <div class="contact-point">'
        f"<strong>{escape(contact['websiteLabel'])}</strong><br>{escape(site['domain'])}</div>\n"
        "              </div>\n"
        "            </article>\n"
        f'            <div class="response-promise">{promise_cards}</div>\n'
        "          </div>\n"
        "          <article class=\"card\">\n"
        f'            <p class="eyebrow">{escape(contact["formEyebrow"])}</p>\n'
        f"            <h2>{escape(contact['formTitle'])}</h2>\n"
        f"            <p>{escape(contact['formIntro'])}</p>\n"
        f'            <p class="form-note" data-form-mode>{escape(contact["formNote"])}</p>\n'
        '            <form class="inquiry-form" action="#" method="get">\n'
        f"              {form_fields}"
        f'              <button class="button button--primary" type="submit">{escape(contact["formSubmit"])}</button>\n'
        "            </form>\n"
        '            <p class="form-status" data-form-status aria-live="polite"></p>\n'
        "          </article>\n"
        "        </div>\n"
        "      </div>\n"
        "    </section>"
    )


def collect_logical_paths() -> list[str]:
    data = load_locale("en")
    paths = ["/", "/about/", "/contact/", "/solutions/", "/products/", "/cases/"]
    for collection_name in ("solutions", "products", "cases"):
        for item in data[collection_name]:
            paths.append(f"/{collection_name}/{item['slug']}/")
    return paths


def collect_sitemap_urls() -> list[str]:
    urls: list[str] = []
    for logical_path in collect_logical_paths():
        for locale in LOCALES:
            urls.append(locale_url(locale, logical_path))
    return urls


def write_sitemap() -> None:
    entries: list[str] = []
    for logical_path in collect_logical_paths():
        for locale in LOCALES:
            path = locale_url(locale, logical_path)
            alternates = "".join(
                "    "
                f'<xhtml:link rel="alternate" hreflang="{escape(LOCALES[alt_locale]["hreflang"])}" '
                f'href="{escape(canonical(locale_url(alt_locale, logical_path)))}" />\n'
                for alt_locale in LOCALES
            )
            default_href = escape(canonical(locale_url("en", logical_path)))
            entries.append(
                "  <url>\n"
                f"    <loc>{escape(canonical(path))}</loc>\n"
                f"{alternates}"
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{default_href}" />\n'
                "  </url>\n"
            )
    content = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "".join(entries)
        + "</urlset>\n"
    )
    write("sitemap.xml", content)


def sync_data_js(data: dict) -> None:
    payload = {key: value for key, value in data.items() if key not in ("about", "ui")}
    content = "window.__SITE_DATA__ = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
    write("assets/js/data.js", content)


def generate_locale_pages(locale: str, data: dict) -> None:
    ui = data["ui"]
    pages = ui["pages"]
    brand = ui["footer"]["brand"]

    write(
        repo_path(locale, "/"),
        page_shell(
            locale,
            "/",
            pages["home"]["title"],
            pages["home"]["description"],
            'data-page="home"',
            build_home(data, locale),
            data,
        ),
    )

    write(
        repo_path(locale, "/solutions/"),
        page_shell(
            locale,
            "/solutions/",
            pages["solutions"]["title"],
            pages["solutions"]["description"],
            'data-page="solutions-overview"',
            build_overview(
                data,
                locale,
                "solutions",
                pages["solutions"]["overviewTitle"],
                pages["solutions"]["overviewDescription"],
            ),
            data,
        ),
    )

    write(
        repo_path(locale, "/products/"),
        page_shell(
            locale,
            "/products/",
            pages["products"]["title"],
            pages["products"]["description"],
            'data-page="products-overview"',
            build_overview(
                data,
                locale,
                "products",
                pages["products"]["overviewTitle"],
                pages["products"]["overviewDescription"],
            ),
            data,
        ),
    )

    write(
        repo_path(locale, "/cases/"),
        page_shell(
            locale,
            "/cases/",
            pages["cases"]["title"],
            pages["cases"]["description"],
            'data-page="cases-overview"',
            build_overview(
                data,
                locale,
                "cases",
                pages["cases"]["overviewTitle"],
                pages["cases"]["overviewDescription"],
            ),
            data,
        ),
    )

    for collection_name in ("solutions", "products", "cases"):
        for item in data[collection_name]:
            logical_path = f"/{collection_name}/{item['slug']}/"
            write(
                repo_path(locale, logical_path),
                page_shell(
                    locale,
                    logical_path,
                    f"{item['title']} | {brand}",
                    item["summary"],
                    f'data-page="detail" data-collection="{collection_name}" data-slug="{item["slug"]}"',
                    build_detail(data, locale, collection_name, item),
                    data,
                    item,
                ),
            )

    write(
        repo_path(locale, "/about/"),
        page_shell(
            locale,
            "/about/",
            data["about"]["pageTitle"],
            data["about"]["pageDescription"],
            'data-page="about"',
            build_about(data, locale),
            data,
        ),
    )

    contact = data["contact"]
    form_note = escape(contact["formNote"])
    form_status = escape(contact.get("formStatusText", ""))
    mailto_attrs = render_mailto_attrs(data)
    write(
        repo_path(locale, "/contact/"),
        page_shell(
            locale,
            "/contact/",
            contact["pageTitle"],
            contact["pageDescription"],
            (
                'data-page="contact" '
                f'data-form-note="{form_note}" '
                f'data-form-status-text="{form_status}" '
                f"{mailto_attrs}"
            ),
            build_contact(data, locale),
            data,
        ),
    )


def main() -> None:
    en_data = load_locale("en")
    sync_data_js(en_data)

    for locale in LOCALES:
        data = load_locale(locale)
        generate_locale_pages(locale, data)

    write_not_found_pages()
    write_sitemap()


if __name__ == "__main__":
    main()
