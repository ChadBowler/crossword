

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
        self.base_value = base_value
        self.answer_value = answer_value
