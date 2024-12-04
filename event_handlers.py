import pygame
import sys
import functions as func
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


def custom_character_events(state, character, possible_characters, gui_elements, mouse_pos, selected_race=None, selected_class=None):
    """Check and handle events in function 'custom_character()' in 'main_functions.py' and return 'state'."""

    # Hashable dict to optimize state checking and improve performance.
    states_dict = {
        "show_abilities": True,
        "race_class_selection": True,
        "set_starting_money": True
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
                        race_list, class_list = func.get_race_class_lists(character)
                        possible_characters = func.build_possible_characters_list(race_list, class_list)
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
                            func.set_character_values(character)
                            state = "name_character"
                    else:
                        pass

            elif state == "set_starting_money":
                if event.type == pygame.MOUSEBUTTONUP:
                    if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                        state = "name_character"
                    else:
                        pass

            else:
                pass

    return possible_characters, state


def naming_character_events(state, character, character_name_input, gui_elements, mouse_pos):
    """Check and handle text input field events in function 'custom_character()' for state 'character_name_input' in
    'main_functions.py' and return new 'state'."""
    # Get pygame events and assign it to variable to be shared between 'pygame_textinput' instance and the for-loop.
    events = pygame.event.get()

    # Check and update events for 'pygame_textinput' instance 'character_name_input' before other events are checked.
    character_name_input.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check of variable 'state' actually unnecessary. Left in for clarity when reading the code.
        if state == "name_character":
            if event.type == pygame.MOUSEBUTTONUP:
                if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    character.reset_character()
                    state = "race_class_selection"

                if gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                    character.set_name(character_name_input.manager.value)
                    state = "set_starting_money"

                else:
                    pass

    return state
