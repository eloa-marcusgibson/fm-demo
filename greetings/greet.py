from .catalog import phrase, render, select_template

_DEFAULT_TEMPLATE = "hello"


def greet(username, language="en", count=None):
    """Return a greeting for username, using language when a translation exists."""
    if not isinstance(username, str):
        raise ValueError("username must be a str")
    template = select_template(
        phrase("greet", language, _DEFAULT_TEMPLATE), count, language
    )
    return render(template, username, language)

