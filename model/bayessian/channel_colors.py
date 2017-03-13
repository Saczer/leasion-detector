from enum import Enum


class ChannelColors(Enum):
    """
    Enum describing color reduction possibilities
    """
    CHANNEL_4 = 4
    CHANNEL_8 = 8
    CHANNEL_16 = 16
    CHANNEL_32 = 32
    CHANNEL_64 = 64
    CHANNEL_128 = 128
    CHANNEL_256 = 256


class Reducer:
    """
    Reducer for colors to expected number of bins
    """
    """
    Maximum number of colors for multiplier
    """
    _MAX = 256

    def __init__(self, channel_colors=ChannelColors.CHANNEL_256):
        self.channel_colors = channel_colors

    def reduce(self, color_reduce):
        """
        Reduce the given color to expected value

        :param color_reduce: color to reduce by Reducer accepted in form of tuple
        :return: return a tuple of reduced colors
        """
        if self.channel_colors == ChannelColors.CHANNEL_256:
            return color_reduce

        b, g, r = color_reduce
        b = self._reduce_single(b, self.channel_colors.value)
        g = self._reduce_single(g, self.channel_colors.value)
        r = self._reduce_single(r, self.channel_colors.value)

        return b, g, r

    def _reduce_single(self, channel, reduce_value):
        """
        Reduce single color value to form of 0-255, the reduction is specified by reduce_value.
        The int casting is intentional as loosing precision is needed to calculate exact value

        :param channel: single channel to be reduced R, G, or B
        :param reduce_value: value specified for reduction factor
        :return: single channel color reduced to factor
        """
        multiplier = self._MAX / reduce_value

        if channel <= (multiplier * (reduce_value - 1)):
            return int(int((channel / multiplier) + 0.5) * multiplier)
        else:
            return self._MAX - 1
