# Example file showing a basic pygame "game loop"
import pygame
from settings.settings import Settings
from crossword_data import generate_new_puzzle
from puzzle_board import structure_puzzle


# pygame setup
pygame.init()

settings = Settings("dark")
# print(settings)
screen_height = settings.screen_height
screen_width = settings.screen_width
flags = pygame.SCALED
screen = pygame.display.set_mode((screen_width, screen_height), flags)
pygame.display.set_caption('Crossword Game')
clock = pygame.time.Clock()
running = True

# print(pygame.font.get_default_font())

margin = 50
tile_size = 50
clues_size = 22
number_font = pygame.font.Font(None, 24)
type_font = pygame.font.Font(None, 36)
clues_font = pygame.font.Font(None, clues_size)
header_font = pygame.font.Font(None, 40)

def new_puzzle():
    # gen_puzzle is the Data class
    gen_puzzle = generate_new_puzzle()
    # puzzle is the Puzzle class
    puzzle = structure_puzzle(gen_puzzle, margin, margin*2, tile_size)
    board_height = puzzle._rows * puzzle._tile_size_y
    board_width = puzzle._cols * puzzle._tile_size_x
    # board is the surface where the gameboard is drawn
    board = pygame.Surface.subsurface(screen, ((puzzle._x1, puzzle._y1), (board_width, board_height)))
    clues_section = pygame.Surface.subsurface(screen, ((screen_width - board_width - margin*2, puzzle._y1), (board_width, screen_height - puzzle._y1)))
    return board, puzzle, gen_puzzle, clues_section


try:
    board, puzzle, gen_puzzle, clues_section = new_puzzle()    
except ValueError:
    board, puzzle, gen_puzzle, clues_section = new_puzzle()


def display_clues():
    down_clues_header = header_font.render("Down:", True, settings.text_color)
    clues_section.blit(down_clues_header, (margin / 2, 0))
    for i in range(len(gen_puzzle.down_clues)):
        clue_text = clues_font.render(gen_puzzle.down_clues[i], True, settings.text_color)
        clues_section.blit(clue_text, (margin / 2, 40 + i*clues_size))
    across_clues_header = header_font.render("Across:", True, settings.text_color)
    clues_section.blit(across_clues_header, (clues_section.get_width()/2 + margin*2, 0))
    for i in range(len(gen_puzzle.across_clues)):
        clue_text = clues_font.render(gen_puzzle.across_clues[i], True, settings.text_color)
        clues_section.blit(clue_text, (clues_section.get_width()/2 + margin*2, 40 + i*clues_size))

def clear_focus():
    for row in puzzle._tiles:
        for tile in row:
            tile.focus = False

def draw_grid(tile):
    pygame.draw.line(screen, settings.grid_color, (tile.tl_corner.x, tile.tl_corner.y), (tile.bl_corner.x, tile.bl_corner.y), width=3)
    pygame.draw.line(screen, settings.grid_color, (tile.tl_corner.x, tile.tl_corner.y), (tile.tr_corner.x, tile.tr_corner.y), width=3)
    pygame.draw.line(screen, settings.grid_color, (tile.tr_corner.x, tile.tr_corner.y), (tile.br_corner.x, tile.br_corner.y), width=3)
    pygame.draw.line(screen, settings.grid_color, (tile.br_corner.x, tile.br_corner.y), (tile.bl_corner.x, tile.bl_corner.y), width=3)

def draw_square(square_type):
    if square_type == "focus":
        square_color = settings.focus_highlight
    if square_type == "blank":
        square_color = settings.blank_blocks
    square = pygame.draw.rect(board, square_color, [tile.tl_corner.x - puzzle._x1 + 2, tile.tl_corner.y - puzzle._y1 + 2, puzzle._tile_size_x - 3, puzzle._tile_size_y - 3])
    if tile.base_value != 0:
        board.blit(number, (tile.tl_corner.x - puzzle._x1 + 3, tile.tl_corner.y - puzzle._y1 + 3))
    board.blit(text, (tile.center_point.x - puzzle._x1 - 5, tile.center_point.y - puzzle._y1 - 5))


def draw_across_highlight(array, color, width=4):
    if array:
        pygame.draw.lines(board, color, True, [(array[0].tl_corner.x - margin, array[0].tl_corner.y - margin*2), (array[-1].tr_corner.x - margin, array[-1].tr_corner.y - margin*2), (array[-1].br_corner.x - margin, array[-1].br_corner.y - margin*2), (array[0].bl_corner.x - margin, array[0].bl_corner.y - margin*2)], width)
    else:
        return
def draw_down_highlight(array, color, width=4):
    if array:
        pygame.draw.lines(board, color, True, [(array[0].tl_corner.x - margin, array[0].tl_corner.y - margin*2), (array[0].tr_corner.x - margin, array[0].tr_corner.y - margin*2), (array[-1].br_corner.x - margin, array[-1].br_corner.y - margin*2), (array[-1].bl_corner.x - margin, array[-1].bl_corner.y - margin*2)], width)
    else:
        return

def check_across_answers():
    across_word_array = puzzle._find_word_across()
    key_check = across_word_array[0].base_value
    across_word = ""
    for tile in across_word_array:
        across_word += tile.input
    if gen_puzzle.across_answer_dict[str(key_check)] == across_word:
        for tile in across_word_array:
            tile.locked = True
        # draw_across_highlight(across_word_array, "yellow", 5)
        

def check_down_answers():
    down_word_array = puzzle._find_word_down()
    key_check = down_word_array[0].base_value
    down_word = ""
    for tile in down_word_array:
        down_word += tile.input
    if gen_puzzle.down_answer_dict[str(key_check)] == down_word:
        for tile in down_word_array:
            tile.locked = True
        # draw_down_highlight(down_word_array, "yellow", width=5)
        

def change_direction():
    if puzzle.across:
        puzzle.across = False
    else:
        puzzle.across = True

def handle_keyboard_input():
    # next_focus boolean to handle looping logic when changing focus
    next_focus = False
    # alpha characters
    if event.key >= 97 and event.key <= 122:
        if puzzle.across:
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
                            check_across_answers()
                            check_down_answers()
                            clear_focus()
                            next_focus = True
        else:
            for i in range(puzzle._cols):
                for j in range(puzzle._rows):
                    tile = puzzle._tiles[j][i]
                    if next_focus:
                        if not tile.blank:
                            tile.focus = True
                            next_focus = False
                            continue
                    if tile.focus:
                        if not tile.locked:
                            tile.input = event.unicode.upper()
                            check_down_answers()
                            check_across_answers()
                            clear_focus()
                            next_focus = True
    # backspace (8) and delete (127) keys
    elif event.key == 8 or event.key == 127:
        for row in puzzle._tiles:
            for tile in row: 
                if tile.focus:
                    if not tile.locked:
                        tile.input = ""
    # arrow keys
    elif event.key == pygame.K_LEFT:
        for i in range(len(puzzle._tiles)-1, -1, -1):
            for j in range(len(puzzle._tiles[i])-1, -1, -1):
                if next_focus:
                    if not puzzle._tiles[i][j].blank:
                        puzzle._tiles[i][j].focus = True
                        next_focus = False
                        return
                if puzzle._tiles[i][j].focus:
                    if i == 0 and j == 0:
                        clear_focus()
                        puzzle._tiles[-1][-1].focus = True
                        break
                    clear_focus()
                    next_focus = True
    elif event.key == pygame.K_RIGHT:
        for i in range(len(puzzle._tiles)):
            for j in range(len(puzzle._tiles[i])):
                if next_focus:
                    if not puzzle._tiles[i][j].blank:
                        puzzle._tiles[i][j].focus = True
                        next_focus = False
                        return
                if puzzle._tiles[i][j].focus:
                    if i == len(puzzle._tiles) - 1 and j == len(puzzle._tiles[i]) - 1:
                        clear_focus()
                        puzzle._tiles[0][0].focus = True
                        break
                    clear_focus()
                    next_focus = True
    elif event.key == pygame.K_DOWN:
        for i in range(len(puzzle._tiles)):
            for j in range(len(puzzle._tiles[i])):
                if puzzle._tiles[i][j].focus:
                    clear_focus()
                    next_focus = True
                    while next_focus:
                        if i == len(puzzle._tiles) - 1:
                            i = -1
                        i += 1
                        if not puzzle._tiles[i][j].blank:
                            puzzle._tiles[i][j].focus = True
                            next_focus = False
                            return
    elif event.key == pygame.K_UP:
        for i in range(len(puzzle._tiles) - 1, -1, -1):
            for j in range(len(puzzle._tiles[i]) - 1, -1, -1):
                if puzzle._tiles[i][j].focus:
                    clear_focus()
                    next_focus = True
                    while next_focus:
                        if i == -1:
                            i = len(puzzle._tiles) - 1
                        i -= 1
                        if not puzzle._tiles[i][j].blank:
                            puzzle._tiles[i][j].focus = True
                            next_focus = False
                            return
    elif event.key == pygame.K_TAB:
        change_direction()
       

    else:
        print(event.key)





down_answers, across_answers = puzzle._group_answers()
# print(gen_puzzle.across_answer_dict)
# print(gen_puzzle.down_answer_dict)
# print(across_answers)
# print(down_answers)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    mos_x, mos_y = pygame.mouse.get_pos()
    # print(mos_x, mos_y)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Get user input for squares
        if event.type == pygame.KEYDOWN:
            handle_keyboard_input()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill(settings.bg_color)
    board.fill(settings.board_color)
    # clues_section.fill("white")
    # Set up individual tiles on the screen
    tiles = []
    
    for row in puzzle._tiles:
        for tile in row:
            # Draw grid
            draw_grid(tile)

            # set tile background as a subsurface of board
            tile_bg = board.subsurface([tile.tl_corner.x - puzzle._x1, tile.tl_corner.y - puzzle._y1, puzzle._tile_size_x, puzzle._tile_size_y])
            # Set up the values that will be rendered in each square
            number = number_font.render(str(tile.base_value), True, settings.text_color)
            text = type_font.render(str(tile.input), True, settings.text_color)
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
            
    # Render clues text
    display_clues()
    # highlight current word
    if puzzle.across:
        draw_across_highlight(array=puzzle._find_word_across(), color=settings.block_highlight)
    else:
        draw_down_highlight(array=puzzle._find_word_down(), color=settings.block_highlight)

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