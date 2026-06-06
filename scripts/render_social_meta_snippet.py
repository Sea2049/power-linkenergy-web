"""Print social meta tags for standalone HTML pages (about, contact)."""

from __future__ import annotations

import json
from pathlib import Path

from generate_static_pages import load_data, render_social_meta, resolve_og_image


def main() -> None:
    data = load_data()
    site = data["site"]
    pages = [
        ("/about/", "About Powerlink Energy", "Learn how Powerlink Energy approaches integrated power supply for critical applications."),
        (
            "/contact/",
            "Contact Us | Powerlink Energy",
            "Contact Powerlink Energy for UPS, battery, inverter, telecom power, and integrated solution inquiries.",
        ),
    ]
    for path, title, description in pages:
        image_path, image_alt, width, height = resolve_og_image(site)
        print(f"<!-- {path} -->")
        print(render_social_meta(path, title, description, image_path, image_alt, width, height), end="")


if __name__ == "__main__":
    main()
