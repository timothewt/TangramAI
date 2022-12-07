from math import floor, sqrt, ceil
import cv2 as cv
from settings import *
from elements import *


class ImageProcessor:
    def __init__(self, path_to_image: str = None) -> None:
        self.corners = []
        self.image = None
        if path_to_image is not None:
            self.image = self.load_image(path_to_image)  # image of the shape we want to reproduce with the tangram pieces

    def load_image(self, path_to_image: str) -> np.ndarray([], dtype=int):
        """
        loads the image into a 2d np array with 255 as white pixels and 0 as black pixels, resizes it and turns it
        into black and white again
        :param path_to_image: path of the image
        :return: a 2d numpy array of the resized b&w image
        """
        image = cv.imread(path_to_image, cv.IMREAD_GRAYSCALE)

        black_and_white_image = self.image_to_black_and_white(image)
        resized_image = self.resize_image(black_and_white_image)  # resizes the image for the tangram pieces to be the good size
        resized_black_and_white_image = self.image_to_black_and_white(resized_image)  # to b&w to eliminate gray pixels
        filled_image = self.fill_shape(resized_black_and_white_image)  # in case of small holes between very close pieces
        self.corners = self.get_corners(filled_image.copy())
        self.draw_corners(filled_image)
        return filled_image

    def draw_corners(self, image):
        for corner in self.corners:
            cv.circle(image, (corner.x, corner.y),3,128, -1)

    def get_corners(self, image: np.ndarray) -> list[Corner]:
        """
        Gives the coordinates of all the corners of the shape, and all its edges
        :param image: image from which we want the corners and edges
        :return: a list of the corners, which also has the edges in it
        """
        contours = cv.findContours(image, 1, 2)[0]
        corners = []
        for contour in contours[:-1]:  # last contour is the contour of the image
            if cv.contourArea(contour) < MIN_SUB_PUZZLE_AREA:
                continue

            sub_puzzle_corners = [Corner(contour[0][0][0], contour[0][0][1])]
            contour_length = len(contour)

            for i in range(1, contour_length):  # gets all the corners
                corner = Corner(contour[i][0][0], contour[i][0][1])
                if not corner.close_to(sub_puzzle_corners[-1], MIN_DIST_BETWEEN_TWO_CORNERS):
                    sub_puzzle_corners.append(corner)
                else:
                    # Calculate new corner position
                    sub_puzzle_corners[-1] = Corner(int((sub_puzzle_corners[-1].x + corner.x) / 2),
                                                    int((sub_puzzle_corners[-1].y + corner.y) / 2))

            corners_number = len(sub_puzzle_corners)
            for i in range(corners_number):  # link them with edges
                corner = sub_puzzle_corners[i - 1]
                previous_corner = sub_puzzle_corners[i]
                next_corner = sub_puzzle_corners[(i + 1) % corners_number]

                corner.first_edge = Edge(corner, previous_corner)
                corner.second_edge = Edge(corner, next_corner)

                corner.compute_angle_between_edges()

            corners.extend(sub_puzzle_corners)
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