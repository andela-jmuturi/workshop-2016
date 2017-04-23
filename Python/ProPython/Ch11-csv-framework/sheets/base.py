from collections import OrderedDict
import csv

from sheets import options


class RowMeta(type):
    def __init__(cls, name, bases, attrs):
        if 'Dialect' in attrs:
            # Filter out Python's additions to the namespace
            items = attrs.pop('Dialect').__dict__.items()
            items = {k: v for k, v in items if not k.startswith('__')}
        else:
            # No dialect options defined explicitly.
            items = {}

        # Keep dialect options assigned to the class itself to maintain as much
        # information as possible.
        cls._dialect = options.Dialect(**items)

        # Locate field attributes and attach them to the class.
        for key, attr in attrs.items():
            if hasattr(attr, 'attach_to_class'):
                attr.attach_to_class(cls, key, cls._dialect)

        # Sort the columns according to the order of their instantiation
        cls._dialect.columns.sort(key=lambda column: column.counter)

    @classmethod
    def __prepare__(self, name, bases):
        return OrderedDict()


class Row(metaclass=RowMeta):
    def __init__(self, *args, **kwargs):
        # First make sure the arguments make sense
        column_names = [column.name for column in self._dialect.columns]

        if len(args) > len(column_names):
            msg = "__init__() takes at most {} arguments. {} given."
            raise TypeError(msg.format(len(self._dialect.columns, len(args))))

        # Check if we got invalid kwarg
        for name in kwargs:
            if name not in column_names:
                msg = "__init__() got an unexpect keyword argument '{}'"
                raise TypeError(msg.format(name))

        # Confirm that we don't have multiple values for same argument
        # If we don't add it to kwargs
        for i, name in enumerate(column_names[:len(args)]):
            if name in kwargs:
                msg = "__init__() got multiple values for keyword argument '{}'"
                raise TypeError(msg.format(name))
            kwargs[name] = args[i]

        # Populate actual values on the object
        for column in self._dialect.columns:
            try:
                value = column.to_python(kwargs[column.name])
            except KeyError:
                value = None

            setattr(self, column.name, value)

    @classmethod
    def reader(cls, file):
        return Reader(cls, file)

    @classmethod
    def writer(cls, file):
        return Writer(file, cls._dialect)


class Reader:
    def __init__(self, row_cls: Row, file):
        self.row_cls = row_cls
        self.csv_reader = csv.reader(file, **row_cls._dialect.csv_dialect)
        self.skip_header_row = row_cls._dialect.has_header_row

    def __iter__(self):
        return self

    def __next__(self):
        # Skip the first row if it's a header
        if self.skip_header_row:
            self.csv_reader.__next__()
            self.skip_header_row = False

        return self.row_cls(*self.csv_reader.__next__())


class Writer:
    def __init__(self, file, dialect: options.Dialect):
        self.columns = dialect.columns
        self._writer = csv.writer(file, dialect.csv_dialect)
        self.needs_header_row = dialect.has_header_row

    def writerow(self, row):
        if self.needs_header_row:
            values = [column.title.title() for column in self.columns]
            self._writer.writerow(values)
            self.needs_header_row = False

        values = [getattr(row, column.name) for column in self.columns]
        self._writer.writerow(values)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
