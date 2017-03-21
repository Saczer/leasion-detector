import cv2
import json
from abc import ABC, abstractmethod
from utils import opencv_utils as cv_util, file_utils as files, decorators
from model.bayessian import *
import os


class Reader(ABC):
    @abstractmethod
    def read(self, channel_color):
        pass

    @abstractmethod
    def process(self, channel_color):
        pass

    @abstractmethod
    def create_probability_map(self, table, reducer):
        pass

    @abstractmethod
    def store_in_files(self, directory, filename, probability_map):
        pass


class BayessianReader(Reader):
    def __init__(self, mask_directory='mask', database_images_directory='images'):
        self.masks_directory = mask_directory
        self.database_images_directory = database_images_directory

    def process(self, channel_color):
        table, reducer = self.read(channel_color)
        probability_map = self.create_probability_map(table, reducer)

        return self.store_in_files(self.DEFAULT_DIRECTORY, self.JSON_EXTENSION.format(channel_color.value),
                                   probability_map)

    pass

    def create_probability_map(self, table, reducer):
        probability_map = BayessianProbabilityMap(table.bins)

        total_count = table.total_count

        for key, count in table.skin_class.items():
            non_skin_color_count = table.non_skin_class.get(key, 0)
            skin_color_count = count

            probability = cv_util.calculate_probability(skin_color_count, non_skin_color_count, total_count)
            probability_map.lesion_probability[key] = probability
            probability_map.non_lesion_probability[key] = 1 - probability

        filtered = {(k, v) for k, v in table.non_skin_class.items() if
                    k not in probability_map.non_lesion_probability.items()}
        # filtered = filter(lambda key, value: not key in probability_map.non_lesion_probability,
        #                   table.non_skin_class())
        for key, count in filtered:
            skin_count = table.skin_class.get(key, 0)
            non_skin_count = count

            probability = cv_util.calculate_probability(skin_count, non_skin_count, total_count)
            probability_map.lesion_probability[key] = probability
            probability_map.non_lesion_probability[key] = 1 - probability

        return probability_map

    def read(self, channel_color):
        table = ColorLookUpTable(channel_color.value)
        reducer = Reducer(channel_color)

        masks = dict(files.images_list(self.masks_directory))
        for image_name, image_dir in files.images_union(files.images_list(self.database_images_directory),
                                                        files.images_list(self.masks_directory)):
            current_mask_dir = masks.get(image_name)
            if current_mask_dir:
                img = cv2.imread(image_dir, cv2.IMREAD_COLOR)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                mask = cv2.imread(current_mask_dir, cv2.IMREAD_GRAYSCALE)
                self._read_single(mask, img, table, reducer)
        return table, reducer

    def store_in_files(self, directory, filename, probability_map):
        with open(directory + '\\' + filename, mode='w', encoding='utf8') as output:
            str = json.dumps(probability_map.__dict__, indent=4, sort_keys=True, separators=(',', ':'))
            output.write(str)

    @decorators.time_measurement
    def _read_single(self, mask, img, table, reducer):
        width, height, channels = img.shape
        mask_width, mask_height = mask.shape

        if width == mask_width and height == mask_height:
            indices = list([(x, y) for y in range(height) for x in range(width)])
            for x, y in indices:
                [r, g, b] = img[x, y]
                color = Color(r, g, b)
                color = reducer.reduce(color)
                if cv_util.is_skin(mask[x, y]):
                    table.add_skin_class(color)
                else:
                    table.add_non_skin(color)

    @decorators.constant
    def DEFAULT_DIRECTORY():
        return 'jsons'

    @decorators.constant
    def JSON_EXTENSION():
        return 'bayessian-{}.json'
