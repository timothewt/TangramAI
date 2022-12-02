import cv2 as cv
from settings import *


class ShapeValidation:
    def __init__(self):
        pass

    def validate(self, path_to_image: str):
        image = cv.imread(path_to_image, cv.IMREAD_GRAYSCALE)
        return (image != 255).sum() >= TANGRAM_AREA * .99
