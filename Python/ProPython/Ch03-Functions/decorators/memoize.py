import functools


def memoize(func):
    """
    Cache the results of a function so it's not called again
    when the same arguments are provided again.
    """
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        # Dictionaries (kwargs) can't be used as dict keys, so use only args here.
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return wrapper


@memoize
def multiply(a, b):
    return a * b


@memoize
def factorial(n):
    result = 1
    for i in range(n):
        result *= i + 1
    return result
