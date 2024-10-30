import pygame
import sys
import character_creation_functions as cf
"""Contains event handler functions."""


def main_events(screen, state, gui_elements, mouse_pos):
    """Check and handle pygame events for 'run_character_creator()' in 'main.py'. Set and return 'state'"""

    # Hashable dict to optimize state checking and improve performance.
    states_dict = {
        "title_screen": True,
        "main_menu": True,
    }

    if state in states_dict.keys():

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "title_screen":
                if event.type == pygame.KEYUP:
                    state = "main_menu"
                elif event.type == pygame.MOUSEBUTTONUP:
                    if screen.get_rect().collidepoint(mouse_pos):
                        state = "main_menu"

            elif state == "main_menu":
                if event.type == pygame.MOUSEBUTTONUP:
                    if gui_elements["custom"].button_rect.collidepoint(mouse_pos):
                        state = "set_abilities"

                    if gui_elements["random"].button_rect.collidepoint(mouse_pos):
                        state = "random_character"

    return state


def custom_character_events(state, character, race_list, class_list, gui_elements, mouse_pos):
    """Check and handle events in function 'custom_character()' in 'main_functions.py' and return 'state'."""

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "show_abilities":
            if event.type == pygame.MOUSEBUTTONUP:
                if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "main_menu"

                if gui_elements["reroll_button"].button_rect.collidepoint(mouse_pos):
                    state = "set_abilities"

                if gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                    # Set and return available races/classes and state after confirmation of ability scores.
                    race_list, class_list = cf.get_race_class_lists(character)
                    state = "race_class_selection"

        elif state == "race_class_selection":
            if event.type == pygame.MOUSEBUTTONUP:
                if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "show_abilities"

                if gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                    state = "custom_character_4"

        else:
            pass

    return race_list, class_list, state
