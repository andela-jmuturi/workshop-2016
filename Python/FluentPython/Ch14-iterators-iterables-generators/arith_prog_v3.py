import itertools


def arith_prog(begin, step, end=None):
    first = type(begin + step)(begin)
    ap_gen = itertools.count(begin, step)
    if end is not None:
        ap_gen = itertools.takewhile(lambda n: n < end, ap_gen)
    return ap_gen
