# Example file showing a basic pygame "game loop"
import pygame
from crossword_data import generate_new_puzzle
from puzzle_board import structure_puzzle

gen_puzzle = generate_new_puzzle()
puzzle = structure_puzzle(gen_puzzle)
board_height = puzzle._rows * puzzle._tile_size_y
board_width = puzzle._cols * puzzle._tile_size_x

# pygame setup
pygame.init()
flags = pygame.SCALED
screen = pygame.display.set_mode((1920, 1080), flags)
pygame.display.set_caption('Crossword Game')
clock = pygame.time.Clock()
running = True

color = (0,150,255)
font = pygame.font.Font(None, 36)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # pygame.draw.line(screen, color, (50, 50), (50, 500), width=3)
    # print(puzzle._tiles)
    board = pygame.Surface.subsurface(screen, ((puzzle._x1, puzzle._y1), (board_width, board_height)))
    board.fill("white")
    tiles = []
    for row in puzzle._tiles:
        for tile in row:
            text = font.render(str(tile.answer_value), True, (0, 0, 0))
            board.blit(text, (tile.center_point.x - puzzle._x1, tile.center_point.y - puzzle._y1))
            # square = pygame.draw.rect(board, "red", [tile.tl_corner.x, tile.tl_corner.y, puzzle._tile_size_x, puzzle._tile_size_y])
            # square = pygame.Surface.subsurface(board, ((tile.tl_corner.x + 10, tile.tl_corner.y + 10), (puzzle._tile_size_x - 20, puzzle._tile_size_y - 20)))
            # pygame.Surface.blit(square, board, (tile.tl_corner.x, tile.tl_corner.y))

            pygame.draw.line(screen, color, (tile.tl_corner.x, tile.tl_corner.y), (tile.bl_corner.x, tile.bl_corner.y), width=3)
            pygame.draw.line(screen, color, (tile.tl_corner.x, tile.tl_corner.y), (tile.tr_corner.x, tile.tr_corner.y), width=3)
            pygame.draw.line(screen, color, (tile.tr_corner.x, tile.tr_corner.y), (tile.br_corner.x, tile.br_corner.y), width=3)
            pygame.draw.line(screen, color, (tile.br_corner.x, tile.br_corner.y), (tile.bl_corner.x, tile.bl_corner.y), width=3)

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()