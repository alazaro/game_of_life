import random
from copy import deepcopy
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
    max_fps = 100
    seed = 1
    alive_cells_at_start = 0.1
    title = 'Game of Life'


class Board:
    size = Config.board_size
    cells: BoolMatrix

    def __init__(self):
        random.seed(Config.seed)
        self.cells = [
            random.choices(
                (True, False),
                cum_weights=(Config.alive_cells_at_start, 1),
                k=self.size[1]
            )
            for w in range(self.size[0])
        ]

    def next_step(self):
        next_cells = deepcopy(self.cells)
        for y, column in enumerate(self.cells):
            for x, cell in enumerate(column):
                next_cells[x][y] = self.get_next_status(x, y)
        self.cells = next_cells

    def get_next_status(self, x: int, y: int) -> bool:
        alive_neighbors = len(self.get_alive_neighbors(x, y))
        status = self.cells[x][y]
        return (
            status and alive_neighbors in (2, 3)
            or not status and alive_neighbors == 3
        ) or False

    def get_alive_neighbors(self, x: int, y: int) -> Sequence[Point]:
        neighbors = self.get_neighbors(x, y)
        alive = []
        for x_, y_ in neighbors:
            # Connect with the opposite edge
            if x_ >= self.size[0]:
                x_ = 0
            if y_ >= self.size[1]:
                y_ = 0
            if self.cells[x_][y_]:
                alive.append((x_, y_))
        return alive

    def get_neighbors(self, x: int, y: int) -> Sequence[Point]:
        return (
            (x - 1, y - 1),
            (x + 1, y - 1),
            (x - 1, y + 1),
            (x + 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x - 1, y),
            (x + 1, y),
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
    size = Config.cell_size

    def __init__(self, x: int, y: int, status: bool, board: Board):
        super().__init__()
        self.image = pygame.Surface(Config.cell_size)
        self.rect = self.image.get_rect()
        self.rect.x = x * self.size[0]
        self.rect.y = y * self.size[1]
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
        board.size[0] * GameCell.size[0],
        board.size[1] * GameCell.size[1]
    ))
    pygame.display.set_caption(Config.title)
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((250, 250, 250))
    all_cells = pygame.sprite.RenderUpdates(board.generate_cells())
    clock = pygame.time.Clock()

    while True:
        clock.tick(Config.max_fps)
        print(f'\r       \rFPS: {int(clock.get_fps())}', end='')

        for event in pygame.event.get():
            if event.type == gl.QUIT:
                return
            elif event.type == gl.KEYDOWN and event.key == gl.K_ESCAPE:
                return
            elif event.type == gl.KEYDOWN and event.key == gl.K_s:
                running = not running
            elif event.type == gl.KEYDOWN and event.key == gl.K_r:
                board = Board()
                all_cells = pygame.sprite.RenderUpdates(board.generate_cells())
            elif event.type == gl.MOUSEBUTTONDOWN:
                pass
            elif event.type == gl.MOUSEBUTTONUP:
                pass

        if running:
            all_cells.update()
            board.next_step()
            all_cells.draw(screen)
            pygame.display.flip()


if __name__ == '__main__':
    __main__()
