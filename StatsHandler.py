import json
from utils import draw_piece_in_image
from elements import *
import cv2 as cv
import os


class StatsHandler:
    """
    Used to store all the information on the puzzle solving process

    Attributes:
        image_path:     path of the tangram puzzle to solve
        puzzle_name:    name of the image file, used to store all
        stats:          statistics about solving time and number of corners
        solution_pieces:       pieces of the solution and the
    """
    def __init__(self, image_path: str):
        self.image_path: str = image_path
        self.puzzle_name: str = image_path.split("/")[-1].split('.')[0] if "/" in image_path else image_path.split("\\")[-1].split('.')[0]
        self.stats: dict[str, int] = {
            "time": 0,
            "cornersNumber": 0
        }
        self.solution_pieces: list[dict] =  []

    def save_data(self, solve_duration: float, corners_number: int, used_pieces: list[Piece], puzzle_image: np.ndarray) -> None:
        """
        Saves all the data of the solving process
        :param solve_duration: time that the program took to solve the puzzle
        :param corners_number: number of corners of the original tangram shadow
        :param used_pieces: list of all the pieces used in the solution
        :param puzzle_image: origin image of the puzzle shadow
        """
        self.stats["time"] = solve_duration
        self.stats["cornersNumber"] = corners_number
        self.parse_pieces_solution(used_pieces)
        self.save_stats()
        self.save_solution_steps(used_pieces, puzzle_image)

    def parse_pieces_solution(self, used_pieces: list[Piece]) -> None:
        """
        Parses all the information of the pieces in order to store them as json
        :param used_pieces: list of the pieces used in the solution
        """
        for piece in used_pieces:
            self.solution_pieces.append({
                "type": piece.name,
                "color": piece.color,
                "points": [str(point) for point in piece.get_points_in_image()],
                "rotation": piece.rotation
            })

    def save_stats(self) -> None:
        """
        Saves the solution of the puzzle with some statistics
        """
        final_json = {
            "stats": self.stats,
            "pieces": self.solution_pieces
        }
        os.makedirs(os.path.dirname(self.puzzle_name + "/infos.json"), exist_ok=True)
        with open(self.puzzle_name + "/infos.json", "w") as file:
            json.dump(final_json, file, indent=4)

    def save_solution_steps(self, pieces_used: list[Piece], image: np.ndarray) -> None:
        """
        Saves the 8 images of the tangram solution piece by piece
        :param pieces_used: list of the pieces used to solve the puzzle
        :param image: origin image of the tangram shape
        """
        image_rgb = cv.cvtColor(image, cv.COLOR_GRAY2BGR)
        cv.imwrite(self.puzzle_name + "/step0.png", image_rgb)
        image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        for i in range(len(pieces_used)):
            image_rgb = cv.cvtColor(image_rgb, cv.COLOR_RGB2BGR)
            draw_piece_in_image(image_rgb, pieces_used[i], pieces_used[i].color)
            image_rgb = cv.cvtColor(image_rgb, cv.COLOR_BGR2RGB)
            cv.imwrite(self.puzzle_name + "/step" + str(i + 1) + ".png", image_rgb)
