class PluginMount(type):
    """
    Place this metaclass on standard Python class to turn it into a
    plugin mount point. All subclasses are automatically registered
    as plugins.
    """
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            # The class has no plugins list, must be a mount point.
            # Add one for plugins to be registered later.
            cls.plugins = []
        else:
            # Already has plugins attribute, must be an individual
            # plugin. Register it.
            cls.plugins.append(cls)


class InputValidator(metaclass=PluginMount):
    """
    A plugin mount for input validation.

    Supported plugins must provide a validate(self, input) method,
    which receives input as a string and raises a ValueError if the
    input is invalid. If the input was properly valid, it should just
    return without error. Any return value will be ignored.
    """
    def validate(self, input):
        # Default implementation raises a NotImplementedError
        # to ensure any subclasses must override it.
        raise NotImplementedError


class AsciiValidator(InputValidator):
    """
    Validate input consists only of valid ASCII character.
    """
    def validate(self, input):
        # If encoding fails, str.encode() raises a UnicodeEncodeError,
        # which is a subclass of ValueError
        input.encode('ascii')


def is_valid(input):
    for plugin in InputValidator.plugins:
        try:
            plugin().validate(input)
        except ValueError:
            # ValueError means invalid input.
            return False
    return True
