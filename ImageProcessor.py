from math import floor, sqrt, ceil
import cv2 as cv
from settings import *
from elements import *


class ImageProcessor:
    def __init__(self, path_to_image: str) -> None:
        self.corners = []
        self.image = self.load_image(path_to_image)  # image of the shape we want to reproduce with the tangram pieces

    def load_image(self, path_to_image: str) -> np.ndarray([], dtype=int):
        """
        loads the image into a 2d np array with 255 as white pixels and 0 as black pixels, resizes it and turns it
        into black and white again
        :param path_to_image: path of the image
        :return: a 2d numpy array of the resized b&w image
        """
        image = cv.imread(path_to_image, cv.IMREAD_GRAYSCALE)
        self.corners = self.get_corners_coordinates(image.copy())
        black_and_white_image = self.image_to_black_and_white(image)
        resized_image = self.resize_image(black_and_white_image)  # resizes the image for the tangram pieces to be the good size
        resized_black_and_white_image = self.image_to_black_and_white(resized_image)  # to b&w to eliminate gray pixels
        show_image(resized_black_and_white_image)
        filled_image = self.fill_shape(resized_black_and_white_image)  # in case of small holes between very close pieces
        show_image(filled_image)
        return filled_image

    def get_corners_coordinates(self, image: np.ndarray([], dtype=int)):
        dst = cv.cornerHarris(image, 5, 3, 0.04)
        ret, dst = cv.threshold(dst, 0.1 * dst.max(), 255, 0)
        dst = np.uint8(dst)
        ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv.cornerSubPix(image, np.float32(centroids), (5, 5), (-1, -1), criteria)
        return corners

    def get_corners(self, image: np.ndarray) -> list[Corner]:
        """
        Gives the coordinates of all the corners of the shape, and all its edges
        :param image: image from which we want the corners and edges
        :return: a list of the corners, which also has the edges in it
        """
        contours = cv.findContours(image, 1, 2)[0]
        corners = []
        for i in range(0, len(contours)):
            corner = Corner(contours[i][0][0], contours[i][0][1])
            if len(corners) == 0:
                corners.append(corner)
                # Add edges
                if i < len(contours) - 1:
                    index = i + 1
                else:
                    index = 0
                point2 = Point(contours[index][0][0], contours[index][0][1])
                corner.second_edge = Edge(corner, point2)

            elif len(corners) > 0 and not corner.close_to(corners[-1], MIN_DIST_BETWEEN_TWO_CORNERS):
                # Add corner
                corners.append(corner)
                # Add edges
                if i < len(contours) - 1:
                    index = i + 1
                else:
                    index = 0
                point2 = Point(contours[index][0][0], contours[index][0][1])
                corner.first_edge = Edge(corner, corners[-1])
                corner.second_edge = Edge(corner, point2)
            else:
                # Update last corner
                if i < len(contours) - 1:
                    index = i + 1
                else:
                    index = 0
                point2 = Point(contours[index][0][0], contours[index][0][1])
                # Calculate new corner position
                corners[-1] = Corner(int((corners[-1].x + corner.x) / 2), int((corners[-1].y + corner.y) / 2))

                corners[-1].second_edge = Edge(corners[-1], point2)
                if len(corners) > 1:
                    corners[-2].second_edge = Edge(corners[-2], corners[-1])

        corners[0].first_edge = Edge(corners[0], corners[-1])
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
        b_w_image = cv.threshold(b_w_image, 250, 255, cv.THRESH_BINARY)[1]
        return b_w_image

    def fill_shape(self, image: np.ndarray) -> np.ndarray:
        """
        Fills the eventual holes between two pieces. It could've happened during the composing because of the grid
        :param image: black and white image that we fill
        :return: the image filled
        """
        for i in range(len(image) - 3):
            for j in range(len(image[0]) - 3):
                if image[i][j] == 0:
                    if image[i][j + 1] == 255 and image[i][j + 3] == 0:
                        image[i][j + 1] = 0
                        image[i][j + 2] = 0
                    if image[i + 1][j] == 255 and image[i + 3][j] == 0:
                        image[i + 1][j] = 0
                        image[i + 2][j] = 0
        return image


def show_image(image):
    cv.imshow("Tangram", image)
    cv.waitKey(0)


if __name__ == "__main__":
    pass
