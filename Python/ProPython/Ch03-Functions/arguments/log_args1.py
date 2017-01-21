"""
Logging arguments passed to a function: initial version.
"""
import inspect


def get_arguments(func, args, kwargs):
    """
    Given a function and a set of arguments, return  a dictionary
    of argument values that will be sent to the function.
    """

    # kwargs don't need manual matching as they are provided with
    # the right values. Copy the kwargs dict since we'll be adding
    # fields to it.
    arguments = kwargs.copy()

    # Deal with positional arguments by figuring out which arg names
    # map to which positional values and adding the values to the
    # dictionary with appropriate names.
    spec = inspect.getfullargspec(func)
    arguments.update(zip(spec.args, args))

    # Deal with default values by extracting any default values that
    # were not already overriden by the provided arguments and adding
    # those to the dictionary.
    if spec.defaults:
        # Since optional args must come after required args,
        # use the size of the defaults to determine the names
        # of the positional args.
        for i, name in enumerate(spec.args[-len(spec.defaults):]):
            if name not in arguments:
                arguments[name] = spec.defaults[i]

    # Since keyword-only args can also take defaults,
    # getfullargspec returns a different dict for those.
    if spec.kwonlydefaults:
        for name, value in spec.kwonlydefaults.item():
            if name not in arguments:
                arguments[name] = value

    return arguments
