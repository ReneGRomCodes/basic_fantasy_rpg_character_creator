import pygame
import main_functions as mf
import character_model as char
from settings import Settings
import screen_objects as so
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def run_character_creator():
    """Initialize Pygame, create a window and start the character creator."""
    # Initialize pygame and create a window.
    pygame.init()
    pg_settings = Settings()
    screen = pygame.display.set_mode((pg_settings.screen_width, pg_settings.screen_height))
    pygame.display.set_caption("Basic Fantasy RPG Character Creator")

    # Create instance of class 'Character'.
    character = char.Character()
    # Set initial state.
    state = "title_screen"
    # Create dict for GUI elements.
    gui_elements = {}

    # Loop to keep Pygame running and responsive during migration
    while True:
        screen.fill(pg_settings.bg_color)
        state = mf.handle_events(character, state, gui_elements)

        if state == "title_screen":
            mf.show_title_screen(screen)
        elif state == "main_menu":
            # Instantiate elements for main menu and populate dict 'gui_elements'.
            custom = so.TextField(screen, "Custom Character")
            random = so.TextField(screen, "Random Character")
            gui_elements["custom"] = custom
            gui_elements["random"] = random

            mf.show_menu(screen, gui_elements)

        pygame.display.flip()


run_character_creator()
