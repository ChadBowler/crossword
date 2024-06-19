# Example file showing a basic pygame "game loop"
import pygame
from crossword_data import generate_new_puzzle
from puzzle_board import structure_puzzle

# pygame setup
pygame.init()
flags = pygame.SCALED
screen = pygame.display.set_mode((1920, 1080), flags)
pygame.display.set_caption('Crossword Game')
clock = pygame.time.Clock()
running = True

light_blue = (0,150,255)
light_gray = (166, 166, 166)
dark_gray = (52, 56, 64)
number_font = pygame.font.Font(None, 24)
type_font = pygame.font.Font(None, 36)

def new_puzzle():
    gen_puzzle = generate_new_puzzle()
    puzzle = structure_puzzle(gen_puzzle)
    board_height = puzzle._rows * puzzle._tile_size_y
    board_width = puzzle._cols * puzzle._tile_size_x
    board = pygame.Surface.subsurface(screen, ((puzzle._x1, puzzle._y1), (board_width, board_height)))
    return board, puzzle

# def set_focus():
#     if not tile.blank:
#         tile.focus = True
#     draw_square("focus")

def clear_focus():
    for row in puzzle._tiles:
        for tile in row:
            tile.focus = False

def draw_grid(tile):
    pygame.draw.line(screen, light_blue, (tile.tl_corner.x, tile.tl_corner.y), (tile.bl_corner.x, tile.bl_corner.y), width=3)
    pygame.draw.line(screen, light_blue, (tile.tl_corner.x, tile.tl_corner.y), (tile.tr_corner.x, tile.tr_corner.y), width=3)
    pygame.draw.line(screen, light_blue, (tile.tr_corner.x, tile.tr_corner.y), (tile.br_corner.x, tile.br_corner.y), width=3)
    pygame.draw.line(screen, light_blue, (tile.br_corner.x, tile.br_corner.y), (tile.bl_corner.x, tile.bl_corner.y), width=3)



def handle_keyboard_input():
    next_focus = False
    if event.key >= 97 and event.key <= 122:
        for row in puzzle._tiles:
            for tile in row:
                if next_focus:
                    if not tile.blank:
                        tile.focus = True
                        next_focus = False
                        continue
                if tile.focus:
                    if not tile.locked:
                        tile.input = event.unicode.upper()
                        clear_focus()
                        next_focus = True                        
    elif event.key == 8 or event.key == 127:
        for row in puzzle._tiles:
            for tile in row:
                
                if tile.focus:
                    if not tile.locked:
                        tile.input = ""
    else:
        if event.key == pygame.K_LEFT:
            print("left")
        # print(event)

def draw_square(square_type):
    if square_type == "focus":
        square_color = light_gray
    if square_type == "blank":
        square_color = dark_gray
    square = pygame.draw.rect(board, square_color, [tile.tl_corner.x - puzzle._x1 + 2, tile.tl_corner.y - puzzle._y1 + 2, puzzle._tile_size_x - 3, puzzle._tile_size_y - 3])
    if tile.base_value != 0:
        board.blit(number, (tile.tl_corner.x - puzzle._x1 + 3, tile.tl_corner.y - puzzle._y1 + 3))
    board.blit(text, (tile.center_point.x - puzzle._x1 - 5, tile.center_point.y - puzzle._y1 - 5))

try:
    board, puzzle = new_puzzle()    
except ValueError:
    board, puzzle = new_puzzle()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    mos_x, mos_y = pygame.mouse.get_pos()
    # print(mos_x, mos_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            handle_keyboard_input()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    board.fill("white")

    tiles = []
    for row in puzzle._tiles:
        for tile in row:
            # Draw grid
            draw_grid(tile)

            # set tile background as a subsurface of board
            tile_bg = board.subsurface([tile.tl_corner.x - puzzle._x1, tile.tl_corner.y - puzzle._y1, puzzle._tile_size_x, puzzle._tile_size_y])
            # Set up the values that will be rendered in each square
            number = number_font.render(str(tile.base_value), True, (0, 0, 0))
            text = type_font.render(str(tile.input), True, (0, 0, 0))
            # Set up blank tiles
            if tile.answer_value == ".":
                tile.blank = True
                draw_square("blank")
            else:
                board.blit(text, (tile.center_point.x - puzzle._x1 - 5, tile.center_point.y - puzzle._y1 - 5))

            # Set the numbers as blits in each square that has a number
            if tile.base_value != 0:
                board.blit(number, (tile.tl_corner.x - puzzle._x1 + 3, tile.tl_corner.y - puzzle._y1 + 3))
            tiles.append(tile_bg)
            # Set focus for squares

            if event.type==pygame.MOUSEBUTTONDOWN and tile.tl_corner.x < mos_x and mos_x < tile.tr_corner.x and tile.tl_corner.y < mos_y and mos_y < tile.bl_corner.y:
                clear_focus()
                if not tile.blank:
                    tile.focus = True
            if tile.focus:
                draw_square("focus")
            # Get user input for squares
    
        # if event.key == pygame.K_0:
        #     print("Hey, you pressed the key, '0'!")
        # if event.key == pygame.K_1:
        #     print("Doing whatever")
    # # if event.type==pygame.KEYDOWN:
    # if pygame.key.get_pressed()[pygame.K_SPACE]:
    # # type_text = pygame.event.event_name(event.type)
    # # typed = type_font.render(type_text, True, (0, 0, 0))
    #     print("I pressed space bar")
    # else:
    #     print("What did I press?")
        # board.blit(typed, (tile.center_point.x - puzzle._x1 - 5, tile.center_point.y - puzzle._y1 - 5))


    # clear focus if mouse is pressed outside the game board
    if (event.type==pygame.MOUSEBUTTONDOWN and 
        (puzzle._x1 > mos_x
        or mos_x > puzzle._x1 +  puzzle._cols * puzzle._tile_size_x
        or puzzle._y1 > mos_y 
        or mos_y > puzzle._y1 +  puzzle._rows * puzzle._tile_size_y)):
                clear_focus()

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()