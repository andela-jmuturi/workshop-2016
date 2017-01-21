import functools


def suppress_errors(log_func=None):
    """Automatically suppress any errors that occur within a function."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_func:
                    log_func(str(e))
        return wrapper
    return decorator
