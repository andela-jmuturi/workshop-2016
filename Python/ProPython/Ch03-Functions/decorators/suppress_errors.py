import functools


def suppress_errors(func):
    """Automatically suppress any errors that occur within a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            pass
    return wrapper
