# Example file showing a basic pygame "game loop"
import pygame
from crossword_data import generate_new_puzzle
from puzzle_board import structure_puzzle

# gen_puzzle = generate_new_puzzle()
# puzzle = structure_puzzle(gen_puzzle)
# board_height = puzzle._rows * puzzle._tile_size_y
# board_width = puzzle._cols * puzzle._tile_size_x

# pygame setup
pygame.init()
flags = pygame.SCALED
screen = pygame.display.set_mode((1920, 1080), flags)
pygame.display.set_caption('Crossword Game')
clock = pygame.time.Clock()
running = True

light_blue = (0,150,255)
light_gray = "#A6A6A6"
dark_gray = "#343840"
number_font = pygame.font.Font(None, 24)
font = pygame.font.Font(None, 36)

def new_puzzle():
    gen_puzzle = generate_new_puzzle()
    puzzle = structure_puzzle(gen_puzzle)
    board_height = puzzle._rows * puzzle._tile_size_y
    board_width = puzzle._cols * puzzle._tile_size_x
    board = pygame.Surface.subsurface(screen, ((puzzle._x1, puzzle._y1), (board_width, board_height)))
    return board, puzzle

try:
    board, puzzle = new_puzzle()
    
except ValueError:
    board, puzzle = new_puzzle()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    board.fill("white")
    tiles = []
    for row in puzzle._tiles:
        for tile in row:
            number = number_font.render(str(tile.base_value), True, (0, 0, 0))
            text = font.render(str(tile.answer_value), True, (0, 0, 0))
            if tile.answer_value == ".":
                square = pygame.draw.rect(board, dark_gray, [tile.tl_corner.x - puzzle._x1, tile.tl_corner.y - puzzle._y1, puzzle._tile_size_x, puzzle._tile_size_y])
            # else:
            #     board.blit(text, (tile.center_point.x - puzzle._x1 - 5, tile.center_point.y - puzzle._y1 - 5))
            if tile.base_value != 0:
                board.blit(number, (tile.tl_corner.x - puzzle._x1 + 3, tile.tl_corner.y - puzzle._y1 + 3))

            pygame.draw.line(screen, light_blue, (tile.tl_corner.x, tile.tl_corner.y), (tile.bl_corner.x, tile.bl_corner.y), width=3)
            pygame.draw.line(screen, light_blue, (tile.tl_corner.x, tile.tl_corner.y), (tile.tr_corner.x, tile.tr_corner.y), width=3)
            pygame.draw.line(screen, light_blue, (tile.tr_corner.x, tile.tr_corner.y), (tile.br_corner.x, tile.br_corner.y), width=3)
            pygame.draw.line(screen, light_blue, (tile.br_corner.x, tile.br_corner.y), (tile.bl_corner.x, tile.bl_corner.y), width=3)


    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()