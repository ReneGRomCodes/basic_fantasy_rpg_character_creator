import pygame
import main_functions as mf
import character_model as char
import event_handlers as eh
from settings import Settings
from gui.gui_elements import initialize_screen_elements
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def run_character_creator():
    """Initialize Pygame, create a window, instantiate character and start the character creator."""
    # Initialize pygame and create a window.
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Basic Fantasy RPG Character Creator")

    # Create instance of class 'Character'.
    character = char.Character()
    # Variables for character creation.
    possible_characters = []
    selected_race = None
    selected_class = None

    # Set initial state.
    state = "title_screen"
    # Initialize GUI elements.
    gui_elements = initialize_screen_elements(screen)

    # Start main loop.
    while True:
        # Keep track of mouse position.
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(settings.bg_color)
        state = eh.main_events(screen, state, gui_elements, mouse_pos)

        if state == "title_screen":
            mf.show_title_screen(screen, gui_elements)
        elif state == "main_menu":
            mf.show_menu(screen, gui_elements, mouse_pos)
        elif state in ["set_abilities", "show_abilities", "race_class_selection", "name_character"]:
            possible_characters, state, selected_race, selected_class = mf.custom_character(screen, state, character,
                                                                                           possible_characters, selected_race,
                                                                                           selected_class, gui_elements,
                                                                                           mouse_pos)
        elif state == "random_character":
            mf.random_character(character)

        pygame.display.flip()


run_character_creator()
