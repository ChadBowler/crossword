

class Point():
    def __init__(self, x, y):
        self.x=x
        self.y=y


class Tile():
    def __init__(self, x1, y1, x2, y2, base_value=None, answer_value=None):
        # defining significant points in a tile
        self.tl_corner = Point(x1, y1)
        self.tr_corner = Point(x2, y1)
        self.bl_corner = Point(x1, y2)
        self.br_corner = Point(x2, y2)
        self.center_point = Point(((x2+x1)/2), ((y2+y1)/2))
        # base_value shows the numbers on the board(or leaves it blank if it's a 0)
        self.base_value = base_value
        # answer_value is the correct letter for the tile
        self.answer_value = answer_value
        # input is the user's input
        self.input = ""
        # focus allows us to highlight different cells
        self.focus = False
        # blank is for filler spaces in the puzzle that won't be filled in with letters
        self.blank = False
        # locked will remove the ability to change the value in the tile
        self.locked = False