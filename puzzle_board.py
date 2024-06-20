from tiles import Tile
import pygame

class Puzzle():
    def __init__(self, x1, y1, puzzle, tile_size_x, tile_size_y):
        self._tiles = []
        self._x1 = x1
        self._y1 = y1
        self._rows = puzzle.rows
        self._cols = puzzle.cols
        self._tile_size_x = tile_size_x
        self._tile_size_y = tile_size_y
        self._tile_base = puzzle.gridnums
        self._tile_answers = puzzle.grid
        

    def _create_tiles(self):
        k = 0
        for i in range(self._rows):
            row = []
            for j in range(self._cols):
                x1 = self._x1 + (j * self._tile_size_x)
                y1 = self._y1 + (i * self._tile_size_y)
                x2 = x1 + self._tile_size_x
                y2 = y1 + self._tile_size_y
                new_tile = Tile(x1, y1, x2, y2, self._tile_base[k], self._tile_answers[k])
                row.append(new_tile)
                k += 1
            self._tiles.append(row)

def structure_puzzle(puzzle, x1, y1, tile_size):
    new_puzzle = Puzzle( x1, y1, puzzle, tile_size, tile_size)
    new_puzzle._create_tiles()
    return new_puzzle