from random import randint

import pygame as pg
from settings import *
from elements import *


class ShapeComposer:
    def __init__(self) -> None:
        self.screen = pg.display.set_mode(MENU_RES)
        self.pieces = [
            LargeTriangle((8, 189, 100)),
            LargeTriangle((255, 200, 3)),
            MediumTriangle((142, 207, 33)),
            Parallelogram((96, 107, 217)),
            Square((255, 74, 74)),
            SmallTriangle((44, 174, 242)),
            SmallTriangle((251, 140, 50)),
        ]
        pg.display.set_caption("Tangram - Shape Composer")
        self.current_piece = None
        self.font1 = None
        self.font2 = None
        self.font3 = None
        self.output_file_name = ""

    def draw_menu(self) -> None:
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
        for piece in self.pieces:
            points = [(point.x, point.y) for point in piece.get_points_in_image()]
            pg.draw.polygon(self.screen, piece.color, points)

    def get_grid_position(self, x: int, y: int) -> (int, int):
        col = x // settings.GRID_CELL_SIZE
        row = y // settings.GRID_CELL_SIZE
        return int(col), int(row)

    def save_shape(self) -> bool:
        self.screen.fill((255, 255, 255))
        self.draw_pieces()
        pg.display.update()
        file_name = str(randint(1000000000000000000000, 9999999999999999999999)) + ".png"
        pg.image.save(self.screen, "user_shapes/" + file_name)
        return False

    def run(self):
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
                        self.current_piece.rotate_shape_around_pivot(PIECE_ROTATION)
                    if event.key == pg.K_f and self.current_piece.name == "Parallelogram":
                        self.current_piece.flip()
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    self.save_shape()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.current_piece = None
            # Selecting the current piece
            keys = pg.key.get_pressed()
            if keys[pg.K_0]:
                self.current_piece = None
            if keys[pg.K_1]:
                self.current_piece = self.pieces[0]
            elif keys[pg.K_2]:
                self.current_piece = self.pieces[1]
            elif keys[pg.K_3]:
                self.current_piece = self.pieces[2]
            elif keys[pg.K_4]:
                self.current_piece = self.pieces[3]
            elif keys[pg.K_5]:
                self.current_piece = self.pieces[4]
            elif keys[pg.K_6]:
                self.current_piece = self.pieces[5]
            elif keys[pg.K_7]:
                self.current_piece = self.pieces[6]

            # Moving the piece to the mouse cursor
            if self.current_piece is not None:
                mouse_pos = pg.mouse.get_pos()
                position = [pos * settings.GRID_CELL_SIZE for pos in self.get_grid_position(mouse_pos[0], mouse_pos[1])]
                self.current_piece.position_in_image = Point(position[0], position[1])

            self.draw_shape_composer()
