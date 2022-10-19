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

    def draw_shape_on_image(self, img: np.ndarray([], dtype=int), shape: Shape) -> np.ndarray([], dtype=int):
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

    def accept(self, candidate_image: np.ndarray([], dtype=int)) -> bool:
        """
        Says if the placement of all the pieces is accepted, i.e. the pieces cover at least 97% of the drawing
        :param candidate_image: image with all the tangram pieces placed on the drawing
        :return: True if the tangram pieces cover more than 97% of the drawing, False otherwise
        """
        accept_ratio = .97  # acceptable ratio of covered black pixels
        base_image_black_pixels = (self.image == 0).sum()
        candidate_image_black_pixels = (candidate_image == 0).sum()
        ratio = (candidate_image_black_pixels / base_image_black_pixels)
        return ratio < 1 - accept_ratio

    def reject(self, prev_img: np.ndarray([], dtype=int), candidate_img: np.ndarray([], dtype=int)) -> bool:
        """
        Says if the placement of the new piece is rejected considering two criteria:
        If the new piece is placed over another piece
        Or if less than 95% of the new piece covers the drawing (black pixels)
        :param prev_img: image before placing the new piece
        :param candidate_img: image with the new piece placed
        :return: True if the piece is rejected, False otherwise
        """
        accept_ratio = .95
        covered_non_black_pixels = (prev_img != 0).sum() - (candidate_img != 0).sum()
        covered_black_pixels = (prev_img == 0).sum() - (candidate_img == 0).sum()
        if covered_black_pixels == 0 and covered_non_black_pixels == 0:
            return True
        ratio = covered_black_pixels / (covered_non_black_pixels + covered_black_pixels)
        if ratio < accept_ratio:
            return True
        return False

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
        # Try another rotation
        node.rota = node.rota + increment_rota
        node.piece.rotate_shape_around_pivot(increment_rota)

        if node.rota > 360:
            # Try another position
            node.rota = 0
            node, any_next = self.get_next_point(self.corners, shape_corners_list, node)
            if any_next == False:
                # Try another piece
                node.i += 1
                node.rota = 0
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
        nb_used = 0
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

        while not self.accept(nodes_list[len(nodes_list) - 1].img) and nb_used < len(available_pieces):

            while node.i < len(available_pieces):
                # cv.imshow("dqsf", node.img)
                # cv.waitKey(0)
                # Get the piece
                node.piece = available_pieces[node.i]
                # Draw the piece
                node.img = node.prev.img.copy()
                node.piece.position_in_image = node.position
                node.img = self.draw_shape_on_image(node.img, node.piece)

                # Check if piece is rejected
                if self.reject(node.prev.img, node.img):
                    print("Piece:" + str(node.piece) + " rejected")
                    print("Position:" + str(node.position))
                    node = self.change_test_state_shape(node, shape_used_corners, increment_rota)
                else:
                    # Add piece to used pieces and add its corners to the list of usables corners
                    used_pieces.append(node.piece)
                    for point in node.piece.get_points_in_image():
                        shape_used_corners.append(point)

                    print("Piece:" + str(node.piece) + " placed")
                    print("Position:" + str(node.position))

                    # Remove piece from dispo bag
                    available_pieces.pop(node.i)
                    node = node.next
                    node.rota = 0
                    node.index_point = 0

            if len(available_pieces) > 0:

                node = node.prev
                # If no pieces were ok then remove last piece from used pieces and add it to dispo bag
                if node.prev:
                    available_pieces.insert(node.i, used_pieces.pop(len(used_pieces) - 1))
                    shape_used_corners = shape_used_corners[:-len(node.piece.points)]

                # Update piece position + rotation
                node = self.change_test_state_shape(node, shape_used_corners, increment_rota)

                print("Nothing fits... getting back to the last piece" + str(node.prev.piece))


if __name__ == "__main__":
    ai_tangram = TangramSolver('13.png')

    # Shows the image

    ai_tangram.solve_fast_3()

    cv.imshow("f", ai_tangram.image)
    cv.waitKey(0)

"""

    def solve_very_slowly(self) -> np.ndarray([], dtype=int):
        
        Solves the problem by filling the drawing with the 7 tangram pieces using a backtracking algorithm.
        This method is very slow and will take way too long to work
        :return: the image containing a solution with the tangram pieces covering the drawing
        

        base_pieces = [
            LargeTriangle(32),
            LargeTriangle(64),
            Parallelogram(96),
            Square(128),
            MediumTriangle(160),
            SmallTriangle(192),
            SmallTriangle(224),
        ]
        img_list = [self.image.copy() for _ in range(0, len(base_pieces) + 1)]
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
                    # Reset start position of the new piece
                    a[i] = 0
                    x[i] = start_x
                    y[i] = start_y
        return img_list[len(base_pieces)]
        
        launched at 15:26

    def solve_fast(self):

        base_pieces = [
            LargeTriangle(32),
            LargeTriangle(64),
            Parallelogram(96),
            Square(128),
            MediumTriangle(160),
            SmallTriangle(192),
            SmallTriangle(224),
        ]

        used_pieces = []

        img_list = [self.image.copy() for _ in range(0, len(base_pieces) + 1)]

        current_piece = [Shape() for _ in range(0, len(base_pieces))]
        pieces_used = 0
        # Used to position image
        height, width = img_list[0].shape
        max_angle = 360

        iterationA = 8
        corner_index_point = [0 for _ in range(0, len(base_pieces))]
        corner_nb = len(self.corners)

        pieces_placed_corners = []
        pieces_placed_corners_index = [0 for _ in range(0, len(base_pieces))]

        point_to_test = Point()
        a = [0 for _ in range(0, len(base_pieces))]

        while not self.accept(img_list[pieces_used]):
            i = 0
            # While there is still remaining pieces to try
            while i < len(base_pieces):
                #Set the current piece to the piece to test from the unsused pieces
                current_piece[pieces_used] = base_pieces[i]
                # Copy last image to add the shape over it
                img_list[pieces_used + 1] = img_list[pieces_used].copy()
                # Draw shape on img at pos
                current_piece[pieces_used].rotate_shape_around_pivot(a[pieces_used] * max_angle / iterationA)
                current_piece[pieces_used].position_in_image = self.corners[corner_index_point[pieces_used]]
                img_list[pieces_used + 1] = self.draw_shape_on_image(img_list[pieces_used + 1],
                                                                     current_piece[pieces_used])
                current_piece[pieces_used].rotate_shape_around_pivot(-a[pieces_used] * max_angle / iterationA)


                # If the solution is not ok then go back
                if self.reject(img_list[pieces_used], img_list[pieces_used + 1]):

                    # Reset image
                    img_list[pieces_used + 1] = img_list[pieces_used].copy()

                    # Change rotation of the shape drawing
                    a[pieces_used] = a[pieces_used] + 1
                    if a[pieces_used] >= iterationA:
                        a[pieces_used] = 0
                        corner_index_point[pieces_used] = corner_index_point[pieces_used] + 1

                    # Change position
                    if corner_index_point[pieces_used] < len(self.corners)-1:
                        point_to_test = self.corners[corner_index_point[pieces_used]]
                    elif pieces_placed_corners_index[pieces_used] < len(pieces_placed_corners)-1:
                        point_to_test = pieces_placed_corners[pieces_placed_corners_index[pieces_used]]
                    else:
                        # Change piece
                        i = i + 1
                        # Reset start position of the new piece
                        a[pieces_used] = 0
                        corner_index_point[pieces_used] = 0
                        pieces_placed_corners_index[pieces_used] = 0

                else:
                    cv.imshow("e", img_list[pieces_used + 1])
                    
                    cv.waitKey(0)
                    print(pieces_used)
                    # Else go for the next piece
                    # Place the piece in the used list
                    used_pieces.append(base_pieces.pop(len(used_pieces) - 1))
                    pieces_placed_corners.append(current_piece[pieces_used].get_points_in_image())
                    pieces_used = pieces_used + 1

                    # Reset start position of the new piece
                    a[pieces_used] = 0
                    corner_index_point[pieces_used] = 0
            else:
                # Remove piece placement
                used_pieces.pop(len(used_pieces)-1)
                pieces_used = pieces_used - 1
                #Add piece to unused
                base_pieces.append((current_piece[pieces_used -1 ]))
                # Remove the corners
                pieces_placed_corners = pieces_placed_corners[:len(pieces_placed_corners) - len(current_piece[pieces_used - 1].points)]
                # Continue the placement
                a[pieces_used] = a[pieces_used] + 1

        return img_list[len(base_pieces)]
"""
