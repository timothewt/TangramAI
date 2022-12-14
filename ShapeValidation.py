import cv2 as cv
from settings import *


class ShapeValidation:
    def __init__(self):
        pass

    @staticmethod
    def validate(path_to_image: str) -> bool:
        """
        Tells if the shape is correct, i.e. that no pieces interlap and all the pieces are inside the image_processor
        :param path_to_image: path to the image_processor to validate
        :return: True if it is valid, False otherwise
        """
        image = cv.imread(path_to_image, cv.IMREAD_GRAYSCALE)

        is_left_border_white = (image[:, 0] < 255).any()
        is_right_border_white = (image[:, -1] < 255).any()
        is_top_border_white = (image[0, :] < 255).any()
        is_bottom_border_white = (image[-1, :] < 255).any()

        are_pieces_overflowing_on_image_side = not is_left_border_white and not is_right_border_white and not is_top_border_white and not is_bottom_border_white
        are_pieces_overlapping = (image != 255).sum() >= TANGRAM_AREA * .98

        return are_pieces_overlapping and are_pieces_overflowing_on_image_side


if __name__ == "__main__":
    pass