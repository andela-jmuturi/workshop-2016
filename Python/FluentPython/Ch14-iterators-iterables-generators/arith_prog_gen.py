def arith_prog_gen(begin, step, end=None):
    result = type(begin + step)(begin)
    forever = end is None
    index = 0

    while forever or result < end:
        yield result
        index += 1
        result = being + step * index
