import json
from pathlib import Path
from string import Formatter

_LANG_DIR = Path(__file__).resolve().parent.parent / "lang"
_cache = {}
_formatter = Formatter()


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


def validate_template(template, language):
    try:
        parsed = list(_formatter.parse(template))
    except ValueError:
        raise ValueError(
            f"invalid template for locale {language}: unbalanced braces"
        ) from None
    fields = []
    for _literal, field_name, format_spec, conversion in parsed:
        if field_name is None:
            continue
        if field_name != "name" or format_spec or conversion:
            raise ValueError(
                f"invalid template for locale {language}: unknown placeholder"
            )
        fields.append(field_name)
    return fields


def select_template(value, count, language):
    if count is not None and not isinstance(count, int):
        raise ValueError("count must be an int")
    if isinstance(value, dict):
        for entry in value.values():
            if isinstance(entry, str):
                validate_template(entry, language)
        if count == 1 and "one" in value:
            return value["one"]
        if "other" in value:
            return value["other"]
        raise ValueError(f"invalid template for locale {language}: missing other")
    return value


def render(template, name, language):
    fields = validate_template(template, language)
    if "name" in fields:
        return template.format(name=name)
    return f"{template} {name}"
