import pygame

def change_direction(puzzle):
    if puzzle.across:
        puzzle.across = False
    else:
        puzzle.across = True

def handle_keyboard_input(event, puzzle):
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
                            puzzle.check_across_answers()
                            puzzle.check_down_answers()
                            puzzle.clear_focus()
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
                            puzzle.check_down_answers()
                            puzzle.check_across_answers()
                            puzzle.clear_focus()
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
                        puzzle.clear_focus()
                        puzzle._tiles[-1][-1].focus = True
                        break
                    puzzle.clear_focus()
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
                        puzzle.clear_focus()
                        puzzle._tiles[0][0].focus = True
                        break
                    puzzle.clear_focus()
                    next_focus = True
    elif event.key == pygame.K_DOWN:
        for i in range(len(puzzle._tiles)):
            for j in range(len(puzzle._tiles[i])):
                if puzzle._tiles[i][j].focus:
                    puzzle.clear_focus()
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
                    puzzle.clear_focus()
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
        change_direction(puzzle)
       

    else:
        print(event.key)