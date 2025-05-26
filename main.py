import pygame
import core.state_manager as sm
from core.settings import settings
from gui.gui_elements import initialize_screen_elements
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def initialize_character_creator() -> tuple[pygame.Surface, pygame.time.Clock, dict]:
    """Initialize Pygame, settings, screen, and GUI elements."""
    # Initialize pygame.
    pygame.init()
    # Set default values for imported instance 'settings' from module 'core.settings'.
    settings.set_default()
    # Create Clock object and pygame window.
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(settings.screen_size, pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption("Basic Fantasy RPG Character Creator")

    # Initialize dict with GUI elements. See package 'gui' for details.
    gui_elements: dict = initialize_screen_elements(screen, settings)

    return screen, clock, gui_elements


def run_character_creator() -> None:
    """Start the character creator."""

    # Initialize Pygame, screen, clock and GUI elements.
    screen, clock, gui_elements = initialize_character_creator()

    # Set initial state.
    state: str = "title_screen"
    # Set of states for character creation.
    main_states: set[str] = {"title_screen", "pre_main_menu", "main_menu", "init_credits", "credits", "character_menu",
                             "init_character_sheet", "character_sheet"}
    custom_character_states: set[str] = {"set_abilities", "show_abilities", "init_race_class_selection",
                                         "race_class_selection", "name_character", "spell_selection",
                                         "select_starting_money", "custom_input_money", "creation_complete"}
    random_character_states: set[str] = {"random_character", "set_random_money", "name_random_character"}

    # Start main loop.
    while True:
        # Keep track of mouse position.
        mouse_pos = pygame.mouse.get_pos()

        # Blit background image to screen.
        screen.blit(gui_elements["background_image"], (0, 0))

        # Main states.
        if state in main_states:
            state = sm.main_state_manager(screen, state, gui_elements, mouse_pos)
        # Settings state.
        elif state == "settings_screen":
            gui_elements, state = sm.settings_screen(screen, state, gui_elements, mouse_pos)

        # Character creation states.
        elif state in custom_character_states:
            state = sm.custom_character(screen, state, gui_elements, mouse_pos)
        elif state in random_character_states:
            state = sm.random_character(screen, state, gui_elements, mouse_pos)

        pygame.display.flip()
        clock.tick(settings.frame_rate)


if __name__ == "__main__":
    run_character_creator()
