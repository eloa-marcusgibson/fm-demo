import json
from pathlib import Path

_LANG_DIR = Path(__file__).resolve().parent.parent / "lang"
_cache = {}


def language_codes():
    found = {"en"}
    if _LANG_DIR.is_dir():
        for path in _LANG_DIR.glob("*.json"):
            found.add(path.stem)
    return sorted(found)


def phrase(kind, language, default):
    if language == "en":
        return default
    if language not in _cache:
        path = _LANG_DIR / f"{language}.json"
        if path.is_file():
            with path.open(encoding="utf-8") as f:
                _cache[language] = json.load(f)
        else:
            _cache[language] = None
    data = _cache[language]
    if not data:
        return default
    return data.get(kind, default)
