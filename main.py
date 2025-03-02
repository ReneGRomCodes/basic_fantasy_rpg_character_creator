import pygame
import core.state_manager as sm
from core.settings import Settings
from gui.settings_gui import SettingsGUI
from gui.gui_elements import initialize_screen_elements
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def run_character_creator():
    """Initialize Pygame, create a window, instantiate character and start the character creator."""
    # Initialize pygame.
    pygame.init()
    # Create settings object and initialize default values.
    settings = Settings()
    settings.set_default()
    # Create Clock object and pygame window.
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(settings.screen_size)
    pygame.display.set_caption("Basic Fantasy RPG Character Creator")

    # Initialize dicts with GUI elements. See package 'gui' for details.
    gui_elements = initialize_screen_elements(screen, settings)
    # Instantiate further GUI objects.
    settings_gui = SettingsGUI(screen, gui_elements)
    # Create placeholder variable for later 'CharacterSheet' class object.
    cs_sheet = None

    # Set initial state.
    state = "title_screen"
    # Set of states for character creation.
    main_states = {"title_screen", "main_menu", "init_credits", "credits", "character_menu"}
    custom_character_states = {"set_abilities", "show_abilities", "race_class_selection", "name_character",
                               "set_starting_money", "custom_input_money", "creation_complete"}
    random_character_state = {"random_character", "set_random_money", "name_random_character"}

    # Start main loop.
    while True:
        # Keep track of mouse position.
        mouse_pos = pygame.mouse.get_pos()

        screen.fill(settings.bg_color)


        # Main states.
        if state in main_states:
            state = sm.main_state_manager(screen, state, gui_elements, mouse_pos)
        # Settings state.
        elif state == "settings_screen":
            gui_elements, state = sm.settings_screen(screen, state, settings, settings_gui, gui_elements, mouse_pos)

        # Character creation states.
        elif state in custom_character_states:
            state = sm.custom_character(screen, state, gui_elements, mouse_pos)
        elif state in random_character_state:
            state = sm.random_character(screen, state, gui_elements, mouse_pos)

        # Character sheet states.
        elif state == "initialize_character_sheet":
            cs_sheet, state = sm.initialize_character_sheet(screen, gui_elements)
        elif state == "character_sheet":
            cs_sheet.show_character_sheet_screen()


        pygame.display.flip()
        clock.tick(30)


run_character_creator()
