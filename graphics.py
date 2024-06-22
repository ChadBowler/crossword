import pygame
import math

class Graphics():
    def __init__(self, settings, data, puzzle) -> None:
        self.settings = settings
        self.data = data
        self.puzzle = puzzle
        # screen
        self.screen = pygame.display.set_mode((settings.screen_width, settings.screen_height), flags=pygame.SCALED)
        self.screen_height = self.screen.get_height()
        self.screen_width = self.screen.get_width()
        self.margin = settings.margin
        # board
        self.board_height = puzzle._rows * puzzle._tile_size_y
        self.board_width = puzzle._cols * puzzle._tile_size_x
        self.board = pygame.Surface.subsurface(self.screen, ((puzzle._x1, puzzle._y1), (self.board_width, self.board_height)))
        # tiles
        self.grid_color = settings.grid_color
        self.focus_highlight = settings.focus_highlight
        self.blank_blocks = settings.blank_blocks
        self.number_font = pygame.font.Font(None, math.floor(settings.font_size * 2))
        self.type_font = pygame.font.Font(None, math.floor(settings.font_size * 3))
        # clues
        self.clues_section = pygame.Surface.subsurface(self.screen, ((self.board_width + self.margin*2, puzzle._y1), (self.board_width * 1.8, self.screen_height - puzzle._y1)))
        self.clues_size = math.floor(settings.font_size * 1.8)
        self.clues_font = pygame.font.Font(None, math.floor(settings.font_size * 1.8))
        self.clues_header_font = pygame.font.Font(None, math.floor(settings.font_size * 3.5))
        # extra info
        self.info_section = pygame.Surface.subsurface(self.screen, ((puzzle._x1, self.board_height + self.margin*2), (self.board_width, self.screen_height - self.board_height - self.margin*3)))
        self.author = data.author
        self.editor = data.editor
        self.cpyright = data.cpyright
        self.date = data.date
        self.publisher = data.publisher
        self.title = data.title
        self.title_font = pygame.font.Font(None, math.floor(settings.font_size * 4.5))
        self.info_font = pygame.font.Font(None, math.floor(settings.font_size * 2))

    # use the draw.line to draw 4 lines around the tile
    def draw_grid(self, tile):
        pygame.draw.line(self.screen, self.grid_color, (tile.tl_corner.x, tile.tl_corner.y), (tile.bl_corner.x, tile.bl_corner.y), width=3)
        pygame.draw.line(self.screen, self.grid_color, (tile.tl_corner.x, tile.tl_corner.y), (tile.tr_corner.x, tile.tr_corner.y), width=3)
        pygame.draw.line(self.screen, self.grid_color, (tile.tr_corner.x, tile.tr_corner.y), (tile.br_corner.x, tile.br_corner.y), width=3)
        pygame.draw.line(self.screen, self.grid_color, (tile.br_corner.x, tile.br_corner.y), (tile.bl_corner.x, tile.bl_corner.y), width=3)
    # fill in blank squares, and create a square to represent the focus tile
    def draw_square(self, square_type, tile):
        if square_type == "focus":
            square_color = self.focus_highlight
        if square_type == "blank":
            square_color = self.blank_blocks
        number = self.number_font.render(str(tile.base_value), True, self.settings.text_color)
        text = self.type_font.render(str(tile.input), True, self.settings.text_color)
        square = pygame.draw.rect(self.board, square_color, [tile.tl_corner.x - self.puzzle._x1 + 2, tile.tl_corner.y - self.puzzle._y1 + 2, self.puzzle._tile_size_x - 3, self.puzzle._tile_size_y - 3])
        if tile.base_value != 0:
            self.board.blit(number, (tile.tl_corner.x - self.puzzle._x1 + 3, tile.tl_corner.y - self.puzzle._y1 + 3))
        self.board.blit(text, (tile.center_point.x - self.puzzle._x1 - 5, tile.center_point.y - self.puzzle._y1 - 5))
    # highlight the current word the user is focused on
    def draw_across_highlight(self, array, color, width=4):
        if array:
            pygame.draw.lines(self.board, color, True, [(array[0].tl_corner.x - self.margin, array[0].tl_corner.y - self.margin*2), (array[-1].tr_corner.x - self.margin, array[-1].tr_corner.y - self.margin*2), (array[-1].br_corner.x - self.margin, array[-1].br_corner.y - self.margin*2), (array[0].bl_corner.x - self.margin, array[0].bl_corner.y - self.margin*2)], width)
        else:
            return
    def draw_down_highlight(self, array, color, width=4):
        if array:
            pygame.draw.lines(self.board, color, True, [(array[0].tl_corner.x - self.margin, array[0].tl_corner.y - self.margin*2), (array[0].tr_corner.x - self.margin, array[0].tr_corner.y - self.margin*2), (array[-1].br_corner.x - self.margin, array[-1].br_corner.y - self.margin*2), (array[-1].bl_corner.x - self.margin, array[-1].bl_corner.y - self.margin*2)], width)
        else:
            return
    
    def draw_highlights(self, puzzle):
        if puzzle.across:
            self.draw_across_highlight(array=puzzle._find_word_across(), color=self.settings.block_highlight)
        else:
            self.draw_down_highlight(array=puzzle._find_word_down(), color=self.settings.block_highlight)
    # two separate blocks for displaying clues depending on how many clues there are
    def display_clues(self):
        if len(self.data.down_clues) > 70 or len(self.data.across_clues) > 70:
            down_clues_header = self.clues_header_font.render("Down:", True, self.settings.text_color)
            self.clues_section.blit(down_clues_header, (self.margin // 2, 0))

            for i in range(len(self.data.down_clues)//2):
                clue_text = self.clues_font.render(self.data.down_clues[i], True, self.settings.text_color)
                self.clues_section.blit(clue_text, (self.margin // 2, 40 + i*self.clues_size))
            for i in range(len(self.data.down_clues)//2, len(self.data.down_clues)):
                clue_text = self.clues_font.render(self.data.down_clues[i], True, self.settings.text_color)
                self.clues_section.blit(clue_text, (self.clues_section.get_width()//4 + self.margin*2, 40 + (i - len(self.data.down_clues)//2)*self.clues_size))

            across_clues_header = self.clues_header_font.render("Across:", True, self.settings.text_color)
            self.clues_section.blit(across_clues_header, (self.clues_section.get_width()//2 + self.margin*3, 0))

            for i in range(len(self.data.across_clues)//2):
                clue_text = self.clues_font.render(self.data.across_clues[i], True, self.settings.text_color)
                self.clues_section.blit(clue_text, (self.clues_section.get_width()//2 + self.margin*3, 40 + i*self.clues_size))
            for i in range(len(self.data.across_clues)//2, len(self.data.across_clues)):
                clue_text = self.clues_font.render(self.data.across_clues[i], True, self.settings.text_color)
                self.clues_section.blit(clue_text, (self.clues_section.get_width()//4*3 + self.margin*4, 40 + (i - len(self.data.across_clues)//2)*self.clues_size))

        else:
            down_clues_header = self.clues_header_font.render("Down:", True, self.settings.text_color)
            self.clues_section.blit(down_clues_header, (self.margin // 2, 0))

            for i in range(len(self.data.down_clues)):
                clue_text = self.clues_font.render(self.data.down_clues[i], True, self.settings.text_color)
                self.clues_section.blit(clue_text, (self.margin // 2, 40 + i*self.clues_size))

            across_clues_header = self.clues_header_font.render("Across:", True, self.settings.text_color)
            self.clues_section.blit(across_clues_header, (self.clues_section.get_width()//2 + self.margin*2, 0))

            for i in range(len(self.data.across_clues)):
                clue_text = self.clues_font.render(self.data.across_clues[i], True, self.settings.text_color)
                self.clues_section.blit(clue_text, (self.clues_section.get_width()//2 + self.margin*2, 40 + i*self.clues_size))

    def fill_tiles(self, tile):
        # set tile background as a subsurface of board
        tile_bg = self.board.subsurface([tile.tl_corner.x - self.puzzle._x1, tile.tl_corner.y - self.puzzle._y1, self.puzzle._tile_size_x, self.puzzle._tile_size_y])
        # Set up the values that will be rendered in each square
        number = self.number_font.render(str(tile.base_value), True, self.settings.text_color)
        text = self.type_font.render(str(tile.input), True, self.settings.text_color)
        # Set up blank tiles
        if tile.answer_value == ".":
            tile.blank = True
            self.draw_square("blank", tile)
        else:
            self.board.blit(text, (tile.center_point.x - self.puzzle._x1 - 5, tile.center_point.y - self.puzzle._y1 - 5))

        # Set the numbers as blits in each square that has a number
        if tile.base_value != 0:
            self.board.blit(number, (tile.tl_corner.x - self.puzzle._x1 + 3, tile.tl_corner.y - self.puzzle._y1 + 3))
    # Title and puzzle info
    def render_info(self):
        title = self.title_font.render(self.title, True, self.settings.text_color)
        self.screen.blit(title, (self.screen_width // 2 - self.margin * 4, self.margin))
        author = self.info_font.render(f"Author: {self.author}                     Editor: {self.editor}", True, self.settings.text_color)
        self.info_section.blit(author, (self.margin, self.margin))
        publisher = self.info_font.render(f"Publisher: {self.publisher}", True, self.settings.text_color)
        self.info_section.blit(publisher, (self.margin, self.margin*2))
        cpyright = self.info_font.render(f"©{self.cpyright}", True, self.settings.text_color)
        self.info_section.blit(cpyright, (self.margin, self.margin*3))
        