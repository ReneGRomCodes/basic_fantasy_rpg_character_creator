import pygame
import core.main_functions as mf
import gui.gui as gui
import core.event_handlers as eh
from core.settings import Settings
from gui.gui_elements import initialize_screen_elements
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
    gui_elements = initialize_screen_elements(screen, settings)
    # Create placeholder variable for later 'CharacterSheet' class object.
    cs_sheet = None

    # Set initial state.
    state = "title_screen"
    # Set of states for character creation.
    main_states = {"title_screen", "main_menu", "character_menu"}
    custom_character_states = {"set_abilities", "show_abilities", "race_class_selection", "name_character",
                               "set_starting_money", "custom_input_money", "creation_complete"}
    random_character_state = {"random_character", "set_random_money", "name_random_character"}

    # Start main loop.
    while True:
        # Keep track of mouse position.
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(settings.bg_color)

        # Main event handler.
        if state in main_states:
            state = eh.main_events(screen, state, gui_elements, mouse_pos)

        # Main states.
        if state == "title_screen":
            gui.show_title_screen(screen, gui_elements)
        elif state == "main_menu":
            gui.show_main_menu(screen, gui_elements, mouse_pos)
        # Character creation states.
        elif state == "character_menu":
            gui.show_character_menu(screen, gui_elements, mouse_pos)
        elif state in custom_character_states:
            state = mf.custom_character(screen, state, gui_elements, mouse_pos)
        elif state in random_character_state:
            state = mf.random_character(screen, state, gui_elements, mouse_pos)
        # Character sheet states.
        elif state == "initialize_character_sheet":
            cs_sheet, state = mf.initialize_character_sheet(screen, gui_elements)
        elif state == "character_sheet":
            cs_sheet.show_character_sheet_screen()

        pygame.display.flip()
        clock.tick(30)


run_character_creator()
