import pygame
import main_functions as mf
import character_model as char
from settings import Settings
from gui.gui_elements import initialize_screen_elements
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def run_character_creator():
    """Initialize Pygame, create a window, instantiate character and start the character creator."""
    # Initialize pygame and create a window.
    pygame.init()
    pg_settings = Settings()
    screen = pygame.display.set_mode((pg_settings.screen_width, pg_settings.screen_height))
    pygame.display.set_caption("Basic Fantasy RPG Character Creator")

    # Create instance of class 'Character'.
    character = char.Character()
    # Set initial state.
    state = "title_screen"
    # Initialize GUI elements.
    gui_elements = initialize_screen_elements(screen)

    # Start main loop.
    while True:
        screen.fill(pg_settings.bg_color)
        state = mf.handle_events(character, state, gui_elements)

        if state == "title_screen":
            mf.show_title_screen(screen, gui_elements)
        elif state == "main_menu":
            mf.show_menu(screen, gui_elements)

        pygame.display.flip()


run_character_creator()
