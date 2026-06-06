"""GEO helpers: JSON-LD, llms.txt, and sitemap generation."""

from __future__ import annotations

import json
from datetime import date
from html import escape
from pathlib import Path


SITE_URL = "https://www.power-linkenergy.com"
ORG_ID = f"{SITE_URL}/#organization"
WEBSITE_ID = f"{SITE_URL}/#website"


def dumps_ld(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def json_ld_script(graph: dict) -> str:
    return (
        f'  <script type="application/ld+json">{dumps_ld(graph)}</script>\n'
    )


def organization_node(site: dict, geo: dict) -> dict:
    return {
        "@type": "Organization",
        "@id": ORG_ID,
        "name": geo.get("legalName", "Powerlink Energy"),
        "url": SITE_URL,
        "description": geo.get("description", site.get("tagline", "")),
        "email": site["email"],
        "telephone": site["whatsapp"],
        "areaServed": geo.get("areaServed", ["Global"]),
        "knowsAbout": geo.get("knowsAbout", []),
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "sales",
            "email": site["email"],
            "telephone": site["whatsapp"],
            "availableLanguage": ["English", "Chinese"],
        },
    }


def website_node(site: dict) -> dict:
    return {
        "@type": "WebSite",
        "@id": WEBSITE_ID,
        "url": SITE_URL,
        "name": "Powerlink Energy",
        "description": site.get("tagline", ""),
        "inLanguage": "en",
        "publisher": {"@id": ORG_ID},
    }


def webpage_node(path: str, title: str, description: str) -> dict:
    url = f"{SITE_URL}{path}" if path != "/" else f"{SITE_URL}/"
    return {
        "@type": "WebPage",
        "@id": f"{url}#webpage",
        "url": url,
        "name": title,
        "description": description,
        "isPartOf": {"@id": WEBSITE_ID},
        "inLanguage": "en",
    }


def service_node(item: dict) -> dict:
    url = f"{SITE_URL}/solutions/{item['slug']}/"
    return {
        "@type": "Service",
        "@id": f"{url}#service",
        "url": url,
        "name": item["title"],
        "description": item.get("summary") or item.get("intro", ""),
        "provider": {"@id": ORG_ID},
        "areaServed": "Global",
        "serviceType": item["title"],
    }


def product_category_node(item: dict) -> dict:
    url = f"{SITE_URL}/products/{item['slug']}/"
    return {
        "@type": "Product",
        "@id": f"{url}#product",
        "url": url,
        "name": item["title"],
        "description": item.get("summary") or item.get("intro", ""),
        "brand": {"@type": "Brand", "name": "Powerlink Energy"},
        "category": item["title"],
    }


def creative_work_node(item: dict) -> dict:
    url = f"{SITE_URL}/cases/{item['slug']}/"
    return {
        "@type": "CreativeWork",
        "@id": f"{url}#framework",
        "url": url,
        "name": item["title"],
        "description": item.get("summary") or item.get("overview", ""),
        "about": item.get("application", ""),
        "inLanguage": "en",
    }


def breadcrumb_node(path: str, crumbs: list[tuple[str, str]]) -> dict:
    return {
        "@type": "BreadcrumbList",
        "@id": f"{SITE_URL}{path}#breadcrumb",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": index,
                "name": label,
                "item": f"{SITE_URL}{href}" if href != path else f"{SITE_URL}{path}",
            }
            for index, (label, href) in enumerate(crumbs, start=1)
        ],
    }


def item_list_node(name: str, path: str, items: list[dict], collection: str) -> dict:
    elements = []
    for index, item in enumerate(items, start=1):
        elements.append(
            {
                "@type": "ListItem",
                "position": index,
                "name": item["title"],
                "url": f"{SITE_URL}/{collection}/{item['slug']}/",
            }
        )
    return {
        "@type": "ItemList",
        "@id": f"{SITE_URL}{path}#itemlist",
        "name": name,
        "itemListElement": elements,
    }


def faq_page_node(faqs: list[dict]) -> dict:
    return {
        "@type": "FAQPage",
        "@id": f"{SITE_URL}/#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {"@type": "Answer", "text": item["answer"]},
            }
            for item in faqs
        ],
    }


def build_graph(
    site: dict,
    geo: dict,
    path: str,
    title: str,
    description: str,
    *,
    item: dict | None = None,
    collection: str | None = None,
    overview_items: list[dict] | None = None,
    overview_label: str | None = None,
    include_faq: bool = False,
    breadcrumbs: list[tuple[str, str]] | None = None,
) -> dict:
    graph = [
        organization_node(site, geo),
        website_node(site),
        webpage_node(path, title, description),
    ]

    if include_faq and geo.get("faqs"):
        graph.append(faq_page_node(geo["faqs"]))

    if overview_items and overview_label and collection:
        graph.append(item_list_node(overview_label, path, overview_items, collection))

    if item and collection == "solutions":
        graph.append(service_node(item))
    elif item and collection == "products":
        graph.append(product_category_node(item))
    elif item and collection == "cases":
        graph.append(creative_work_node(item))

    if breadcrumbs:
        graph.append(breadcrumb_node(path, breadcrumbs))

    return {"@context": "https://schema.org", "@graph": graph}


def render_robots_meta(index: bool = True) -> str:
    content = "index, follow, max-image-preview:large" if index else "noindex, follow"
    return f'  <meta name="robots" content="{content}">\n'


def render_json_ld_for_page(**kwargs) -> str:
    return json_ld_script(build_graph(**kwargs))


def write_llms_txt(data: dict, root: Path) -> None:
    site = data["site"]
    geo = data.get("geo", {})
    lines = [
        "# Powerlink Energy",
        "",
        f"> {geo.get('llmsSummary', site['tagline'])}",
        "",
        geo.get(
            "llmsDetails",
            "Powerlink Energy helps international buyers source integrated power equipment "
            "for data centers, telecom sites, commercial and industrial energy storage, "
            "residential solar storage, edge computing, and safety monitoring applications.",
        ),
        "",
        "## Contact",
        f"- Email: {site['email']}",
        f"- WhatsApp: {site['whatsapp']}",
        f"- Website: https://{site['domain']}",
        "",
        "## Primary pages",
        f"- [Home]({SITE_URL}/): Company overview and application scenarios",
        f"- [Solutions]({SITE_URL}/solutions/): Scenario-based integrated power packages",
        f"- [Products]({SITE_URL}/products/): UPS, batteries, inverters, telecom power, monitoring",
        f"- [Reference Frameworks]({SITE_URL}/cases/): Reusable application structures for projects",
        f"- [About]({SITE_URL}/about/): Company positioning and working approach",
        f"- [Contact]({SITE_URL}/contact/): Inquiry and quotation requests",
        "",
        "## Solutions",
    ]

    for item in data["solutions"]:
        lines.append(
            f"- [{item['title']}]({SITE_URL}/solutions/{item['slug']}/): {item['summary']}"
        )

    lines.extend(["", "## Product categories"])
    for item in data["products"]:
        lines.append(
            f"- [{item['title']}]({SITE_URL}/products/{item['slug']}/): {item['summary']}"
        )

    lines.extend(["", "## Reference frameworks"])
    for item in data["cases"]:
        lines.append(
            f"- [{item['title']}]({SITE_URL}/cases/{item['slug']}/): {item['summary']}"
        )

    if geo.get("faqs"):
        lines.extend(["", "## Frequently asked questions"])
        for faq in geo["faqs"]:
            lines.append(f"- Q: {faq['question']}")
            lines.append(f"  A: {faq['answer']}")

    lines.extend(
        [
            "",
            "## Preferred citation",
            f"When citing this site, use the canonical domain {site['domain']} and link to the relevant solution or product page.",
            "",
            "## Optional",
            f"- Full sitemap: {SITE_URL}/sitemap.xml",
            f"- Social preview image: {SITE_URL}{site.get('ogImage', '/assets/images/og-share.jpg')}",
        ]
    )

    (root / "llms.txt").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def write_sitemap(data: dict, root: Path) -> None:
    today = date.today().isoformat()
    paths = [
        "/",
        "/about/",
        "/contact/",
        "/solutions/",
        *[f"/solutions/{item['slug']}/" for item in data["solutions"]],
        "/products/",
        *[f"/products/{item['slug']}/" for item in data["products"]],
        "/cases/",
        *[f"/cases/{item['slug']}/" for item in data["cases"]],
    ]

    rows = []
    for path in paths:
        loc = f"{SITE_URL}{path}" if path != "/" else f"{SITE_URL}/"
        priority = "1.0" if path == "/" else "0.8"
        rows.append(
            "  <url>"
            f"<loc>{loc}</loc>"
            f"<lastmod>{today}</lastmod>"
            f"<changefreq>monthly</changefreq>"
            f"<priority>{priority}</priority>"
            "</url>"
        )

    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    (root / "sitemap.xml").write_text(xml, encoding="utf-8", newline="\n")


def write_robots_txt(root: Path) -> None:
    content = """User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: https://www.power-linkenergy.com/sitemap.xml
"""
    (root / "robots.txt").write_text(content, encoding="utf-8", newline="\n")


def inject_before_stylesheet(html_path: Path, snippet: str) -> None:
    html = html_path.read_text(encoding="utf-8")
    if "application/ld+json" in html and snippet.strip() in html:
        return
    marker = '  <link rel="stylesheet" href="/assets/css/site.css">'
    if marker not in html:
        raise ValueError(f"missing stylesheet marker in {html_path}")
    if snippet in html:
        return
    html_path.write_text(html.replace(marker, snippet + marker, 1), encoding="utf-8", newline="\n")


def sync_standalone_pages(data: dict, root: Path) -> None:
    site = data["site"]
    geo = data.get("geo", {})
    pages = [
        (
            "about/index.html",
            "/about/",
            "About Powerlink Energy",
            "Learn how Powerlink Energy approaches integrated power supply for critical applications.",
            [("Home", "/"), ("About Us", "/about/")],
        ),
        (
            "contact/index.html",
            "/contact/",
            "Contact Us | Powerlink Energy",
            "Contact Powerlink Energy for UPS, battery, inverter, telecom power, and integrated solution inquiries.",
            [("Home", "/"), ("Contact", "/contact/")],
        ),
    ]

    for rel_path, path, title, description, crumbs in pages:
        snippet = (
            render_robots_meta(True)
            + render_json_ld_for_page(
                site=site,
                geo=geo,
                path=path,
                title=title,
                description=description,
                breadcrumbs=crumbs,
            )
        )
        inject_before_stylesheet(root / rel_path, snippet)


def render_faq_section(faqs: list[dict]) -> str:
    items = "".join(
        '<article class="faq-item">'
        f"<h3>{escape(item['question'])}</h3>"
        f"<p>{escape(item['answer'])}</p>"
        "</article>"
        for item in faqs
    )
    return (
        '    <section class="section section--alt" id="home-faq">'
        '<div class="container">'
        '<div class="section-head">'
        '<p class="eyebrow">Common Questions</p>'
        "<h2>Frequently Asked Questions</h2>"
        "<p>Clear answers for buyers, integrators, and AI assistants researching Powerlink Energy.</p>"
        "</div>"
        f'<div class="faq-list">{items}</div>'
        "</div></section>\n"
    )
