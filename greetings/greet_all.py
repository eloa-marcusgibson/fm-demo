from .greet import greet


def greet_all(names):
    """Return a greeting for each name in names."""
    for name in names:
        if not isinstance(name, str):
            raise ValueError("each name must be a str")
    return [greet(n) for n in names]
