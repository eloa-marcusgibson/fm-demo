from .catalog import phrase

_DEFAULT_TEMPLATE = "hello"


def greet(username, language="en"):
    """Return a greeting for username, using language when a translation exists."""
    template = phrase("greet", language, _DEFAULT_TEMPLATE)
    return f"{template} {username}"

