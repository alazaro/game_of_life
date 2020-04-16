import random
import re
from typing import Sequence, Tuple

import pygame
from pygame import locals as gl

Point = Tuple[int, int]
BoolMatrix = Sequence[Sequence[bool]]


class Config:
    board_size = 100, 100
    cell_size = 5, 5
    on_color = pygame.Color(255, 255, 255)
    off_color = pygame.Color(50, 50, 50)
    max_fps = 0  # 0 => No limit
    seed = None
    alive_cells_at_start = 0.6  # 0 to 1
    title = 'Game of Life'
    rules = 'b3s23'  # https://catagolue.appspot.com/rules


class RenderDirty(pygame.sprite.RenderPlain):
    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sprites:
            if spr.dirty:
                self.spritedict[spr] = surface_blit(spr.image, spr.rect)


class Board:
    cells: BoolMatrix

    def __init__(self):
        random.seed(Config.seed)
        self.cells = [
            random.choices(
                (True, False),
                cum_weights=(Config.alive_cells_at_start, 1),
                k=Config.board_size[1]
            )
            for w in range(Config.board_size[0])
        ]
        self.rule_born, self.rule_survive = self.parse_rules()

    def parse_rules(self):
        if match := re.findall(
            r'B([0-9]*)\/?S([0-9]*)', Config.rules, flags=re.I
        ):
            return (tuple(int(y) for y in list(x)) for x in match[0])

    def next_step(self):
        next_cells = []
        for x, column in enumerate(self.cells):
            next_cells.append([])
            for y in range(Config.board_size[1]):
                next_cells[x].append(self.get_next_status(x, y))
        self.cells = next_cells

    def get_next_status(self, x: int, y: int) -> bool:
        alive_neighbors = len(self.get_alive_neighbors(x, y))
        status = self.cells[x][y]
        return (
            not status and alive_neighbors in self.rule_born
            or status and alive_neighbors in self.rule_survive
        ) or False

    def get_alive_neighbors(self, x: int, y: int) -> Sequence[Point]:
        neighbors = self.get_neighbors(x, y)
        board_width = Config.board_size[0]
        board_height = Config.board_size[1]
        alive = []
        for x_, y_ in neighbors:
            # Connect with the opposite edge
            if x_ >= board_width:
                x_ = 0
            if y_ >= board_height:
                y_ = 0
            if self.cells[x_][y_]:
                alive.append((x_, y_))
        return alive

    def get_neighbors(self, x: int, y: int) -> Sequence[Point]:
        x_plus_one = x + 1
        x_minus_one = x - 1
        y_plus_one = y + 1
        y_minus_one = y - 1
        return (
            (x_minus_one, y_minus_one),
            (x_plus_one, y_minus_one),
            (x_minus_one, y_plus_one),
            (x_plus_one, y_plus_one),
            (x, y_minus_one),
            (x, y_plus_one),
            (x_minus_one, y),
            (x_plus_one, y),
        )

    def print(self):
        for col in self.cells:
            print(('| {} |' * len(col)).format(*col))

    def generate_cells(self) -> Sequence['GameCell']:
        return [
            GameCell(x, y, status, self)
            for y, columns in enumerate(self.cells)
            for x, status in enumerate(columns)
        ]


class GameCell(pygame.sprite.DirtySprite):
    def __init__(self, x: int, y: int, status: bool, board: Board):
        super().__init__()
        self.image = pygame.Surface(Config.cell_size)
        self.rect = self.image.get_rect()
        self.rect.x = x * Config.cell_size[0]
        self.rect.y = y * Config.cell_size[1]
        self.pos = x, y
        self.board = board
        self.status = status

    def update_color(self, status: bool):
        if status:
            self.image.fill(Config.on_color)
        else:
            self.image.fill(Config.off_color)

    def update(self):
        next_status = self.board.cells[self.pos[0]][self.pos[1]]
        if next_status != self.status:
            self.dirty = 1
            self.update_color(next_status)
        else:
            self.dirty = 0
        self.status = next_status


def __main__():
    pygame.init()
    board = Board()
    running = True
    screen = pygame.display.set_mode((
        Config.board_size[0] * Config.cell_size[0],
        Config.board_size[1] * Config.cell_size[1]
    ))
    pygame.display.set_caption(Config.title)
    background = pygame.Surface(screen.get_size()).convert()
    background.fill((250, 250, 250))
    all_cells = RenderDirty(board.generate_cells())
    clock = pygame.time.Clock()
    fps = Config.max_fps
    i = 0

    while True:
        clock.tick(fps)
        if i % 60 == 0:  # Calculate FPS only every 60 frames
            print(
                f'\r       \rFPS: {int(clock.get_fps())}'
                f' MAX FPS: {fps}           ', end=''
            )
        i += 1

        for event in pygame.event.get():
            if event.type == gl.QUIT:
                return
            elif event.type == gl.KEYDOWN and event.key == gl.K_ESCAPE:
                return
            elif event.type == gl.KEYDOWN and event.key == gl.K_s:
                running = not running
            elif event.type == gl.KEYDOWN and event.key == gl.K_r:
                board = Board()
                all_cells = RenderDirty(board.generate_cells())
            elif event.type == gl.KEYDOWN and event.key == gl.K_MINUS:
                fps = max((0, fps - 10))
            elif event.type == gl.KEYDOWN and event.key == gl.K_EQUALS:
                fps += 10

        if running:
            all_cells.update()
            board.next_step()
            all_cells.draw(screen)
            pygame.display.flip()


if __name__ == '__main__':
    __main__()
