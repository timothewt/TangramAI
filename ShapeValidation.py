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
        height, width = image.shape

        cond_border_left = (image[:, 0] < 255).any()
        cond_border_right = (image[:, -1] < 255).any()
        cond_border_top = (image[0, :] < 255).any()
        cond_border_bottom = (image[-1, :] < 255).any()

        cond_pieces_in_image = not cond_border_left and not cond_border_right and not cond_border_top and not cond_border_bottom
        condition_no_pieces_overlaping = (image != 255).sum() >= TANGRAM_AREA * .98




        #cond_border_image_white
        return condition_no_pieces_overlaping and cond_pieces_in_image


if __name__ == "__main__":
    pass