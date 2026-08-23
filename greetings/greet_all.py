from .greet import greet


def greet_all(names):
    return [greet(n) for n in names]
