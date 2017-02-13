"""
This module serves as an example to illustrate how annotations may be used
by libraries and frameworks.

Verifies that a function is called with the right argument types and that
it returns a value of the right type, according to its annotations.
"""
import inspect
import functools
from itertools import chain


def annotations_decorator(process):
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
            new_args = []
            new_kwargs = {}
            keyword_args = kwargs.copy()

            # Deal with explicit arguments passed positionally.
            for name, arg in zip(spec.args, args):
                if name in annotations:
                    new_args.append(process(arg, annotations[name]))

            # Deal with explicit arguments passed by keyword.
            for name, arg in chain(spec.args, spec.kwonlyargs):
                if name in kwargs and name in annotations:
                    new_kwargs[name] = process(keyword_args.pop(name), annotations[name])

            # Deal with variable positional arguments
            if spec.varargs and spec.varargs in annotations:
                annotation = annotations[spec.varargs]
                for arg in args[len(spec.args):]:
                    new_args.append(process(arg, annotation))

            # Deal with variable keyword arguments
            if spec.varkw and spec.varkw in annotations:
                annotation = annotations[spec.varkw]
                for name, arg in keyword_args.items():
                    new_kwargs[name] = process(arg, annotation)

            r = func(*new_args, **new_kwargs)
            if 'return' in annotations:
                r = process(r, annotations['return'])

            return r
        return wrapper
    return decorator


@annotations_decorator
def coerce_arguments(value, annotation):
    return annotation(value)


@annotations_decorator
def typesafe(value, annotation):
    """
    Verify that a function is called with the right argument types and that
    it returns a value of the right type, according to its annotations.
    """
    if not isinstance(value, annotation):
        raise TypeError(f'Expected {annotation.__name__}, got {type(value).__name__}')
    return value


@typesafe
def example(*args: int, **kwargs: str):
    return (args, kwargs)


def main():
    print(example(spam='eggs'))
    print(example(kwargs='spam'))
    print(example(args='spam'))


if __name__ == '__main__':
    main()
