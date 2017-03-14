from core.bayessian import reader
from model.bayessian.channel_colors import ChannelColors
from multiprocessing import Pool


def pooled(channel_color):
    bayessian_reader = reader.BayessianReader()
    bayessian_reader.process(channel_color)


if __name__ == '__main__':
    pooled(ChannelColors.CHANNEL_4)
