import cv2 as cv
from elements import *
from State import State, search
from model import ImageProcessor


if __name__ == "__main__":
    image = ImageProcessor('13.png')
    cv.imshow("Tangram", image.image)
    cv.waitKey(0)
    av_pieces = [
        LargeTriangle(32),
        LargeTriangle(64),
        MediumTriangle(160),
        Parallelogram(96),
        Square(128),
        SmallTriangle(192),
        SmallTriangle(224),
    ]

    root_state = State(av_pieces, image.image, image.corners)
    result = search(root_state)
    cv.imshow("Tangram", result.current_state.image)
    cv.waitKey(0)
