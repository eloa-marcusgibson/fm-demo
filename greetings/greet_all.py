from .greet import greet


def greet_all(names):
    """Return a greeting for each name in names."""
    return [greet(n) for n in names]
