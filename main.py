from ShapeValidation import ShapeValidation
from elements import *
from State import State, search
from ImageProcessor import ImageProcessor, show_image
from ShapeComposer import ShapeComposer


if __name__ == "__main__":
    """
    image = ImageProcessor('assets/13.png')
    show_image(image.image)
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
    if result:
        show_image(result.current_state.image)
    """
    s_c = ShapeComposer()
    s_c.run()

