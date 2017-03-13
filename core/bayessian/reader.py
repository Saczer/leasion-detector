import cv2
from abc import ABC, abstractmethod
from utils import array_utils as util, opencv_utils as cv_util, file_utils as files, measurement
from model.bayessian import *


class Reader(ABC):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def process(self):
        pass

    @abstractmethod
    def store_in_files(self, directory):
        pass


class BayessianReader(Reader):
    def __init__(self, mask_directory='..\..\mask', database_images_directory='..\..\images'):
        self.masks_directory = mask_directory
        self.database_images_directory = database_images_directory
        self.bayesian_probability_maps = {}
        self.look_up_tables = {}

    def process(self):
        pass

    def read(self):
        table = ColorLookUpTable(ChannelColors.CHANNEL_256.value)
        reducer = Reducer()

        masks = dict(files.images_list(self.masks_directory))
        for image_name, image_dir in files.images_union(files.images_list(self.masks_directory),
                                                        files.images_list(self.database_images_directory)):
            current_mask_dir = masks.get(image_name)
            if current_mask_dir:
                img = cv2.imread(image_dir, cv2.IMREAD_GRAYSCALE)
                mask = cv2.imread(mask_dir, cv2.IMREAD_GRAYSCALE)

                self._read_single(mask, img, table, reducer)

    def store_in_files(self, directory):
        pass

    @measurement.time_measurement
    def _read_single(self, mask, img, table, reducer):
        width, height, channels = img.shape

        indices = list([(x, y) for y in range(height) for x in range(width)])
        for x, y in indices:
            (b, g, r) = img[x, y]
            bgr = (b, g, r)
            bgr = reducer.reduce(bgr)
            if cv_util.is_skin(mask[x, y]):
                table.add_skin_class(bgr)
            else:
                table.add_non_skin(bgr)

# table = ColorLookUpTable(ChannelColors.CHANNEL_256.value)
#
# colors = []
#
# masks = dict(files.images_list('..\..\mask'))
# for image_name, image_dir in files.images_union(files.images_list('..\..\images'), files.images_list('..\..\mask')):
#     mask_dir = masks.get(image_name)
#     if mask_dir:
#         print('{}, {}, {}'.format(mask_dir,
#                                   image_name,
#                                   image_dir))
#         img = cv2.imread(image_dir, cv2.IMREAD_COLOR)
#         msk = cv2.imread(mask_dir, cv2.IMREAD_GRAYSCALE)
#         width, height, channels = img.shape
#
#         indices = list([(x, y) for y in range(height) for x in range(width)])
#         for x, y in indices:
#             (b, g, r) = img[x, y]
#             bgr = (b, g, r)
#             if cv_util.is_skin(msk[x, y]):
#                 table.add_skin_class(bgr)
#             else:
#                 table.add_non_skin(bgr)
#         print('done')
#
# for (b, g, r), count in util.generator(table.skin_class.items()):
#     print('blue {} '.format(b))
#     print('green {} '.format(g))
#     print('red {} '.format(r))
#     print('color count {} \n'.format(count))
#
# print(len(table.skin_class))
# print(len(table.non_skin_class))
# print(table.total_count)
