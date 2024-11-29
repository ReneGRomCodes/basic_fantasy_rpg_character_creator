import pygame
import pygame_textinput
from settings import Settings
import sys
import gui.screen_objects
"""This file contains code in development and is meant to try out concepts or just play around with ideas."""

# TODO figure out how to implement different attacks with spear in 'item_instance.py'
# TODO Equip/unequip methods work only for armor right now in 'character_model.py'
# TODO fully implement weapons shop within 'shop_functions.py'

Settings = Settings()

def show_test_screen():
    """Initialize Pygame and create a window to test GUI elements."""
    pygame.init()
    screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))

    # Create TextInput-object
    textinput = pygame_textinput.TextInputVisualizer()


    while True:
        screen.fill(Settings.bg_color)

        events = pygame.event.get()

        # Feed it with events every frame
        textinput.update(events)
        # Blit its surface onto the screen
        screen.blit(textinput.surface, (10, 10))

        pygame.display.update()


show_test_screen()
