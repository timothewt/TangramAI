from __future__ import annotations
from math import floor, sqrt, ceil
from utils import *
import cv2 as cv


class ImageProcessor:
    """
    Used to process the input image, turns it black and white and makes it the good size

    Attributes:
        corners:    corners of the shape on the image
        image:      image of the puzzle shadow
    """
    def __init__(self, path_to_image: str = None) -> None:
        self.corners = []
        self.image = None
        if path_to_image is not None:
            self.image = self.load_image(path_to_image)

    def load_image(self, path_to_image: str) -> np.ndarray:
        """
        loads the image_processor into a 2d np array with 255 as white pixels and 0 as black pixels, resizes it and turns it
        into black and white again
        :param path_to_image: path of the image_processor
        :return: a 2d numpy array of the resized b&w image_processor
        """
        image = cv.imread(path_to_image, cv.IMREAD_GRAYSCALE)

        black_and_white_image = self.image_to_black_and_white(image)
        resized_image = self.resize_image(black_and_white_image)  # resizes the image_processor for the tangram pieces to be the good size
        resized_black_and_white_image = self.image_to_black_and_white(resized_image)  # to b&w to eliminate gray pixels
        self.corners = get_corners(resized_black_and_white_image)
        return resized_black_and_white_image

    def resize_image(self, image: np.ndarray) -> np.ndarray:
        """
        resizes the image_processor for the area of the drawing to match the area of all the tangram pieces, which is 280*280
        :param image: image_processor we want to resize
        :return: the np array of the black and white resized image_processor
        """
        resized_image = image.copy()
        (h, w) = image.shape[:2]
        black_pixels = (image == 0).sum()
        resize_ratio = ceil(sqrt(pow(settings.TANGRAM_SIDE_LENGTH, 2) / black_pixels) * 10) / 10
        (new_h, new_w) = (int(resize_ratio * h), int(resize_ratio * w))
        resized_image = cv.resize(resized_image, (new_w, new_h), interpolation=cv.INTER_CUBIC)
        self.resize_corners(resize_ratio)
        return resized_image

    def resize_corners(self, resize_ratio: float) -> None:
        """
        Changes the coordinates of the corners for the resized image_processor
        :param resize_ratio: ratio of resizing
        """
        resized_corners = []
        for i in range(0, len(self.corners)):
            resized_corners.append(Point(floor(self.corners[i][0] * resize_ratio), floor(self.corners[i][1] * resize_ratio)))
        self.corners = resized_corners

    @staticmethod
    def image_to_black_and_white(image: np.ndarray) -> np.ndarray:
        """
        turns a picture to black and white
        :param image: image_processor we want to convert to b&w
        :return: the np array of the black (0) and white (255) pixels
        """
        b_w_image = image.copy()
        b_w_image = cv.threshold(b_w_image, 250, 255, cv.THRESH_BINARY)[1]
        return b_w_image


if __name__ == "__main__":
    pass