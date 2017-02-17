"""
Functions assigned to classes are considered methods.
Work like functions in general, but have access to class information
since functions are actually descriptors.

Unbound methods - Methods can be accessed from a class as well as its
    instances since methods are descriptors and descriptors can be accessed
    from the class as well as its instances.
    Accessing a method from a class makes it an unbound method.
    The descriptor receives the class, but methods typically require the
    instance, so are referred to as unbound when accessed without one.

Bound methods - Once the class is instantiated, each method descriptor
    returns a function that's bound to that instance. The bound method
    automatically receives the instance object as the first argument.

Class methods - Methods that require access to the class they're defined
    in. Always receive the class object as first positional argument.
"""
