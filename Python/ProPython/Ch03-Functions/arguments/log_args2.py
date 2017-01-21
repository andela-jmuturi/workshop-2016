"""
Logging arguments passed to a function: take 2
"""
import inspect


def get_arguments(func, args, kwargs):
    """
    Given a function and a set of arguments, return  a dictionary
    of argument values that will be sent to the function.
    """

    # Start with an empty dict, then add in default values. The defaults
    # will be overriden by actual values if such were provided.
    arguments = {}
    spec = inspect.getfullargspec(func)

    # When unavailable, spec.defaults and spec.kwonlydefaults are set to None
    if spec.defaults:
        # Reverse the positional args list and the defaults so
        # they still match up starting from the end.
        arguments.update(zip(reversed(spec.args), reversed(spec.defaults)))

    if spec.kwonlydefaults:
        # Since kwonlydefaults are a dict, update arguments with it.
        arguments.update(spec.kwonlydefaults)

    arguments.update(zip(spec.args, args))
    arguments.update(kwargs)

    return arguments
