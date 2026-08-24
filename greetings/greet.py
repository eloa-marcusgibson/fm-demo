from .catalog import phrase, render

_DEFAULT_TEMPLATE = "hello"


def greet(username, language="en"):
    """Return a greeting for username, using language when a translation exists."""
    if not isinstance(username, str):
        raise ValueError("username must be a str")
    template = phrase("greet", language, _DEFAULT_TEMPLATE)
    return render(template, username, language)

