import numpy as np
import cv2 as cv

class TangramSolver:
    def __init__(self, image_path):
        self.image = self.load_image(image_path)
        self.pieces_size = self.get_drawing_area()

    def load_image(self, path):
        # load the image into a 2d np array with 255 as white pixels and 0 as black pixels
        # @param path: path of the image
        # @return a 2d numpy array
        img = cv.imread(path)
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        img = cv.threshold(img, 230, 255, cv.THRESH_BINARY)[1]
        return img

    def get_drawing_area(self):
        nb_black_pixel = (self.image < 200).sum()
        ratio = nb_black_pixel/(len(self.image)*len(self.image[0]))
        # gives the ratio of black pixels over all the pixels
        return ratio


if __name__ == "__main__":
    ai_tangram = TangramSolver('tangram_unsolved.png')
    print(ai_tangram.get_drawing_area())
