import os

IMAGES_DIR = '..\images'
MASK_DIR = '..\mask'
IMAGE_PATTERN = '.bmp'
COLORED_IMAGE_PATTERN = ".ppm"


def images_list(directory):
    for (dirpath, dirnames, filenames) in os.walk(directory):
        for filename in filenames:
            if filename.endswith(IMAGE_PATTERN) | filename.endswith(COLORED_IMAGE_PATTERN):
                yield os.path.splitext(filename)[0], os.sep.join([dirpath, filename])


def images_union(images, masks):
    masks_files = [file[0] for file in masks]
    return filter(lambda img: img[0] in masks_files, images)





