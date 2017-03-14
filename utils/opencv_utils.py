from utils.decorators import constant


class Constants(object):
    @constant
    def FACTOR(self):
        return 0.5


def is_skin(val):
    return val > 0


def calculate_probability(skin_value, non_skin_value, total_count):
    skin_probability = skin_value / total_count
    non_skin_probability = non_skin_value / total_count

    result = (skin_probability * 0.5) / (
        (skin_probability * 0.5) + (non_skin_probability * 0.5))
    return result


__all__ = [
    'is_skin', 'calculate_probability'
]
