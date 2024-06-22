from tiles import Tile
import pygame

class Puzzle():
    def __init__(self, puzzle, x1, y1, tile_size):
        self._x1 = x1
        self._y1 = y1
        self.puzzle_data = puzzle
        self._rows = puzzle.rows
        self._cols = puzzle.cols
        self._tile_size_x = tile_size
        self._tile_size_y = tile_size
        self._tile_base = puzzle.gridnums
        self._tile_answers = puzzle.grid
        self._tiles = self._create_tiles()
        self.across = True
        
    def _create_tiles(self):
        tiles = []
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
            tiles.append(row)
        return tiles
    
    def _find_focus(self, array):
            for tile in array:
                if tile.focus:
                    return True
            return False

    def _find_word_across(self):
        for i in range(len(self._tiles)):
            word_array = []
            for j in range(len(self._tiles[i])):
                if self._tiles[i][j].answer_value == ".":
                    if self._find_focus(word_array):
                        return word_array
                    else:
                        word_array = []
                else:
                    word_array.append(self._tiles[i][j])
                if j == len(self._tiles[i]) - 1:
                    if self._find_focus(word_array):
                        return word_array
                    else:
                        word_array = []
                
    def _find_word_down(self):
        for i in range(self._cols):
            word_array = []
            for j in range(self._rows):
                if self._tiles[j][i].answer_value == ".":
                    if self._find_focus(word_array):
                        return word_array
                    else:
                        word_array = []    
                else:
                    word_array.append(self._tiles[j][i])
                if j == self._rows - 1:
                    if self._find_focus(word_array):
                        return word_array
                    else:
                        word_array = [] 
    # cross check user input against answers dictionaries after a word is filled on the board                    
    def check_across_answers(self):
        across_word_array = self._find_word_across()
        key_check = across_word_array[0].base_value
        across_word = ""
        for tile in across_word_array:
            across_word += tile.input
        if self.puzzle_data.across_answer_dict[str(key_check)] == across_word:
            for tile in across_word_array:
                tile.locked = True
            
    def check_down_answers(self):
        down_word_array = self._find_word_down()
        key_check = down_word_array[0].base_value
        down_word = ""
        for tile in down_word_array:
            down_word += tile.input
        if self.puzzle_data.down_answer_dict[str(key_check)] == down_word:
            for tile in down_word_array:
                tile.locked = True

    def clear_focus(self):
        for row in self._tiles:
            for tile in row:
                tile.focus = False