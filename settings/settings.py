import pygame
import json
import math

pygame.init()

class Settings():
    # use theme to get variables from settings file, and data after pulling data from API
    def __init__(self, theme, data) -> None:
        # dimensions
        self.screen_height = pygame.display.Info().current_h * .9
        self.screen_width = self.screen_height * 1.9
        self.font_size = data
        self.margin = data
        #colors
        self.bg_color = theme
        self.board_color = theme
        self.text_color = theme
        self.grid_color = theme
        self.block_highlight = theme
        self.focus_highlight = theme
        self.blank_blocks = theme

    def _get_configs(self):
        with open(r'./settings/settings.json', 'r') as f:
            configs = json.load(f)
        return configs
    
    @property
    def margin(self):
        return self._margin

    @margin.setter
    def margin(self, data):
        if data.cols > 15:
            self._margin = math.floor((self.screen_height * 0.0385)* 0.8)
        else:
            self._margin = math.floor(self.screen_height * 0.0385)

    @property
    def font_size(self):
        return self._font_size

    @font_size.setter
    def font_size(self, data):
        if data.cols > 15:
            self._font_size = math.floor((self.screen_height * 0.0093)* 0.8)
        else:
            self._font_size = math.floor(self.screen_height * 0.0093)

    @property
    def bg_color(self):
        return self._bg_color

    @bg_color.setter
    def bg_color(self, theme):
        self._bg_color = self._get_configs()["appearance"]["themes"][theme]["colors"]["bg_color"]

    @property
    def board_color(self):
        return self._board_color

    @board_color.setter
    def board_color(self, theme):
        self._board_color = self._get_configs()["appearance"]["themes"][theme]["colors"]["board_color"]

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, theme):
        self._text_color = self._get_configs()["appearance"]["themes"][theme]["colors"]["text_color"]

    @property
    def grid_color(self):
        return self._grid_color

    @grid_color.setter
    def grid_color(self, theme):
        self._grid_color = self._get_configs()["appearance"]["themes"][theme]["colors"]["grid_color"]

    @property
    def block_highlight(self):
        return self._block_highlight

    @block_highlight.setter
    def block_highlight(self, theme):
        self._block_highlight = self._get_configs()["appearance"]["themes"][theme]["colors"]["block_highlight"]

    @property
    def focus_highlight(self):
        return self._focus_highlight

    @focus_highlight.setter
    def focus_highlight(self, theme):
        self._focus_highlight = self._get_configs()["appearance"]["themes"][theme]["colors"]["focus_highlight"]

    @property
    def blank_blocks(self):
        return self._blank_blocks

    @blank_blocks.setter
    def blank_blocks(self, theme):
        self._blank_blocks = self._get_configs()["appearance"]["themes"][theme]["colors"]["blank_blocks"]


    def __repr__(self) -> str:
        return f"Screen height: {self.screen_height} Screen width: {self.screen_width}"

