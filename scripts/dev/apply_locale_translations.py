"""Apply string-level translations to en.json and write zh/fr/ru locale files."""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCALES_DIR = ROOT / "assets" / "locales"
SKIP_KEYS = {
    "slug",
    "href",
    "image",
    "heroImage",
    "src",
    "icon",
    "email",
    "whatsapp",
    "domain",
    "ogImage",
    "ogImageWidth",
    "ogImageHeight",
}


def translate_tree(node, mapping: dict, parent_key: str | None = None):
    if isinstance(node, dict):
        return {k: translate_tree(v, mapping, k) for k, v in node.items()}
    if isinstance(node, list):
        return [translate_tree(item, mapping, parent_key) for item in node]
    if isinstance(node, str):
        if parent_key in SKIP_KEYS:
            return node
        return mapping.get(node, node)
    return node


def load_map(lang: str) -> dict:
    path = ROOT / "scripts" / "translation_maps" / f"{lang}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    en = json.loads((LOCALES_DIR / "en.json").read_text(encoding="utf-8"))
    for lang in ("zh", "fr", "ru", "ar"):
        mapping = load_map(lang)
        translated = translate_tree(deepcopy(en), mapping)
        out = LOCALES_DIR / f"{lang}.json"
        out.write_text(json.dumps(translated, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
