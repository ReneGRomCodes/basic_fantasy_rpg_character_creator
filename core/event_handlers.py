import pygame
import sys
import core.functions as func
from character_creation_functions import build_character_sheet
"""Contains event handler functions."""


def main_events(screen, state, gui_elements, mouse_pos):
    """Check and handle main pygame events for 'run_character_creator()' in 'main.py'. Set and return 'state'.
    ARGS:
        screen: PyGame window.
        state: program state.
        gui_elements: dict of GUI elements.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state: program state.
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "title_screen":
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP and screen.get_rect().collidepoint(mouse_pos):
                state = "main_menu"

        elif state == "main_menu":
            if event.type == pygame.MOUSEBUTTONUP:
                if gui_elements["start_button"].button_rect.collidepoint(mouse_pos):
                    state = "character_menu"

                if gui_elements["settings_button"].button_rect.collidepoint(mouse_pos):
                    state = "settings_screen"

                if gui_elements["credits_button"].button_rect.collidepoint(mouse_pos):
                    state = "credits"

        elif state == "settings_screen":
            if event.type == pygame.MOUSEBUTTONUP:
                if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "main_menu"

        elif state == "credits":
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP and screen.get_rect().collidepoint(mouse_pos):
                state = "main_menu"

        elif state == "character_menu":
            if event.type == pygame.MOUSEBUTTONUP:
                if gui_elements["custom"].button_rect.collidepoint(mouse_pos):
                    state = "set_abilities"

                if gui_elements["random"].button_rect.collidepoint(mouse_pos):
                    state = "random_character"

                if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "main_menu"

    return state


def settings_screen_events(state, gui_elements, mouse_pos):
    """Check and handle events in function 'settings_screen()' in 'main_functions.py' and return state.
    ARGS:
        state: program state.
        gui_elements: dict of GUI elements.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state: program state.
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                state = "main_menu"

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
    states_set = {"show_abilities", "race_class_selection", "set_starting_money", "creation_complete"}

    if state in states_set:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "show_abilities":
                if event.type == pygame.MOUSEBUTTONUP:
                    if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                        state = "character_menu"

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

            elif state == "creation_complete":
                if event.type == pygame.MOUSEBUTTONUP:
                    if gui_elements["show_character_sheet"].button_rect.collidepoint(mouse_pos):
                        build_character_sheet(character)  # TODO Character sheet in console for checks. Remove when done.
                        state = "initialize_character_sheet"

    return possible_characters, state


"""Event handlers for screens where pygame_textinput library is used so 'pygame.event.get()' can be split between pygame
events and pygame_textinput events."""

def naming_character_events(state, character, gui_elements, mouse_pos):
    """Check and handle text input field events in functions 'custom_character()' and 'random_character' for each naming
    character state.
    ARGS:
        state: program state. Entry and exit state differs based on custom or random character creation.
        character: instance of class 'Character'.
        gui_elements: dict of GUI elements.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state: program state
    """
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

        if event.type == pygame.MOUSEBUTTONUP:
            if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                # Different state value is checked and set depending on whether custom or random character is created.
                character.reset_character()
                if state == "name_character":
                    state = "race_class_selection"
                elif state == "name_random_character":
                    # Import and call function to reset "messy globals" in 'main_functions.py' before returning to main
                    # menu. Not a pretty solution, but it resolves the freezing issue when coming back from the naming
                    # screen.
                    from core.main_functions import fix_my_messy_globals
                    fix_my_messy_globals()
                    state = "character_menu"

            if gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                character.set_name(character_name_input.manager.value)
                # Different state value is checked and set depending on whether custom or random character is created.
                if state == "name_character":
                    state = "set_starting_money"
                elif state == "name_random_character":
                    state = "creation_complete"

    return state


def custom_starting_money_events(state, character, gui_elements, mouse_pos):
    """Check and handle text input field events in function 'custom_character()' for state 'custom_input_money' in
    'main_functions.py'.
        ARGS:
        state: program state. Entry and exit state differs based on custom or random character creation.
        character: instance of class 'Character'.
        gui_elements: dict of GUI elements.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state: program state
    """
    # Assign 'pygame_textinput' instance stored in dict 'gui_elements' to variable.
    starting_money_input = gui_elements["money_amount_input"][0]

    # Set of valid keys for numeric only input and list for filtered events to be passed to the input field.
    valid_keys = {pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                  pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
                  pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4,
                  pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9,
                  pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_LEFT, pygame.K_RIGHT}
    filtered_keys = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Allow only text input with numeric keys and populate 'filtered_key' with valid inputs.
        if event.type == pygame.KEYDOWN and event.key in valid_keys:
            filtered_keys.append(event)

        if event.type == pygame.MOUSEBUTTONUP:
            if gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                state = "name_character"

            if gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                # Set characters starting money to '0' if input field is left empty.
                if starting_money_input.manager.value:
                    character.money = int(starting_money_input.manager.value)
                else:
                    character.money = 0
                state = "creation_complete"

    # Check and update events for 'pygame_textinput' instance 'starting_money_input'
    starting_money_input.update(filtered_keys)

    return state
