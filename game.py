# Example file showing a basic pygame "game loop"
import pygame
import pygame_menu
from settings.settings import Settings
from graphics import Graphics
from crossword_data import Data
from puzzle_board import Puzzle
from keyboard_input import handle_keyboard_input

# pygame setup
pygame.init()

puzzle_data = Data()
settings = Settings("dark", puzzle_data)
puzzle = Puzzle(puzzle_data, settings.margin, settings.margin*2, settings.margin)
graphics = Graphics(settings, puzzle_data, puzzle)
pygame.display.set_caption('Crossword Game')
clock = pygame.time.Clock()
running = True

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Get user input for squares
        if event.type == pygame.KEYDOWN:
            handle_keyboard_input(event, puzzle)
    # keeping track of the mouse position
    mos_x, mos_y = pygame.mouse.get_pos()
    # fill the screen with a color to wipe away anything from last frame
    graphics.screen.fill(settings.bg_color)
    graphics.board.fill(settings.board_color)
    # Set up individual tiles on the screen
    for row in puzzle._tiles:
        for tile in row:
            graphics.draw_grid(tile)
            graphics.fill_tiles(tile)

            # Set focus for squares
            if event.type==pygame.MOUSEBUTTONDOWN and tile.tl_corner.x < mos_x and mos_x < tile.tr_corner.x and tile.tl_corner.y < mos_y and mos_y < tile.bl_corner.y:
                puzzle.clear_focus()
                if not tile.blank:
                    tile.focus = True
            if tile.focus:
                graphics.draw_square("focus", tile)
            
    # Render clues text
    graphics.display_clues()
    graphics.render_info()
    # highlight current word
    graphics.draw_highlights(puzzle)

    # clear focus if mouse is pressed outside the game board
    if (event.type==pygame.MOUSEBUTTONDOWN and 
        (puzzle._x1 > mos_x
        or mos_x > puzzle._x1 +  puzzle._cols * puzzle._tile_size_x
        or puzzle._y1 > mos_y 
        or mos_y > puzzle._y1 +  puzzle._rows * puzzle._tile_size_y)):
                puzzle.clear_focus()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()