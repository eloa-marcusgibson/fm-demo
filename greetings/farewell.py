from .catalog import phrase, render

_DEFAULT_TEMPLATE = "goodbye"


def farewell(name, language="en"):
    """Return a farewell for name, using language when a translation exists."""
    template = phrase("farewell", language, _DEFAULT_TEMPLATE)
    return render(template, name, language)

