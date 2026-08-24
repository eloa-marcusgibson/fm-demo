from .catalog import phrase, render, select_template

_DEFAULT_TEMPLATE = "goodbye"


def farewell(name, language="en", count=None):
    """Return a farewell for name, using language when a translation exists."""
    template = select_template(
        phrase("farewell", language, _DEFAULT_TEMPLATE), count, language
    )
    return render(template, name, language)

