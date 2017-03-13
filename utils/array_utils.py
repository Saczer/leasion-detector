def generator(table):
    return (item for item in table)


def to_tuple(a):
    try:
        return tuple(to_tuple(i) for i in a)
    except TypeError:
        return a


