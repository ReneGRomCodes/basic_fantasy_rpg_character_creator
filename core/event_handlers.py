import pygame
import sys
import core.functions as func
"""Contains event handler functions."""


def main_events(screen, state, gui_elements, mouse_pos):
    """Check and handle pygame events for 'run_character_creator()' in 'main.py'. Set and return 'state'"""

    # Hashable set to optimize state checking and improve performance.
    states_set = {"title_screen", "main_menu"}

    if state in states_set:

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


def custom_character_events(state, character, gui_elements, mouse_pos, possible_characters=None, context1=None,
                            context2=None, context3=None):
    """Check and handle events in function 'custom_character()' in 'main_functions.py' and return 'state'.
    ARGS:
        state: program state.
        character: instance of class 'Character'.
        gui_elements: dict of GUI elements.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
        possible_characters: list of possible race-class combinations. Default is 'None'.
            NOTE: arg must always be passed in function 'custom_character()' in 'main_functions.py' from state
            'race_class_selection' onwards to keep list stored and not have it reset to 'None'.
        context1: context specific argument whose role depends on current state.
        context2: context specific argument whose role depends on current state.
        context3: context specific argument whose role depends on current state.
    RETURNS:
        possible_characters: see arg above.
        state: program state.
    """

    # Hashable set to optimize state checking and improve performance.
    states_set = {"show_abilities", "race_class_selection", "set_starting_money"}

    if state in states_set:

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

                    # Only continue if race AND class are selected (context1=selected_race, context2=selected_class).
                    if context1 and context2:
                        if gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                            # Set race, class and their specific values in character object after confirmation.
                            character.set_race(context1.text)
                            character.set_class(context2.text)
                            func.set_character_values(character)
                            state = "name_character"
                    else:
                        pass

            elif state == "set_starting_money":
                if event.type == pygame.MOUSEBUTTONUP:
                    if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                        state = "name_character"

                    # Allow to continue to next state if 'context1' (random_money) is 'True' or switch state for user
                    # input if 'context2' (custom_money) is 'True'.
                    if context1:
                        if gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                            # Set starting money to int 'context3' (starting_money) if 'random_money' is 'True'.
                            character.money = context3
                            state = "creation_complete"
                    if context2:
                        state = "custom_input_money"
                    else:
                        pass

            elif state == "creation_complete":
                if event.type == pygame.MOUSEBUTTONUP:
                    if gui_elements["continue_to_character_sheet"].button_rect.collidpoint(mouse_pos):
                        state = "TODO"
                    else:
                        pass

            else:
                pass

    return possible_characters, state


"""Event handlers for screens where pygame_textinput library is used so event handling can be split between pygame events
and pygame_textinput events."""

def naming_character_events(state, character, gui_elements, mouse_pos):
    """Check and handle text input field events in function 'custom_character()' for state 'name_character' in
    'main_functions.py' and return new 'state'."""
    # Assign 'pygame_textinput' instance stored in dict 'gui_elements' to variable.
    character_name_input = gui_elements["character_name_input"][0]
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


def custom_starting_money_events(state, gui_elements, starting_money, mouse_pos):
    """Check and handle text input field events in function 'custom_character()' for state 'custom_money' in
    'main_functions.py' and return 'starting_money' and new 'state'."""
    # Assign 'pygame_textinput' instance stored in dict 'gui_elements' to variable.
    starting_money_input = gui_elements["money_amount_input"][0]

    # Get pygame events and assign it to variable to be shared between 'pygame_textinput' instance and the for-loop.
    events = pygame.event.get()

    # Check and update events for 'pygame_textinput' instance 'character_name_input' before other events are checked.
    starting_money_input.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Check of variable 'state' actually unnecessary. Left in for clarity when reading the code.
        if state == "custom_input_money":
            if event.type == pygame.MOUSEBUTTONUP:
                if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "name_character"

                if gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                    starting_money = starting_money_input.manager.value
                    state = "creation_complete"

    return starting_money, state
