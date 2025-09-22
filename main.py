"""
Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality.
"""
import pygame

import core.state_manager as sm
from core.settings import settings

from gui.shared_data import ui_shared_data as uisd
from gui.ui_registry import initialize_ui_registry


# Program states.
INITIAL_STATE: str = "title_screen"
MAIN_STATES: set[str] = {"title_screen", "pre_main_menu", "main_menu", "settings_screen", "init_credits", "credits",
                         "character_menu"}
SAVE_LOAD_STATES: set[str] = {"init_save_load_screen", "save_load_screen", "char_not_saved", "char_delete",
                              "char_overwrite"}
CUSTOM_CHARACTER_STATES: set[str] = {"set_abilities", "show_abilities", "race_class_selection", "name_character",
                                     "spell_selection", "language_selection", "select_starting_money",
                                     "custom_input_money", "confirm_character", "creation_complete"}
RANDOM_CHARACTER_STATES: set[str] = {"random_character", "set_random_money", "name_random_character"}
CHARACTER_SHEET_STATES: set[str] = {"init_character_sheet", "character_sheet", "sheet_confirmation"}


def initialize_character_creator() -> tuple[pygame.Surface, pygame.time.Clock]:
    """Initialize Pygame, settings, screen, and GUI elements."""
    pygame.init()
    settings.set_default()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(settings.screen_size, pygame.DOUBLEBUF | pygame.HWSURFACE)
    pygame.display.set_caption("Basic Fantasy RPG Character Creator")
    uisd.ui_registry = initialize_ui_registry(screen)

    return screen, clock


def run_character_creator() -> None:
    """Start the character creator."""
    screen, clock = initialize_character_creator()
    state = INITIAL_STATE

    while True:
        mouse_pos = pygame.mouse.get_pos()

        # Display background image based on program state.
        bg_image = uisd.ui_registry["title_background_image"] if state == "title_screen" else uisd.ui_registry["background_image"]
        screen.blit(bg_image, (0, 0))

        # Main states.
        if state in MAIN_STATES:
            state = sm.main_state_manager(screen, state, mouse_pos)
        elif state in SAVE_LOAD_STATES:
            state = sm.save_load_screen_state_manager(screen, state, mouse_pos)

        # Character creation states.
        elif state in CUSTOM_CHARACTER_STATES:
            state = sm.custom_character_state_manager(screen, state, mouse_pos)
        elif state in RANDOM_CHARACTER_STATES:
            state = sm.random_character_state_manager(screen, state, mouse_pos)
        elif state in CHARACTER_SHEET_STATES:
            state = sm.character_sheet_state_manager(screen, state, mouse_pos)

        pygame.display.flip()
        clock.tick(settings.frame_rate)


if __name__ == "__main__":
    run_character_creator()
