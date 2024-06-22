import pygame
import pygame_menu
from settings.settings import Settings

settings = Settings("dark")

pygame.init()
surface = pygame.display.set_mode((settings.screen_width, settings.screen_height))


def start_game():
    print("hello world")

menu = pygame_menu.Menu('Welcome', settings.screen_width, settings.screen_height)

menu.add.text_input('Name :', default='John Doe')
# menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(surface)
                
