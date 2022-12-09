import json

import jsonify as jsonify
from utils import draw_piece_in_image
from elements import *
import cv2 as cv

def save_every_solution_steps(pieces_used, image):
    image_rgb = cv.cvtColor(image, cv.COLOR_GRAY2BGR)

    cv.imwrite("step0.png", image_rgb)
    image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    for i in range(len(pieces_used)):
        image_rgb = cv.cvtColor(image_rgb, cv.COLOR_RGB2BGR)
        curr_image_path = "step" + str(i+1) + ".png"
        piece_used = pieces_used[i]
        draw_piece_in_image(image_rgb, piece_used, piece_used.color)
        image_rgb = cv.cvtColor(image_rgb, cv.COLOR_BGR2RGB)
        cv.imwrite(curr_image_path, image_rgb)



class StatsHandler:
    def __init__(self):
        self.stats = {
            "time": 0,
            "nbCorner": 0
        }
        self.solution = {
            "pieces": [
            ],
            "imagePath":""
        }

    def save_stats_in_file(self, file_name="infos.json"):
        final_json = {
            "stats": self.stats,
            "solution": self.solution
        }
        with open(file_name, "w") as file:
            #Write stats in json file
            json.dump(final_json, file, indent=4)

    def parse_pieces_solution(self, used_pieces):
        for piece in used_pieces:
            self.solution["pieces"].append({
                "type": piece.name,
                "color": piece.color,
                "points": [str(point) for point in piece.get_points_in_image()],
                "rotation": piece.rotation
            })





