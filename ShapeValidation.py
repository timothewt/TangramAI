import cv2 as cv
from settings import *


class ShapeValidation:
    def __init__(self):
        pass

    def validate(self, path_to_image: str) -> bool:
        """
        Tells if the shape is correct, i.e. that no pieces interlap and all the pieces are inside the image
        :param path_to_image: path to the image to validate
        :return: True if it is valid, False otherwise
        """
        image = cv.imread(path_to_image, cv.IMREAD_GRAYSCALE)
        return (image != 255).sum() >= TANGRAM_AREA * .99


if __name__ == "__main__":
    pass