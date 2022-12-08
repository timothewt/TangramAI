from elements import *
from State import State
from utils import *
from ImageProcessor import ImageProcessor
from utils import show_image
from ShapeComposer import ShapeComposer


if __name__ == "__main__":
    # s_c = ShapeComposer()
    # user_image_file_name = s_c.run()
    user_image_file_name = '1466019767509923539332.png'  # for development purposes

    image = ImageProcessor("user_shapes/" + user_image_file_name)

    available_pieces = [
        LargeTriangle((8, 189, 100)),
        LargeTriangle((255, 200, 3)),
        Parallelogram((96, 107, 217)),
        Square((255, 74, 74)),
        MediumTriangle((142, 207, 33)),
        SmallTriangle((44, 174, 242)),
        SmallTriangle((251, 140, 50)),
    ]

    root_state = State(available_pieces, image.image, image.corners)
    result = search(root_state)
    if result:
        result_image = reconstruct_solution(image.image, result.current_state.used_pieces)
        show_image(result_image)
