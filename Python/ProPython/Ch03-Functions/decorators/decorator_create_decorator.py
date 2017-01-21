import functools


def decorator(declared_decorater):
    """
    Create a decorator out of a function, which will be used as a wrapper.

    >>> @decorator
    ... def suppress_errors(func, args, kwargs, log_func=None):
    ...     try:
    ...         return func(*args, **kwargs)
    ...     except Exception as e:
    ...         if log_func is not None:
    ...             log_func(str(e))
    ...
    >>> @suppress_errors
    ... def example():
    ...     return variable_that_does_not_exist
    ...
    >>> example()
    >>>
    >>> def print_logger(message):
    ...     print(message)
    ...
    >>> @suppress_errors(log_func=print_logger)
    ... def example2():
    ...     return nonexistent_variable
    ...
    >>> example2()
    name 'nonexistent_variable' is not defined
    >>>
    """
    @functools.wraps(declared_decorater)
    def final_decorator(func=None, **kwargs):
        # This is now exposed to the rest of the app as a decorator
        def decorated(func):
            # This is exposed to the rest of the app as the
            # decorated function, regardless of how it's called
            @functools.wraps(func)
            def wrapper(*a, **kw):
                # Used when executing the decorated function
                return declared_decorater(func, a, kw, **kwargs)
            return wrapper
        if func is None:
            # The decorator was called with arguments
            # rather than a function to decorate.
            return decorated
        # The decorator was called without arguments,
        # hence decorate the function immediately.
        return decorated(func)
    return final_decorator


if __name__ == '__main__':
    import doctest
    doctest.testmod()
