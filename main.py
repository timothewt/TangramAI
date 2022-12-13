import time
from elements import *
from State import State
from utils import *
from ImageProcessor import ImageProcessor
from utils import show_image
from ShapeComposer import ShapeComposer
from VisualizationHandler import StatsHandler, save_every_solution_steps
import argparse

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='Tangram solver')
    parser.add_argument('--imagePath', type=str, default='', help='Path to the image to solve')
    parser.add_argument('--saveData', type=bool, default=False, help='Path to save the data relative to the solving process')
    parser.add_argument('--createFig', type=bool, default=False, help='Option to create a figure of using the editor')

    args = parser.parse_args()
    user_image_path =''

    if args.createFig:
        editor = ShapeComposer()
        user_image_path = editor.run()
        print("Image path: ", user_image_path)
    elif args.imagePath != '' :
        user_image_path = args.imagePath

    #Solve the tangram
    image = ImageProcessor(user_image_path)
    stats_handler = StatsHandler()
    stats_handler.solution["imagePath"] = user_image_path
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

    #If the solution is found
    if result:
        result_image = reconstruct_solution(image.image, result.current_state.used_pieces)
        show_image(result_image)

        if args.saveData:
            stats_handler.stats["time"] = end_time
            stats_handler.stats["nbCorner"] = len(image.corners)
            stats_handler.parse_pieces_solution(result.current_state.used_pieces)
            stats_handler.save_stats_in_file(user_image_path.split('.')[0] + str('.json'))
        #save_every_solution_steps(result.current_state.used_pieces, image.image)
