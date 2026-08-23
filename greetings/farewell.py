import json
from pathlib import Path

_LANG_FILE = Path(__file__).resolve().parent.parent / "greetings_lang.json"
_DEFAULT_TEMPLATE = "goodbye"
_translations = None


def _get_translations():
    global _translations
    if _translations is None:
        with _LANG_FILE.open(encoding="utf-8") as f:
            _translations = json.load(f)
    return _translations


def farewell(name, language="en"):
    """Return a farewell for name, using language when a translation exists."""
    template = _DEFAULT_TEMPLATE
    if language != "en":
        template = _get_translations().get(language, _DEFAULT_TEMPLATE)
    return f"{template} {name}"
