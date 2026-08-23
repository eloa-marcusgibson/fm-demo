import json
from pathlib import Path

_LANG_FILE = Path(__file__).resolve().parent.parent / "greetings_lang.json"
_DEFAULT_TEMPLATE = "goodbye"


def farewell(name, language="en"):
    template = _DEFAULT_TEMPLATE
    if language != "en":
        with _LANG_FILE.open(encoding="utf-8") as f:
            translations = json.load(f)
        template = translations.get(language, _DEFAULT_TEMPLATE)
    return f"{template} {name}"
