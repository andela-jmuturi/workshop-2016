"""
This module serves as an example to illustrate how annotations may be used
by libraries and frameworks.

Verifies that a function is called with the right argument types and that
it returns a value of the right type, according to its annotations.
"""
import inspect
import functools
from itertools import chain


def typesafe(func):
    """
    Verify that a function is called with the right argument types and that
    it returns a value of the right type, according to its annotations.
    """

    # Validate the annotation types, as they must be valid Python types
    # for the rest of this decorator to work correctly.
    spec = inspect.getfullargspec(func)
    annotations = spec.annotations
    for name, annotation in annotations.items():
        if not isinstance(annotation, type):
            raise TypeError(f'The annotation for {name} is not a type.')

    error = "Wrong type for {}: expected {}, got {}."

    # Validate default values.
    defaults = spec.defaults or ()
    defaults_zip = zip(spec.args[-len(defaults):], defaults)
    kwonlydefaults = spec.kwonlydefaults or {}

    for name, value in chain(defaults_zip, kwonlydefaults.items()):
        if name in annotations and not isinstance(value, annotations[name]):
            raise TypeError(error.format(
                f'default value of {name}',
                annotations[name].__name__,
                type(value).__name__
            ))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Populate a dictionary of explicit arguments passed positionally.
        explicit_args = dict(zip(spec.args, args))
        keyword_args = kwargs.copy()

        # Add all explicit arguments passed by keyword
        for name in chain(spec.args, spec.kwonlyargs):
            if name in kwargs:
                explicit_args[name] = keyword_args.pop(name)

        # Deal with explicit arguments
        for name, arg in explicit_args.items():
            if name in annotations and not isinstance(arg, annotations[name]):
                raise TypeError(error.format(
                    name,
                    annotations[name].__name__,
                    type(arg).__name__
                ))

        # Deal with variable positional arguments
        if spec.varargs and spec.varargs in annotations:
            annotation = annotations[spec.varargs]
            for i, arg in enumerate(args[len(spec.args):]):
                if not isinstance(arg, annotation):
                    raise TypeError(error.format(
                        f'variable argument {i + 1}',
                        annotation.__name__,
                        type(arg).__name__
                    ))

        # Deal with variable keyword arguments
        if spec.varkw and spec.varkw in annotations:
            annotation = annotations[spec.varkw]
            for name, arg in keyword_args.items():
                if not isinstance(arg, annotation):
                    raise TypeError(error.format(
                        name,
                        annotation.__name__,
                        type(arg).__name__
                    ))

        r = func(*args, **kwargs)
        if 'return' in annotations and not isinstance(r, annotations['return']):
            raise TypeError(error.format(
                'the return value',
                annotations['return'].__name__,
                type(r).__name__
            ))

        return r

    return wrapper


@typesafe
def example(*args: int, **kwargs: str):
    return (args, kwargs)


def main():
    print(example(spam='eggs'))
    print(example(kwargs='spam'))
    print(example(args='spam'))

if __name__ == '__main__':
    main()
