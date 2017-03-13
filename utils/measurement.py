from utils.eutils import *
import time


def time_measurement(func):
    if not callable(func):
        raise MeasurementError("The argument should specify callable")

    def wrapper(*args):
        t = time.clock()
        res = func(*args)
        print(func.__name__, time.clock() - t)
        return res

    return wrapper
