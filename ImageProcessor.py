from math import floor, sqrt, ceil

import cv2 as cv
from elements import *


class ImageProcessor:
    def __init__(self, path_to_image: str) -> None:
        self.corners = []
        self.image = self.load_image(path_to_image)  # image of the shape we want to reproduce with the tangram pieces

    def load_image(self, path_to_image: str) -> np.ndarray([], dtype=int):
        """
        loads the image into a 2d np array with 255 as white pixels and 0 as black pixels, resizes it and turns it
        into black and white
        :param path_to_image: path of the image
        :return: a 2d numpy array of the resized b&w image
        """
        image = cv.imread(path_to_image, cv.IMREAD_GRAYSCALE)

        self.corners = self.get_corners_coordinates(image.copy())

        black_and_white_image = self.image_to_black_and_white(image)
        resized_image = self.resize_image(black_and_white_image)  # resizes the image for the tangram pieces to be the good size
        resized_black_and_white_image = self.image_to_black_and_white(resized_image)  # to b&w to eliminate gray pixels
        return resized_black_and_white_image

    def get_corners_coordinates(self, image: np.ndarray([], dtype=int)):
        """
        Gives the coordinates of all the corners of the shape to draw using the Harris corner detection algorithm
        :param image: image from which we want the corners
        :return: a list of the corners
        """
        dst = cv.cornerHarris(image, 5, 3, 0.04)
        ret, dst = cv.threshold(dst, 0.1 * dst.max(), 255, 0)
        dst = np.uint8(dst)
        ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv.cornerSubPix(image, np.float32(centroids), (5, 5), (-1, -1), criteria)
        return corners

    def resize_image(self, image: np.ndarray([], dtype=int)) -> np.ndarray([], dtype=int):
        """
        resizes the image for the area of the drawing to match the area of all the tangram pieces, which is 280*280
        :param image: image we want to resize
        :return: the np array of the black and white resized image
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
        Changes the coordinates of the corners for the resized image
        :param resize_ratio: ratio of resizing
        """
        resized_corners = []
        for i in range(0, len(self.corners)):
            resized_corners.append(Point(floor(self.corners[i][0] * resize_ratio), floor(self.corners[i][1] * resize_ratio)))
        self.corners = resized_corners

    def image_to_black_and_white(self, image: np.ndarray([], dtype=int)) -> np.ndarray([], dtype=int):
        """
        turns a picture to black and white
        :param image: image we want to convert to b&w
        :return: the np array of the black (0) and white (255) pixels
        """
        b_w_image = image.copy()
        b_w_image = cv.threshold(b_w_image, 30, 255, cv.THRESH_BINARY)[1]
        return b_w_image


def show_image(image):
    cv.imshow("Tangram", image)
    cv.waitKey(0)


if __name__ == "__main__":
    pass