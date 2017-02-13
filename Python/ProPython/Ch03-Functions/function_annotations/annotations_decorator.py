"""
This module serves as an example to illustrate how annotations may be used
by libraries and frameworks.

Verifies that a function is called with the right argument types and that
it returns a value of the right type, according to its annotations.
"""
import inspect
import functools
from itertools import chain


def annotations_processor(process):
    """
    Creates a decorator that processes annotations for each argument passed
    into its target function, raising an exception if there's a problem.
    """

    @functools.wraps(process)
    def decorator(func):
        # Validate the annotation types, as they must be valid Python types
        # for the rest of this decorator to work correctly.
        spec = inspect.getfullargspec(func)
        annotations = spec.annotations

        defaults = spec.defaults or ()
        defaults_zip = zip(spec.args[-len(defaults):], defaults)
        kwonlydefaults = spec.kwonlydefaults or {}

        for name, value in chain(defaults_zip, kwonlydefaults.items()):
            if name in annotations:
                process(value, annotations[name])

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
                if name in annotations:
                    process(arg, annotations[name])

            # Deal with variable positional arguments
            if spec.varargs and spec.varargs in annotations:
                annotation = annotations[spec.varargs]
                for arg in args[len(spec.args):]:
                    process(arg, annotation)

            # Deal with variable keyword arguments
            if spec.varkw and spec.varkw in annotations:
                annotation = annotations[spec.varkw]
                for name, arg in keyword_args.items():
                    process(arg, annotation)

            r = func(*args, **kwargs)
            if 'return' in annotations:
                process(r, annotations['return'])

            return r
        return wrapper
    return decorator


@annotations_processor
def typesafe(value, annotation):
    """
    Verify that a function is called with the right argument types and that
    it returns a value of the right type, according to its annotations.
    """
    if not isinstance(value, annotation):
        raise TypeError(f'Expected {annotation.__name__}, got {type(value).__name__}')


@typesafe
def example(*args: int, **kwargs: str):
    return (args, kwargs)


def main():
    print(example(spam='eggs'))
    print(example(kwargs='spam'))
    print(example(args='spam'))


# if __name__ == '__main__':
main()
