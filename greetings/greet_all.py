from .greet import greet


def greet_all(names, language="en"):
    """Return a greeting for each name in names, using language when a translation exists."""
    for name in names:
        if not isinstance(name, str):
            raise ValueError("each name must be a str")
    return [greet(n, language=language) for n in names]
