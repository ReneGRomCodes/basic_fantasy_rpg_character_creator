import pygame
import core.state_manager as sm
from core.settings import settings
from gui.shared_data import ui_shared_data as uisd
from gui.gui_elements import initialize_screen_elements
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def initialize_character_creator() -> tuple[pygame.Surface, pygame.time.Clock]:
    """Initialize Pygame, settings, screen, and GUI elements."""
    # Initialize pygame.
    pygame.init()
    # Set default values for imported instance 'settings' from module 'core.settings'.
    settings.set_default()
    # Create Clock object and pygame window.
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(settings.screen_size, pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption("Basic Fantasy RPG Character Creator")
    # Initialize dict with GUI elements within module 'gui/shared_data.py'. See class 'UISharedData' and package 'gui'
    # for details.
    uisd.gui_elements = initialize_screen_elements(screen)

    return screen, clock


def run_character_creator() -> None:
    """Start the character creator."""

    # Initialize Pygame, screen, clock and GUI elements.
    screen, clock = initialize_character_creator()

    # Set initial state.
    state: str = "title_screen"
    # Set of states for character creation.
    main_states: set[str] = {"title_screen", "pre_main_menu", "main_menu", "init_credits", "credits", "character_menu",
                             "init_character_sheet", "character_sheet"}
    custom_character_states: set[str] = {"set_abilities", "show_abilities", "race_class_selection", "name_character",
                                         "spell_selection", "language_selection", "select_starting_money",
                                         "custom_input_money",
                                         "creation_complete"}
    random_character_states: set[str] = {"random_character", "set_random_money", "name_random_character"}

    # Start main loop.
    while True:
        # Keep track of mouse position.
        mouse_pos = pygame.mouse.get_pos()

        # Blit background image to screen.
        screen.blit(uisd.gui_elements["background_image"], (0, 0))

        # Main states.
        if state in main_states:
            state = sm.main_state_manager(screen, state, mouse_pos)
        # Settings state.
        elif state == "settings_screen":
            state = sm.settings_screen(screen, state, mouse_pos)

        # Character creation states.
        elif state in custom_character_states:
            state = sm.custom_character(screen, state, mouse_pos)
        elif state in random_character_states:
            state = sm.random_character(screen, state, mouse_pos)

        pygame.display.flip()
        clock.tick(settings.frame_rate)


if __name__ == "__main__":
    run_character_creator()
