import cv2 as cv
import numpy as np
from elements import *


class TangramSolver:
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
        resize_ratio = pow(280, 2) / (img < 10).sum()  # 280 being the side of the tangram pieces square, divided by the
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

    def draw_shape_on_image(self, img: np.ndarray([], dtype=int), shape: Piece) -> np.ndarray([], dtype=int):
        """
        draws a shape on the image from its vertexes coordinates
        :param img: image we want to draw in
        :param shape: Piece object we want to draw
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

    def accept(self, candidate_image: np.ndarray([], dtype=int)) -> bool:
        """
        Says if the placement of all the pieces is accepted, i.e. the pieces cover at least 97% of the drawing
        :param candidate_image: image with all the tangram pieces placed on the drawing
        :return: True if the tangram pieces cover more than 90% of the drawing, False otherwise
        """
        accept_ratio = .9  # acceptable ratio of covered black pixels
        base_image_black_pixels = (self.image == 0).sum()
        candidate_image_black_pixels = (candidate_image == 0).sum()
        ratio = (candidate_image_black_pixels / base_image_black_pixels)
        return ratio < 1 - accept_ratio

    def reject(self, prev_img: np.ndarray([], dtype=int), candidate_img: np.ndarray([], dtype=int), color: int) -> bool:
        """
        Says if the placement of the new piece is rejected considering two criteria:
        If the new piece is placed over another piece
        Or if less than 97% of the new piece covers the drawing (black pixels)
        :param prev_img: image before placing the new piece
        :param candidate_img: image with the new piece placed
        :return: True if the piece is rejected, False otherwise
        """
        accept_ratio = .95
        covered_black_pixels = (prev_img == 0).sum() - (candidate_img == 0).sum()
        covered_non_black_pixels = (candidate_img == color).sum() - covered_black_pixels
        if covered_black_pixels == 0 and covered_non_black_pixels == 0:
            return True
        non_black_covered_ratio = covered_black_pixels / (covered_non_black_pixels + covered_black_pixels)
        return non_black_covered_ratio < accept_ratio

    def get_next_point(self, corner_list, shape_corners_list, node):
        if node.index_point + 1 < len(corner_list):
            node.position = corner_list[node.index_point]
            node.index_point += 1
            return node, True
        elif node.index_point < ((len(corner_list) + len(shape_corners_list)) - 1):
            node.position = shape_corners_list[node.index_point - len(corner_list)]
            node.index_point += 1
            return node, True
        else:
            node.position = self.corners[0]
            node.index_point = 0
            return node, False

    def change_test_state_shape(self, node, shape_corners_list, increment_rota):

        # if node.piece == None :
        #    return node
        # Try another rotation
        node.rotation = node.rotation + increment_rota
        node.piece.rotate_shape_around_pivot(increment_rota)

        if node.rotation > 360:
            # Try another position
            node.rotation = 0
            node, any_next = self.get_next_point(self.corners, shape_corners_list, node)
            if not any_next:
                # Try another piece
                node.i += 1
                node.rotation = 0
                node.index_point = 0

        return node

    def solve_fast_3(self):
        """
        Solve the tangram puzzle using a fast algorithm
        :return: image with all the tangram pieces placed on the drawing
        """
        available_pieces = [
            LargeTriangle(32),
            LargeTriangle(64),
            Parallelogram(96),
            Square(128),
            MediumTriangle(160),
            SmallTriangle(192),
            SmallTriangle(224),
        ]
        nb_disp_pieces_start = len(available_pieces)
        used_pieces = []
        max_angle = 360
        iteration_rota = 8
        increment_rota = round(max_angle / iteration_rota)
        shape_used_corners = []

        # Initializations
        nodes_list = [Node() for _ in range(0, nb_disp_pieces_start + 1)]
        for i in range(0, len(nodes_list)):
            if i > 0:
                nodes_list[i].prev = nodes_list[i - 1]
            if i < len(nodes_list) - 1:
                nodes_list[i].next = nodes_list[i + 1]

            nodes_list[i].img = self.image.copy()
            nodes_list[i].position = self.corners[0]

        node = nodes_list[1]

        while not self.accept(nodes_list[-1].img) or len(available_pieces) < 0:

            while node.i < len(available_pieces):

                cv.imshow("Tangram", node.img)
                cv.waitKey(0)
                # Get the piece
                node.piece = available_pieces[node.i]
                # Draw the piece
                # Erase the last move
                node.img = node.prev.img.copy()
                #Set the position of the piece to the current analyzed point
                node.piece.position_in_image = node.position
                #Draw the shape
                node.img = self.draw_shape_on_image(node.img, node.piece)

                # Check if piece is rejected
                if self.reject(node.prev.img, node.img, node.piece.color):
                    # print("Piece:" + str(node.piece) + " rejected")
                    # print("Position:" + str(node.position))
                    node = self.change_test_state_shape(node, shape_used_corners, increment_rota)
                else:
                    # Add piece to used pieces and add its corners to the list of usable corners
                    used_pieces.append(node.piece)
                    for point in node.piece.get_points_in_image():
                        shape_used_corners.append(point)

                    # print("Piece:" + str(node.piece) + " placed")
                    # print("Position:" + str(node.position))

                    # Remove piece from available bag
                    available_pieces.pop(node.i)
                    node = node.next
                    node.rotation = 0
                    node.index_point = 0

            if len(available_pieces) > 0:
                node = node.prev
                # If no pieces were ok then remove last piece from used pieces and add it to available bag
                if node.prev:
                    available_pieces.insert(node.i, used_pieces.pop(len(used_pieces) - 1))
                    shape_used_corners = shape_used_corners[:-len(node.piece.points)]
                    node.img = node.prev.img.copy()

                # Update piece position + rotation
                try:
                    node = self.change_test_state_shape(node, shape_used_corners, increment_rota)

                    # print("Nothing fits... getting back to the last piece" + str(node.prev.piece))
                except AttributeError:
                    print(node)


if __name__ == "__main__":
    ai_tangram = TangramSolver('tangram_unsolved.png')

    # Shows the image

    ai_tangram.solve_fast_3()

    cv.imshow("f", ai_tangram.image)
