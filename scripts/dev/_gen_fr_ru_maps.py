"""Generate translation_data_fr.py and translation_data_ru.py from embedded translations."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STRINGS_FILE = ROOT / "assets" / "locales" / "_strings.txt"
DATA_FILE = Path(__file__).with_name("_fr_ru_translations.json")
RU_FILE = Path(__file__).with_name("_ru_translations.json")
OUT_FR = Path(__file__).with_name("translation_data_fr.py")
OUT_RU = Path(__file__).with_name("translation_data_ru.py")


def py_dict_literal(mapping: dict[str, str]) -> str:
    lines = ["{"]
    for key, value in mapping.items():
        lines.append(f"    {json.dumps(key, ensure_ascii=False)}: {json.dumps(value, ensure_ascii=False)},")
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    strings = STRINGS_FILE.read_text(encoding="utf-8").splitlines()
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    fr = data["fr"]
    ru = json.loads(RU_FILE.read_text(encoding="utf-8"))

    missing_fr = [s for s in strings if s not in fr]
    missing_ru = [s for s in strings if s not in ru]
    if missing_fr:
        raise SystemExit(f"FR missing {len(missing_fr)}: {missing_fr[:5]}")
    if missing_ru:
        raise SystemExit(f"RU missing {len(missing_ru)}: {missing_ru[:5]}")

    fr_map = {s: fr[s] for s in strings}
    ru_map = {s: ru[s] for s in strings}

    OUT_FR.write_text(
        '"""French translation map for Powerlink Energy website."""\n\nFR_MAP = '
        + py_dict_literal(fr_map)
        + "\n",
        encoding="utf-8",
    )
    OUT_RU.write_text(
        '"""Russian translation map for Powerlink Energy website."""\n\nRU_MAP = '
        + py_dict_literal(ru_map)
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUT_FR.name} ({len(fr_map)} entries)")
    print(f"Wrote {OUT_RU.name} ({len(ru_map)} entries)")


if __name__ == "__main__":
    main()
