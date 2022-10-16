import cv2 as cv
from elements import *
import time


class TangramSolver:
    def __init__(self, image_path):
        self.image = self.load_image(image_path)  # image of the shape we want to reproduce with the tangram pieces

    def load_image(self, path):
        """
        loads the image into a 2d np array with 255 as white pixels and 0 as black pixels, resizes it and turns it
        into black and white
        :param path: path of the image
        :return: a 2d numpy array of the resized b&w image
        """
        img = cv.imread(path)
        cv.imshow("dqsf", img)
        cv.waitKey(0)
        gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        cv.imshow("dqsf", gray_img)
        cv.waitKey(0)
        b_w_img = self.to_b_w(gray_img)
        cv.imshow("dqsf", b_w_img)
        cv.waitKey(0)
        resized_img = self.resize_image(b_w_img)
        cv.imshow("dqsf", resized_img)
        cv.waitKey(0)
        resized_img_b_w = self.to_b_w(resized_img)  # to b&w to eliminate gray pixels
        cv.imshow("dqsf", resized_img_b_w)
        cv.waitKey(0)
        return resized_img_b_w

    def resize_image(self, img):
        """
        resizes the image for the area of the drawing to match the area of all the tangram pieces, which is 360*360
        :param img: image we want to resize
        :return: the np array of the black and white resized image
        """
        resized_image = img.copy()
        (h, w) = img.shape[:2]
        resize_ratio = pow(280, 2) / (img < 10).sum()  # 280 being the side of the tangram pieces square, divided by the
        # number of black pixel on the image which represent the area of the goal shape
        (new_h, new_w) = (int(resize_ratio * h), int(resize_ratio * w))
        resized_image = cv.resize(resized_image, (new_w, new_h), interpolation=cv.INTER_CUBIC)
        return resized_image

    def to_b_w(self, img):
        """
        turns a picture to black and white
        :param img: image we want to convert to b&w
        :return: the np array of the black (0) and white (255) pixels
        """
        b_w_image = img.copy()
        b_w_image = cv.threshold(b_w_image, 30, 255, cv.THRESH_BINARY)[1]
        return b_w_image

    def draw_shape_on_image(self, img, shape):
        """
        draws a shape on the image from its vertexes coordinates
        :param img: image we want to draw in
        :param shape: Shape object we want to draw
        :return the new matrix of the image with the shape in it
        """
        new_img = img.copy()
        points = []
        for point in shape.get_points_in_image():
            points.append([point.x, point.y])
        pts = np.array(points, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv.fillPoly(new_img, [pts], shape.color)
        return new_img

    def solve_very_slowly(self):

        base_pieces = [
            LargeTriangle(32),
            LargeTriangle(64),
            Parallelogram(96),
            Square(128),
            MediumTriangle(160),
            SmallTriangle(192),
            SmallTriangle(224),
        ]
        img_list = [self.image.copy() for _ in range(0, len(base_pieces)+1)]
        i = 0

        # Used to position image
        height, width = img_list[0].shape
        max_angle = 360
        iterationX = 50
        iterationY = 50
        iterationA = 8

        start_x = 5
        start_y = 5

        end_x = 45
        end_y = 45

        x = [start_x for _ in range(0, len(base_pieces))]
        y = [start_y for _ in range(0, len(base_pieces))]
        a = [0 for _ in range(0, len(base_pieces))]

        while not self.accept(img_list[i]) and 6 >= i >= 0:
            i = 0
            while i < len(base_pieces):
                # Copy last image to add the shape over it
                img_list[i + 1] = img_list[i].copy()
                # Draw shape on img at pos
                base_pieces[i].rotate_shape_around_pivot(a[i] * max_angle / iterationA)
                base_pieces[i].position_in_image = Point(x[i] * width / iterationX, y[i] * height / iterationY)
                img_list[i + 1] = self.draw_shape_on_image(img_list[i + 1], base_pieces[i])
                base_pieces[i].rotate_shape_around_pivot(-a[i] * max_angle / iterationA)

                # If the solution is not ok then go back
                if self.reject(img_list[i], img_list[i + 1], base_pieces[i].color):

                    # Reset image
                    img_list[i + 1] = img_list[i].copy()

                    # Change position of the shape drawing
                    a[i] = a[i] + 1
                    if a[i] >= iterationA:
                        a[i] = 0
                        x[i] = x[i] + 1
                    if x[i] >= end_x:
                        x[i] = start_x
                        y[i] = y[i] + 1
                    if y[i] >= end_y:
                        i = i - 1
                        a[i] = a[i] + 1
                elif i != 6:  # Else go for the next piece

                    cv.imshow("dqsf", img_list[i + 1])
                    cv.waitKey(0)
                    i = i + 1
                    #Reset start position of the new piece
                    a[i] = 0
                    x[i] = start_x
                    y[i] = start_y
        return img_list[len(base_pieces)]

    def accept(self, candidate_image):
        """
        Says if the placement of all the pieces is accepted, i.e. the pieces cover at least 90% of the drawing
        :param candidate_image: image with all the tangram pieces placed on the drawing
        :return: True if the tangram pieces cover more than 90% of the drawing, False otherwise
        """
        accept_ratio = .97  # acceptable ratio of covered black pixels
        base_image_black_pixels = (self.image == 0).sum()
        candidate_image_black_pixels = (candidate_image == 0).sum()
        ratio = (candidate_image_black_pixels / base_image_black_pixels)
        return ratio < 1 - accept_ratio

    def reject(self, prev_img, candidate_img, new_color):
        """
        Says if the placement of the new piece is rejected considering two criteria:
        If the new piece is placed over another piece
        Or if less than 90% of the new piece covers the drawing (black pixels)
        :param prev_img: image before placing the new piece
        :param candidate_img: image with the new piece placed
        :param new_color: color of the new piece
        :return: True if the piece is rejected, False otherwise
        """
        # if new piece is placed on top of another
        new_img_positions = (candidate_img == new_color)
        for new_pixel in np.argwhere(new_img_positions):
            if prev_img[new_pixel[0], new_pixel[1]] != 255 and prev_img[new_pixel[0], new_pixel[1]] != 0:
                return True
        accept_ratio = .97
        covered_white_pixels = (prev_img == 255).sum() - (candidate_img == 255).sum()
        covered_black_pixels = (prev_img == 0).sum() - (candidate_img == 0).sum()
        if covered_black_pixels == 0 and covered_white_pixels == 0:
            return True
        ratio = covered_black_pixels / (covered_white_pixels + covered_black_pixels)
        if ratio < accept_ratio:
            return True
        return False


if __name__ == "__main__":
    ai_tangram = TangramSolver('13.png')

    # Shows the image

    im2, contours = cv.findContours(ai_tangram.image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    #cv.drawContours(ai_tangram.image, contours, 3, 127, 3)
    for point in im2[1]:
        ai_tangram.image = cv.circle(ai_tangram.image, point[0], radius=0, color=127, thickness=5)
    cv.imshow("dqsf", ai_tangram.image)
    cv.waitKey(0)
