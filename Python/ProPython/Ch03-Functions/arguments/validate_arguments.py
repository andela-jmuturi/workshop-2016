import inspect

from log_args2 import get_arguments


def validate_arguments(func, args, kwargs):
    """
    Given a function and its arguments, return a dictionary
    with any errors that are posed by the given arguments.
    """
    arguments = get_arguments(func, args, kwargs)
    spec = inspect.getfullargspec(func)
    errors = {}

    declared_args = spec.args[:]
    declared_args.extend(spec.kwonlyargs)

    # Start off my making sure all required args were provided.
    for name in declared_args:
        if name not in arguments:
            errors[name] = 'Required argument not provided.'

    # Ensure that the function can handle all the provided arguments
    for name in arguments:
        if name not in declared_args:
            errors[name] = 'Unknown argument provided'

    return errors
