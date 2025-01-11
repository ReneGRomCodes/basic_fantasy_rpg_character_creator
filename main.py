import pygame
import core.main_functions as mf
import gui.gui as gui
import core.event_handlers as eh
from core.settings import Settings
from gui.gui_elements import initialize_screen_elements
from gui.character_sheet.cs_elements import initialize_cs_elements
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def run_character_creator():
    """Initialize Pygame, create a window, instantiate character and start the character creator."""
    # Initialize pygame and create a window.
    pygame.init()
    settings = Settings()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Basic Fantasy RPG Character Creator")

    # Initialize dicts with GUI elements. See package 'gui' for details.
    gui_elements = initialize_screen_elements(screen)
    # Elements for character sheet.
    cs_elements = initialize_cs_elements(screen, gui_elements)

    # Set initial state.
    state = "title_screen"
    # Set of states for character creation.
    custom_character_states = {"set_abilities", "show_abilities", "race_class_selection", "name_character",
                               "set_starting_money", "custom_input_money", "creation_complete"}
    random_character_state = {"random_character", "set_random_money", "name_random_character"}

    # Start main loop.
    while True:
        # Keep track of mouse position.
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(settings.bg_color)
        state = eh.main_events(screen, state, gui_elements, mouse_pos)

        if state == "title_screen":
            gui.show_title_screen(screen, gui_elements)
        elif state == "main_menu":
            gui.show_menu(screen, gui_elements, mouse_pos)
        elif state in custom_character_states:
            state = mf.custom_character(screen, state, gui_elements, mouse_pos)
        elif state in random_character_state:
            state = mf.random_character(screen, state, gui_elements, mouse_pos)
        elif state == "character_sheet":
            mf.show_character_sheet(screen, cs_elements, gui_elements)

        pygame.display.flip()
        clock.tick(30)


run_character_creator()
