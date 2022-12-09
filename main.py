import time

from elements import *
from State import State
from utils import *
from ImageProcessor import ImageProcessor
from utils import show_image
from ShapeComposer import ShapeComposer
from VisualizationHandler import StatsHandler, save_every_solution_steps

if __name__ == "__main__":
    # s_c = ShapeComposer()
    # user_image_file_name = s_c.run()
    user_image_file_name = '6872457878345310086563'  # for development purposes
    image_path = "user_shapes/" + user_image_file_name + ".png"
    image = ImageProcessor(image_path)
    stats_handler = StatsHandler()
    stats_handler.solution["imagePath"] = user_image_file_name
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

    start_time = time.time()
    result = search(root_state)
    end_time = time.time() - start_time
    if result:
        result_image = reconstruct_solution(image.image, result.current_state.used_pieces)
        show_image(result_image)
        stats_handler.stats["time"] = end_time
        stats_handler.stats["nbCorner"] = len(image.corners)
        stats_handler.parse_pieces_solution(result.current_state.used_pieces)
        stats_handler.save_stats_in_file("user_shapes/" + user_image_file_name + ".json")
        save_every_solution_steps(result.current_state.used_pieces, image.image)
