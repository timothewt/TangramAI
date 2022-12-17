import time
from TangramSolver import TangramSolver
from utils import *
from ImageProcessor import ImageProcessor
from ShapeComposer import ShapeComposer
from StatsHandler import StatsHandler
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Tangram solver')
    parser.add_argument('--imagePath', type=str, default=None, help='Path to the image_processor to solve')
    parser.add_argument('--saveData', type=bool, default=False, help='Path to save the data relative to the solving process')
    parser.add_argument('--createFig', type=bool, default=True, help='Option to create a figure of using the editor')

    args = parser.parse_args()
    image_path = ''

    if args.imagePath is not None:
        image_path = args.imagePath
    elif args.createFig:
        editor = ShapeComposer()
        image_path = editor.run()

    image_processor = ImageProcessor(image_path)
    stats_handler = StatsHandler(image_path)

    start_time = time.time()
    solver = TangramSolver(image_processor.image)
    solve_duration = time.time() - start_time

    if solver.solution_node is not None:
        if args.saveData:
            stats_handler.save_data(solve_duration, len(image_processor.corners), solver.solution_node.current_state.used_pieces, image_processor.image)

        result_image = place_all_pieces_on_image(image_processor.image, solver.solution_node.current_state.used_pieces)
        show_image(result_image)
