class UtilsError(Exception):
    def __str__(self):
        return self.__class__.__name__ + ': ' + Exception.__str__(self)


class MeasurementError(UtilsError):
    pass


__all__ = [
    'UtilsError', 'MeasurementError'
]
