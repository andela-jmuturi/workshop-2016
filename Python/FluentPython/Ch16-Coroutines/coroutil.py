"""
Decorator for priming a coroutine.

Priming a corouting is calling `next(coroutine)` before calling
coroutine.send(...)
"""
from functools import wraps


def coroutine(func):
    """Decorator primes `func` before advancing it to first yield"""
    @wraps(func)
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer
