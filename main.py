from elements import *
from State import State, search
from ImageProcessor import ImageProcessor, show_image
from ShapeComposer import ShapeComposer


if __name__ == "__main__":
    # s_c = ShapeComposer()
    # user_image_file_name = s_c.run()
    user_image_file_name = '3282301980754824700651.png'  # for development purposes

    image = ImageProcessor('assets/13.png')
    show_image(image.image)

    edges, corners = image.get_edges_and_corners(image.image)
    print(len(edges))

    available_pieces = [
        LargeTriangle((8, 189, 100)),
        LargeTriangle((255, 200, 3)),
        MediumTriangle((142, 207, 33)),
        Parallelogram((96, 107, 217)),
        Square((255, 74, 74)),
        SmallTriangle((44, 174, 242)),
        SmallTriangle((251, 140, 50)),
    ]

    root_state = State(available_pieces, image.image, image.corners)
    result = search(root_state)
    if result:
        show_image(result.current_state.image)
