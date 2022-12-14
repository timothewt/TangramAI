from random import randint
import pygame as pg
import os
from tkinter import messagebox
from ShapeValidation import ShapeValidation
from elements import *
from settings import *


class ShapeComposer:
    """
    Menu of the program. Makes the user compose its own tangram shape. It will later be solved by the AI.

    Attributes:
        screen:             PyGame surface on which we draw the menu and composer
        pieces:             all the tangram pieces
        current_piece:      the piece that the user is currently placing
        font1:              PyGame font for the title
        font2:              PyGame font for the subtitles
        font3:              PyGame font for the controls
        output_file_name:   name of the image_processor file which is the valid tangram shape
        shape_validation:   shape validation object to validate the shape submitted by the user
    """
    def __init__(self) -> None:
        self.screen = pg.display.set_mode(MENU_RES)
        pg.display.set_caption("Tangram - Shape Composer")
        self.pieces = [
            LargeTriangle((8, 189, 100)),
            LargeTriangle((255, 200, 3)),
            MediumTriangle((142, 207, 33)),
            Parallelogram((96, 107, 217)),
            Square((255, 74, 74)),
            SmallTriangle((44, 174, 242)),
            SmallTriangle((251, 140, 50)),
        ]
        self.randomize_pieces_positions()
        self.current_piece = None
        self.font1 = None
        self.font2 = None
        self.font3 = None
        self.output_file_name = ""
        self.shape_validation = ShapeValidation()

    def randomize_pieces_positions(self) -> None:
        """
        Randomises the pieces position and rotation
        """
        for piece in self.pieces:
            piece.position_in_image = self.random_coordinates(piece.side_length)
            piece.rotate_shape_around_its_pivot_point(PIECE_ROTATION * randint(0, 8))

    def random_coordinates(self, piece_side_length) -> Point:
        """
        Gives random coordinates for a piece
        :param piece_side_length: side length of the piece
        :return a random point in the window
        """
        grid_x, grid_y = self.get_grid_position(randint(100, int(MENU_WIDTH - piece_side_length)), randint(100, int(MENU_HEIGHT - piece_side_length)))
        return Point(grid_x * GRID_CELL_SIZE, grid_y * GRID_CELL_SIZE)

    def draw_menu(self) -> None:
        """
        Draws the main menu of the program presenting the controls
        """
        self.screen.fill((230, 230, 230))
        title_text = self.font1.render("Tangram AI", True, (255, 255, 255), (0, 0, 0))
        self.font1.set_italic(True)
        sub_title_text = self.font1.render("Solving Tangram puzzles with AI", True, (0, 0, 0))
        self.font1.set_italic(False)
        controls_text1 = self.font3.render("Use number keys (1-7) to select the piece you want to move, and the left-click to place it.", True, (0, 0, 0))
        controls_text2 = self.font3.render("Use the R key to rotate them and the F key to flip the parallelogram (mirrored shape).", True, (0, 0, 0))
        controls_text3 = self.font3.render("When finished, press the Return key to validate the shape.", True, (0, 0, 0))
        self.font2.set_italic(True)
        continue_text = self.font2.render("Press any key to continue", True, (0, 0, 0), (220, 220, 220))
        self.font2.set_italic(False)
        self.screen.blit(title_text, ((MENU_WIDTH - title_text.get_width()) // 2, 150))
        self.screen.blit(sub_title_text, ((MENU_WIDTH - sub_title_text.get_width()) // 2, 200))
        self.screen.blit(controls_text1, ((MENU_WIDTH - controls_text1.get_width()) // 2, 300))
        self.screen.blit(controls_text2, ((MENU_WIDTH - controls_text2.get_width()) // 2, 320))
        self.screen.blit(controls_text3, ((MENU_WIDTH - controls_text3.get_width()) // 2, 340))
        self.screen.blit(continue_text, ((MENU_WIDTH - continue_text.get_width()) // 2, 450))

        pg.display.update()

    def draw_shape_composer(self) -> None:
        """
        Draws the shape composer with some controls, the grid, the pieces and the current piece
        """
        self.screen.fill((230, 230, 230))
        [pg.draw.circle(self.screen, (0, 0, 0), (i * GRID_CELL_SIZE, j * GRID_CELL_SIZE), 1) for j in range(GRID_H + 1) for i in range(GRID_W + 1)]
        self.draw_pieces()
        current_piece_name = self.current_piece.name if self.current_piece is not None else "None"
        current_piece_text = self.font2.render("Current piece: " + current_piece_name, True, (0, 0, 0))
        self.screen.blit(current_piece_text, (MENU_WIDTH - current_piece_text.get_width() - 5, 5))
        controls_text = self.font3.render("[1][2]: LTriangle [3]: MTriangle [4]: Parallelogram [5]: Square [6][7]: STriangle [R]: Rotate", True, (0, 0, 0))
        pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(0, MENU_HEIGHT - controls_text.get_height() - 10, MENU_WIDTH, controls_text.get_height() + 10))
        self.screen.blit(controls_text, (5, MENU_HEIGHT - controls_text.get_height() - 5))
        pg.display.update()

    def draw_pieces(self) -> None:
        """
        Draws all the pieces of the window
        """
        for piece in self.pieces:
            points = [(point.x, point.y) for point in piece.get_points_in_image()]
            pg.draw.polygon(self.screen, piece.color, points)

    @staticmethod
    def get_grid_position(x: int, y: int) -> (int, int):
        """
        Gives the grid equivalent of a position for a piece, in order to have fixed coordinates for the pieces
        :param x: x position
        :param y: y position
        :return: the column and row in the grid
        """
        col = x // settings.GRID_CELL_SIZE
        row = y // settings.GRID_CELL_SIZE
        return int(col), int(row)

    def save_shape(self) -> bool:
        """
        Saves the image_processor of the shape if it was validated by the program
        :return: True if it has been validated, False if it is not valid
        """
        # return True  # for development purpose
        self.screen.fill((255, 255, 255))
        self.draw_pieces()
        pg.display.update()
        file_name = str(randint(10 ** 21, 10 ** 22 - 1)) + ".png"
        pg.image.save(self.screen, "user_shapes/" + file_name)
        self.output_file_name = file_name
        if self.shape_validation.validate("user_shapes/" + file_name):
            return True
        return False

    def run(self) -> str:
        """
        Main loop of the user interface. Shows the menu then the composer. Once the shape has been validated, ends the loop.
        :return the name of the image_processor file with the tangram shape
        """
        pg.init()
        self.font1 = pg.font.SysFont('verdana', 40, True)
        self.font2 = pg.font.SysFont('verdana', 25, True)
        self.font3 = pg.font.SysFont('verdana', 15, True)
        self.draw_menu()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN:
                    break
            else:
                continue
            break
        self.draw_shape_composer()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN and self.current_piece is not None:
                    if event.key == pg.K_r:
                        self.current_piece.rotate_shape_around_its_pivot_point(PIECE_ROTATION)
                    if event.key == pg.K_n:
                        self.current_piece.shift_corners()
                    if event.key == pg.K_f and self.current_piece.name == "Parallelogram":
                        self.current_piece.flip()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.current_piece = None

            # Selecting the current piece
            keys = pg.key.get_pressed()
            if keys[pg.K_0]:
                self.current_piece = None
            for i in range(7):
                if keys[pg.K_1 + i]:
                    self.current_piece = self.pieces[i]
            # To save the shape
            if keys[pg.K_RETURN]:
                if self.save_shape():
                    messagebox.showinfo("Shape valid", "The shape has been validated, now the program will solve it.")
                    break
                else:
                    messagebox.showwarning("Pieces misplacement", "Please do not place pieces on top of each others.")
                    os.remove("user_shapes/" + self.output_file_name)
            elif keys[pg.K_TAB]:
                self.randomize_pieces_positions()

            # Moving the piece to the mouse cursor
            if self.current_piece is not None:
                mouse_pos = pg.mouse.get_pos()
                position = [pos * settings.GRID_CELL_SIZE for pos in self.get_grid_position(mouse_pos[0], mouse_pos[1])]
                self.current_piece.position_in_image = Point(position[0], position[1])

            self.draw_shape_composer()

        return "user_shapes/" + self.output_file_name
