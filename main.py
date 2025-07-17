"""
Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality.
"""
import pygame

import core.state_manager as sm
from core.settings import settings

from gui.shared_data import ui_shared_data as uisd
from gui.ui_registry import initialize_ui_registry


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
    uisd.ui_registry = initialize_ui_registry(screen)

    return screen, clock


def run_character_creator() -> None:
    """Start the character creator."""

    # Initialize Pygame, screen, clock and GUI elements.
    screen, clock = initialize_character_creator()

    # Set initial state.
    state: str = "title_screen"
    # Set of states for character creation.
    main_states: set[str] = {"title_screen", "pre_main_menu", "main_menu", "settings_screen", "init_credits", "credits",
                             "character_menu"}
    save_load_states: set[str] = {"init_save_load_screen", "save_load_screen", "char_not_saved", "char_delete",
                                  "char_overwrite"}
    custom_character_states: set[str] = {"set_abilities", "show_abilities", "race_class_selection", "name_character",
                                         "spell_selection", "language_selection", "select_starting_money",
                                         "custom_input_money",
                                         "creation_complete"}
    random_character_states: set[str] = {"random_character", "set_random_money", "name_random_character"}
    character_sheet_states: set[str] = {"init_character_sheet", "character_sheet", "sheet_confirmation"}

    # Start main loop.
    while True:
        # Keep track of mouse position.
        mouse_pos = pygame.mouse.get_pos()

        # Blit background image to screen.
        screen.blit(uisd.ui_registry["background_image"], (0, 0))

        # Main states.
        if state in main_states:
            state = sm.main_state_manager(screen, state, mouse_pos)
        elif state in save_load_states:
            state = sm.save_load_screen_state_manager(screen, state, mouse_pos)

        # Character creation states.
        elif state in custom_character_states:
            state = sm.custom_character_state_manager(screen, state, mouse_pos)
        elif state in random_character_states:
            state = sm.random_character_state_manager(screen, state, mouse_pos)
        elif state in character_sheet_states:
            state = sm.character_sheet_state_manager(screen, state, mouse_pos)

        pygame.display.flip()
        clock.tick(settings.frame_rate)


if __name__ == "__main__":
    run_character_creator()
