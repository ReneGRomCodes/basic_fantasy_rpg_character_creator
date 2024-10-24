import pygame
import sys
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


def custom_character_events(state, gui_elements, mouse_pos):
    """Check and handle events in function 'custom_character()' in 'main_functions.py' and return 'state'."""

    if state == "show_abilities":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "main_menu"

                if gui_elements["reroll_button"].button_rect.collidepoint(mouse_pos):
                    state = "set_abilities"

                if gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                    state = "custom_character_3"

    else:
        pass

    return state
