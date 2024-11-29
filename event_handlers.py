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


def custom_character_events(state, character, possible_characters, gui_elements, mouse_pos, selected_race=None, selected_class=None,
                            character_name=None):
    """Check and handle events in function 'custom_character()' in 'main_functions.py' and return 'state'."""

    # Hashable dict to optimize state checking and improve performance.
    states_dict = {
        "show_abilities": True,
        "race_class_selection": True,
        "name_character": True,
    }

    if state in states_dict.keys():

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
                        possible_characters = cf.build_possible_characters_list(race_list, class_list)
                        state = "race_class_selection"

            elif state == "race_class_selection":
                if event.type == pygame.MOUSEBUTTONUP:
                    if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                        state = "show_abilities"

                    # Only continue if race AND class are selected.
                    if selected_race and selected_class:
                        if gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                            # Set race, class and their specific values in character object after confirmation.
                            character.set_race(selected_race.text)
                            character.set_class(selected_class.text)
                            cf.set_character_values(character)
                            state = "name_character"
                    else:
                        pass

            elif state == "name_character":
                character_name.update(pygame.event.get())

                if event.type == pygame.MOUSEBUTTONUP:
                    if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                        state = "race_class_selection"

                    else:
                        pass

            else:
                pass

    return possible_characters, state
