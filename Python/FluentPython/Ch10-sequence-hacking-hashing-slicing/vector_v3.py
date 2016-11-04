from array import array
import reprlib
import math
import numbers


class Vector:
    typecode = 'd'
    shortcut_names = 'xyzt'

    def __init__(self, components):
        self._components = array(self.typecode, components)

    def __iter__(self):
        return iter(self._components)

    def __repr__(self):
        # use reprlib.repr to produce limited length representations
        components = reprlib.repr(self._components)
        components = components[components.find('['):-1]
        return 'Vector({})'.format(components)

    def __str__(self):
        return str(tuple(self))

    def __bytes__(self):
        return (bytes([ord(self.typecode)]) + bytes(self._components))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __abs__(self):
        return math.sqrt(sum([x * x for x in self]))

    def __bool__(self):
        return bool(abs(self))

    # __len__ and __getitem__ help us use Vector as a sequence.
    def __len__(self):
        return len(self._components)

    def __getitem__(self, index):
        cls = type(self)
        if isinstance(index, slice):
            return cls(self._components[index])
        elif isinstance(index, numbers.Integral):
            return self._components[index]
        else:
            msg = '{cls.__name__} indices must be integers'
            raise TypeError(msg.format(cls=cls))

    # Define __getattr__ so we can use shortcut_names names to access
    # the first few components of Vector.
    def __getattr__(self, name):
        cls = type(self)
        if len(name) == 1:  # if name is one character, it may be a shortcut.
            pos = cls.shortcut_names.find(name)

            # return the element if the position is within range
            if 0 <= pos < len(self._components):
                return self._components[pos]
        msg = '{.__name__!r} object has no attribute {!r}'
        raise AttributeError(msg.format(cls, name))

    # Add special handling for single-character attributes to ensure
    # consistency between getting and setting attributes. This will ensure
    # shortcut_names are not set to instance variables, i.e.
    # assuming v is a Vector:
    # v.x = 10 raises AttributeError.
    # v.xyz = 10 succeeds
    def __setattr__(self, name, value):
        cls = type(self)
        if len(name) == 1:
            if name in self.shortcut_names:
                error = 'readonly attribute {attr_name!r}'
            elif name.islower():
                error = "can't set attributes 'a' to 'z' in {cls_name!r}"
            else:
                error = ''
            if error:
                msg = error.format(cls_name=cls.__name__, attr_name=name)
                raise AttributeError(msg)
        super().__setattr__(name, value)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(memv)
