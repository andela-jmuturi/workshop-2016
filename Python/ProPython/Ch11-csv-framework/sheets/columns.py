import decimal
import datetime


class CounterMeta(type):
    """
    A simple metaclass that keeps track of the order that each instance of a
    given class was instantiated.
    """

    counter = 0

    def __call__(cls, *args, **kwargs):
        obj = super(CounterMeta, cls).__call__(*args, **kwargs)
        obj.counter = CounterMeta.counter
        CounterMeta.counter += 1
        return obj


class Column(metaclass=CounterMeta):
    """
    An individual column with a CSV file.

    This serves as a base for attributes and methods that are common to all
    types of  columns.
    Subclasses of Column will define behaviour for more specific data types.
    """

    # Update this for every Column that's instantiated.
    counter = 0

    def __init__(self, title=None, required=True):
        self.title = title
        self.required = required

    def attach_to_class(self, cls, name, dialect):
        """
        Attach a field to the class it's assigned to.

        By default, Python adds attributes to classes they're defined in.
        However, this method will allow us to convey more information to the
        field than would be possible if we use the default Python behaviour.

        cls
            The class the field is assigned to. Allows us access to more
            information like name of the class, other attributes and methods
            in the class, class module, e.t.c

        name
            Name given to the attribute when it's assigned. This will serve as
            the field title in cases where no title was provided.

        options
            Options that may have a bearing on the field behaviour,
            e.g. encoding.
        """
        self.cls = cls
        self.name = name
        self.dialect = dialect

        if self.title is None:
            # Explicitly check for None for an empty string will skip this.
            self.title = name.replace('_', ' ')

        # Add this column to the list of columns in the options.
        dialect.add_column(self)

    def to_python(self, value):
        """
        Convert the given string to a native Python object.
        """
        return value

    def to_string(self, value):
        """
        Convert the given Python object to a string.
        """
        return value


class StringColumn(Column):
    """
    A column that contains data formatted as generic strings.
    """
    pass


class IntegerColumn(Column):
    """
    A column that contains data in the form of numeric integers.
    """

    def to_python(self, value):
        return int(value)


class FloatColumn(Column):
    """
    A column that contains data in the form of floating point numbers.
    """
    def to_python(self, value):
        return float(value)


class DecimalColumn(Column):
    """
    A column that contains data in the form of decimal values, represented in
    Python by decimal.Decimal
    """

    def to_python(self, value):
        try:
            return decimal.Decimal(value)
        except decimal.InvalidOperation as e:
            raise ValueError(str(e))


class DateColumn(Column):
    """
    A column that contains data in form of Python dates, represented in Python
    by datetime.date

    format
        A strptime()-stype format string.
    """

    def __init__(self, *args, format='%Y-%m-%d', **kwargs):
        super().__init__(*args, **kwargs)
        self.format = format

    def to_python(self, value):
        """
        Parse a string value according to self.format and return only the
        date portion.
        """
        if isinstance(value, datetime.date):
            return value
        return datetime.datetime.strptime(value, self.format).date()

    def to_string(self, value):
        """
        Format a date according to self.format and return that as a string.
        """
        return value.strftime(self.format)
