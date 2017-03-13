class BayessianProbabilityMap:
    """
    Encapsulate probability map colors to
    """
    def __init__(self, bins=256):
        super().__init__()
        self.bins = bins
        self.lesion_probability = {}
        self.non_lesion_probability = {}

    def __str__(self, *args, **kwargs):
        return 'Bayessian Probability map, bins {}, lesion size {}, non lesion size {}'.format(self.bins,
                                                                                               len(self.lesion_probability),
                                                                                               len(self.non_lesion_probability))

    def __repr__(self, *args, **kwargs):
        return 'Bayessian prop map, {} , {}, {}'.format(self.bins,
                                                        self.lesion_probability,
                                                        self.non_lesion_probability)


class ColorLookUpTable:
    """
    Encapsulate information about stored bins per channel and dictionaries for colors with number of occurrences
    """
    def __init__(self, bins, total_count=0):
        super().__init__()
        self.bins = bins
        self.total_count = total_count
        self.skin_class = {}
        self.non_skin_class = {}

    def __str__(self, *args, **kwargs):
        return 'Color table, bins {}, count {}'.format(self.bins,
                                                       self.total_count)

    def __repr__(self, *args, **kwargs):
        return 'Color table, {}, {}, {}, {}'.format(self.bins,
                                                    self.total_count,
                                                    len(self.skin_class),
                                                    len(self.non_skin_class))

    def add_skin_class(self, color):
        """
        Store a color in skin class dictionary, increasing total count and color count
        :param color: color to store in skin class
        """
        count = self.skin_class.get(color, 0)
        count += 1
        self.skin_class[color] = count
        self.total_count += 1

    def add_non_skin(self, color):
        """
        Store a color in non skin class dictionary, increasing to total count and color count in non skin class
        :param color: color to sore in non skin class
        """
        count = self.non_skin_class.get(color, 0)
        count += 1
        self.non_skin_class[color] = count
        self.total_count += 1



