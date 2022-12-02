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

    def draw_pieces(self) -> None:
        self.screen.fill((230, 230, 230))
        [pg.draw.circle(self.screen, (0, 0, 0), (i * GRID_CELL_SIZE, j * GRID_CELL_SIZE), 1) for j in range(GRID_H + 1) for i in range(GRID_W + 1)]
        for piece in self.pieces:
            points = [(point.x, point.y) for point in piece.get_points_in_image()]
            pg.draw.polygon(self.screen, piece.color, points)
        current_piece_name = self.current_piece.name if self.current_piece is not None else "None"
        current_piece_text = self.font1.render("Current piece: " + current_piece_name, True, (0, 0, 0))
        self.screen.blit(current_piece_text, (MENU_WIDTH - current_piece_text.get_width() - 5, 5))
        controls_text = self.font2.render("[1][2]: LTriangle [3]: MTriangle [4]: Parallelogram [5]: Square [6][7]: STriangle [R]: Rotate", True, (0, 0, 0))
        pg.draw.rect(self.screen, (255, 255, 255), pg.Rect(0, MENU_HEIGHT - controls_text.get_height() - 10, MENU_WIDTH, controls_text.get_height() + 10))
        self.screen.blit(controls_text, (5, MENU_HEIGHT - controls_text.get_height() - 5))
        pg.display.update()

    def get_grid_position(self, x: int, y: int) -> (int, int):
        col = x // settings.GRID_CELL_SIZE
        row = y // settings.GRID_CELL_SIZE
        return int(col), int(row)

    def run(self):
        pg.init()
        self.font1 = pg.font.SysFont('verdana', 25, True)
        self.font2 = pg.font.SysFont('verdana', 15, True)
        self.draw_pieces()
        while True:
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

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN and self.current_piece is not None:
                    if event.key == pg.K_r:
                        self.current_piece.rotate_shape_around_pivot(90)
                    elif event.key == pg.K_f and self.current_piece.name == "Parallelogram":
                        self.current_piece.flip()
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.current_piece = None

            self.draw_pieces()
