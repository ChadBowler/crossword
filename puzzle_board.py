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

    def _group_answers(self):
        down_answers = []
        across_answers = []
        for i in range(self._rows):
            current_word = ""
            for j in range(self._cols):
                if self._tiles[i][j].answer_value == ".":
                    if current_word:
                        across_answers.append(current_word)
                        current_word = ""
                else:
                    current_word += self._tiles[i][j].answer_value
                if j == self._cols - 1:
                    if current_word:
                        across_answers.append(current_word)
                        current_word = ""
                    
        for i in range(self._cols):
            current_word = ""
            for j in range(self._rows):
                if self._tiles[j][i].answer_value == ".":
                    if current_word:
                        down_answers.append(current_word)
                        current_word = ""
                else:
                    current_word += self._tiles[j][i].answer_value
                if j == self._rows - 1:
                    if current_word:
                        down_answers.append(current_word)
                        current_word = ""
        return down_answers, across_answers
    
    def _find_word_across(self):
        def _find_focus(array):
            for tile in array:
                if tile.focus:
                    return True
            return False
        
        for i in range(len(self._tiles)):
            word_array = []
            for j in range(len(self._tiles[i])):
                
                if self._tiles[i][j].answer_value == ".":
                    if _find_focus(word_array):
                        return word_array
                    else:
                        word_array = []
                else:
                    word_array.append(self._tiles[i][j])
                if j == len(self._tiles[i]) - 1:
                    if _find_focus(word_array):
                        return word_array
                    else:
                        word_array = []
                




def structure_puzzle(puzzle, x1, y1, tile_size):
    new_puzzle = Puzzle( x1, y1, puzzle, tile_size, tile_size)
    new_puzzle._create_tiles()
    return new_puzzle