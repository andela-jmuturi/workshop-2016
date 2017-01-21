# Decorators
- Functions that accept a callable and return a callable.
- Callable returned can be the one passed in or can be replaced with sth else entirely.
- Decorators are applied as:
  ```python
  @suppress_errors
  def log_error(message, log_file='errors.log'):
    """Log an error message to a file"""
    pass
  ```

  This syntax is equivalent to:
  ```python
  def log_error(...):
    pass
  log_error = suppress_errors(log_error)
  ```

## Wrappers
- Functions designed to contain another function, adding some extra behaviour before or after the contained function executes.
  ```python
  def suppress_errors(func):
    def wrapper(*args, **kwargs):
      try:
        return func(*args, **kwargs)
      except Exception:
        pass
    return wrapper
  ```
  `suppress_errors` (or a decorator) takes in a function as it's only argument, which isn't executed till the inner wrapper executes. The `wrapper` function must accept all arguments the wrapped function accepts, which is achieved by using variable positional arguments (`*args`) and keyword arguments (`**kwargs`) and passing them on to the wrapped function.

- Wrapping functions means loss of potentially useful information like the name, docstrings, e.t.c. of the wrapped function. `functools.wraps` decorator helps maintain some of the important information by copying over that information from the wrapped function to the wrapper function.
  ```python
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
  ```

## Decorators with Arguments
- Python evaluates the `@` line as an expression, whose result is applied as the decorator.
- Decorators, like `functools.wraps`, can also accept arguments.
  ```python
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
  ```
  When defined to accept args this way, you have to call the decorator in order for it to function correctly. As:
  ```python
  @suppress_errors()  # Function call here.
  def something():
      pass
  ```
  Instead of just:
  ```python
  @suppress_errors
  def something():
      pass
  ```
  Taking `functools.wraps` as an example,
  ```python
  @functools.wraps(func)
  def wrapper(*args, **kwargs):
      return func(*args, **kwargs)
  ```
  is equivalent to:
  ```python
  def wrapper(...):
    pass
  wrapper = functools.wraps(func)(wrapper)
  ```

## Decorators With or Without Arguments.
- Ideally, a decorator with arguments should be able to be called without parentheses if no arguments are provided, while still being able to provided the arguments where necessary.
- The outermost decorator function must be able to accept arbitrary arguments or a single function, tell the difference between the two and behave accordingly. Since decorators always receive the decorated function as a positional argument, we can make it the first argument and make it optional, then rely on keyword parameters for any other arguments. We can then branch out into a different code block if arguments are provided, rather than the function to be decorated.
  ```python
  import functools

  def suppress_errors(func=None, log_func=None):
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

      if func is None:
          return decorator
      return decorator(func)
  ```
  This allows `suppress_errors` to be called with or without arguments, but the rest of the arguments **must** be passed by keyword.

## Decorator to Create Decorators.
- Decorators are meant to avoid a lot of boilerplate and simplify functions, but end up complicated to support features as optional arguments.
- Can simplify creating new decorators by abstracting the decorators boilerplate into a decorator.
- The decorator we define in this case needs to distinguish between the arguments meant for the decorator and those meant for the function it decorates.
  ```python
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
  ```
  Using this decorator, we can define other decorators in terms of the `wrapper` function directly. Our declared decorator functions must always accept 3 arguments with any additional keyword arguments beyond those. The arguments are:
  - The function that'll be decorated.
  - A tuple of positional arguments supplied to the decorated function.
  - A dictionary of keyword arguments supplied to the decorated function.

  Usage is as shown in the docstrings.
