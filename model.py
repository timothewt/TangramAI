import cv2 as cv
from elements import *


class ImageProcessor:
    def __init__(self, image_path: str) -> None:
        self.corners = []
        self.image = self.load_image(image_path)  # image of the shape we want to reproduce with the tangram pieces

    def load_image(self, path: str) -> np.ndarray([], dtype=int):
        """
        loads the image into a 2d np array with 255 as white pixels and 0 as black pixels, resizes it and turns it
        into black and white
        :param path: path of the image
        :return: a 2d numpy array of the resized b&w image
        """
        img = cv.imread(path)
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        self.corners = self.get_corners_coordinates(gray_img.copy())

        b_w_img = self.to_b_w(gray_img)
        resized_img = self.resize_image(b_w_img)  # resizes the image for the tangram pieces to be the good size
        resized_img_b_w = self.to_b_w(resized_img)  # to b&w to eliminate gray pixels
        return resized_img_b_w

    def get_corners_coordinates(self, img: np.ndarray([], dtype=int)):
        """
        Gives the coordinates of all the corners of the shape to draw using the Harris corner detection algorithm
        :param img: image from which we want the corners
        :return: a list of the corners
        """
        dst = cv.cornerHarris(img, 5, 3, 0.04)
        ret, dst = cv.threshold(dst, 0.1 * dst.max(), 255, 0)
        dst = np.uint8(dst)
        ret, labels, stats, centroids = cv.connectedComponentsWithStats(dst)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)
        corners = cv.cornerSubPix(img, np.float32(centroids), (5, 5), (-1, -1), criteria)
        return corners

    def resize_image(self, img: np.ndarray([], dtype=int)) -> np.ndarray([], dtype=int):
        """
        resizes the image for the area of the drawing to match the area of all the tangram pieces, which is 280*280
        :param img: image we want to resize
        :return: the np array of the black and white resized image
        """
        resized_image = img.copy()
        (h, w) = img.shape[:2]
        resize_ratio = pow(270, 2) / (img == 0).sum()  # 280 being the side of the tangram pieces square, divided by the
        # number of black pixel on the image which represent the area of the goal shape
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
            resized_corners.append(Point(self.corners[i][0] * resize_ratio, self.corners[i][1] * resize_ratio))
        self.corners = resized_corners

    def to_b_w(self, img: np.ndarray([], dtype=int)) -> np.ndarray([], dtype=int):
        """
        turns a picture to black and white
        :param img: image we want to convert to b&w
        :return: the np array of the black (0) and white (255) pixels
        """
        b_w_image = img.copy()
        b_w_image = cv.threshold(b_w_image, 30, 255, cv.THRESH_BINARY)[1]
        return b_w_image


if __name__ == "__main__":
    pass
