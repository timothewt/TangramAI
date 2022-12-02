from ShapeValidation import ShapeValidation
from elements import *
from State import State, search
from ImageProcessor import ImageProcessor, show_image
from ShapeComposer import ShapeComposer


if __name__ == "__main__":
    s_c = ShapeComposer()
    user_image_file_name = s_c.run()
    user_image_file_name = '3282301980754824700651.png'  # for debug purposes

    image = ImageProcessor('user_shapes/' + user_image_file_name)
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