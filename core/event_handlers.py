import pygame
import sys
import core.rules as rls
from core.shared_data import shared_data as sd
from gui.shared_data import ui_shared_data as uisd
"""Contains event handler functions."""

"""
                           SCREENS FLOW CHART:

                             ABILITY SCORES
                                    │
                                    V
                          RACE/CLASS SELECTION
                                    │
                                    +───────────────────────────┐
                                    │                           │
                         --if magic-using class--    --"language_selection"--
                                    │                --is only displayed if--
                                    V               --intelligence bonus > 0,--
                              SPELL SELECTION    --but state still passed through--
                                    │              --to set default languages--
                                    V                           │
                            LANGUAGE SELECTION <────────────────┘
                                    │
                                    V
                              NAMING SCREEN
                                    │
                                    V
                             MONEY SELECTION
                                    │
                                    V
                            CREATION COMPLETE
                                    │
                                    V
                             CHARACTER SHEET
"""


def main_events(screen, state: str, mouse_pos) -> str:
    """Check and handle main pygame events for 'run_character_creator()' in 'main.py'. Set and return 'state'.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Ensures screen specific UI elements are positioned only once per screen appearance and reset alpha transparency
        # for 'continue' and 'back' buttons.
        handle_screen_switch_reset(screen, event, mouse_pos)

        if state == "title_screen":
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP and screen.get_rect().collidepoint(mouse_pos)\
                    and uisd.gui_elements["title_screen_fields"][3].finished:
                state = "pre_main_menu"

        elif state == "main_menu":
            if event.type == pygame.MOUSEBUTTONUP:
                if uisd.gui_elements["start_button"].button_rect.collidepoint(mouse_pos):
                    state = "character_menu"

                if uisd.gui_elements["menu_buttons"][0].button_rect.collidepoint(mouse_pos):
                    # Set load-only mode for save/load screen when accessing it from main menu.
                    uisd.load_only_flag = True
                    # Event switches to state 'init_save_load_screen', which creates 'SaveLoadScreen' object before
                    # proceeding to final 'save_load_screen' state from within main state manager.
                    state = "init_save_load_screen"

                if uisd.gui_elements["menu_buttons"][1].button_rect.collidepoint(mouse_pos):
                    state = "settings_screen"

                if uisd.gui_elements["menu_buttons"][2].button_rect.collidepoint(mouse_pos):
                    # Event switches to state 'init_credits', which creates 'Credits' object before proceeding to final
                    # 'credits' state from within main state manager.
                    state = "init_credits"

                if uisd.gui_elements["menu_buttons"][3].button_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        elif state == "save_load_screen":
            if event.type == pygame.MOUSEBUTTONUP:
                if sd.save_load_screen.save_button.button_rect.collidepoint(mouse_pos):
                    # Save character and return to character sheet.
                    state = sd.save_load_screen.save_character(state)

                if sd.save_load_screen.load_button.button_rect.collidepoint(mouse_pos):
                    # Load character and return to character sheet.
                    state = sd.save_load_screen.load_character(state)

                if sd.save_load_screen.exit_button.button_rect.collidepoint(mouse_pos):
                    # Select state based on previously set screen mode flag.
                    if uisd.load_only_flag:
                        state = "pre_main_menu"
                    else:
                        state = "init_character_sheet"

        elif state == "settings_screen":
            if event.type == pygame.MOUSEBUTTONUP:
                if uisd.gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "main_menu"

        elif state == "credits":
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP and screen.get_rect().collidepoint(mouse_pos):
                state = "main_menu"

        elif state == "character_menu":
            if event.type == pygame.MOUSEBUTTONUP:
                if uisd.gui_elements["custom"].button_rect.collidepoint(mouse_pos):
                    state = "set_abilities"

                if uisd.gui_elements["random"].button_rect.collidepoint(mouse_pos):
                    state = "random_character"

                if uisd.gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "main_menu"

        elif state == "character_sheet":
            if event.type == pygame.MOUSEBUTTONUP:
                if sd.cs_sheet.save_load_button.button_rect.collidepoint(mouse_pos):
                    # Set save/load mode for save/load screen when accessing it from character sheet.
                    uisd.load_only_flag = False
                    # Event switches to state 'init_save_load_screen', which creates 'SaveLoadScreen' object before
                    # proceeding to final 'save_load_screen' state from within main state manager.
                    state = "init_save_load_screen"

                if sd.cs_sheet.main_menu_button.button_rect.collidepoint(mouse_pos):
                    state = "pre_main_menu"

    return state


def custom_character_events(screen, state: str, mouse_pos) -> str:
    """Check and handle events in function 'custom_character()' in 'state_manager.py' and return 'state'.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Ensures screen-specific UI elements are positioned only once per screen appearance and reset alpha transparency
        # for 'continue' and 'back' buttons.
        handle_screen_switch_reset(screen, event, mouse_pos)

        if state == "show_abilities":
            if event.type == pygame.MOUSEBUTTONUP:
                if uisd.gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "character_menu"

                if uisd.gui_elements["reroll_button"].button_rect.collidepoint(mouse_pos):
                    state = "set_abilities"

                if uisd.gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                    # Set and return available races/classes and state after confirmation of ability scores.
                    sd.possible_characters = rls.build_possible_characters_list(sd.character)
                    # Check intelligence bonus to set 'language_flag' attribute in instance of 'shared_data' (GUI) to
                    # decide if switch to state 'language_selection' should happen at any point.
                    uisd.language_flag = rls.set_language_flag(sd.character)
                    state = "race_class_selection"

        elif state == "race_class_selection":
            if event.type == pygame.MOUSEBUTTONUP:
                # Race/class selection logic.
                for option in uisd.gui_elements["active_races"] + uisd.gui_elements["active_classes"]:
                    if option.interactive_rect.collidepoint(mouse_pos):
                        sd.select_race_class(mouse_pos)
                if uisd.gui_elements["reset_button"].button_rect.collidepoint(mouse_pos):
                    # Reset selection.
                    sd.select_race_class(mouse_pos, reset=True)

                if uisd.gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "show_abilities"

                # Only continue if race AND class are selected.
                if sd.selected_race and sd.selected_class:
                    if uisd.gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                        # Set race, class and their specific values in character object after confirmation.
                        sd.character.set_race(sd.selected_race.text)
                        sd.character.set_class(sd.selected_class.text)
                        sd.character.set_character_values()
                        # Check conditions to decide which screen to show.
                        if sd.character.class_name in sd.magic_classes:
                            state = "spell_selection"
                        else:
                            state = "language_selection"

        # Magic-User specific state for spell selection.
        elif state == "spell_selection":
            if event.type == pygame.MOUSEBUTTONUP:
                # Spell selection logic.
                for option in uisd.gui_elements["spell_fields"]:
                    if option.interactive_rect.collidepoint(mouse_pos):
                        sd.select_spell(uisd.gui_elements["spell_fields"], mouse_pos)

                if uisd.gui_elements["reset_button"].button_rect.collidepoint(mouse_pos):
                    # Reset selection.
                    sd.select_spell(uisd.gui_elements["spell_fields"], mouse_pos, reset=True)
                if uisd.gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "race_class_selection"

                if uisd.gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                    # Add selected spells to character.
                    sd.character.set_starting_spell(uisd.gui_elements["spell_fields"])
                    state = "language_selection"

        elif state == "language_selection":
            # Set default languages and switch to next state if conditions to display language selection are not met.
            if not uisd.language_flag:
                sd.character.set_languages(uisd.gui_elements["lang_fields"])
                state = "name_character"

            if event.type == pygame.MOUSEBUTTONUP:
                # Language selection logic.
                for option in uisd.gui_elements["lang_fields"]:
                    if option.interactive_rect.collidepoint(mouse_pos):
                        sd.select_languages(uisd.gui_elements["lang_fields"], mouse_pos)
                if uisd.gui_elements["reset_button"].button_rect.collidepoint(mouse_pos):
                    # Reset selection.
                    sd.select_languages(uisd.gui_elements["lang_fields"], mouse_pos, reset=True)

                if uisd.gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    if sd.character.class_name in sd.magic_classes:
                        state = "spell_selection"
                    else:
                        state = "race_class_selection"

                if uisd.gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                    # Set selected languages in character object after confirmation.
                    sd.character.set_languages(uisd.gui_elements["lang_fields"])
                    state = "name_character"

        elif state == "select_starting_money":
            # Base state for starting money screen.
            if event.type == pygame.MOUSEBUTTONUP:
                if uisd.gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                    state = "name_character"

                # Allow to continue to next state if 'random_money' is 'True' and the dice roll is complete or switch
                # state for user input if 'custom_money' is 'True'.
                if sd.random_money_flag and uisd.dice_roll_complete:
                    if uisd.gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                        # Set starting money to 'sd.starting_money' if 'random_money' is 'True'.
                        sd.character.money = sd.starting_money
                        state = "creation_complete"
                if sd.custom_money_flag:
                    # Special state to handle money input field functionality.
                    state = "custom_input_money"

        elif state == "creation_complete":
            if event.type == pygame.MOUSEBUTTONUP:
                if uisd.gui_elements["show_character_sheet"].button_rect.collidepoint(mouse_pos):
                    # Reset text input fields after character creation is finished to ensure next character creation
                    # process starts with empty input fields.
                    reset_input_fields()
                    state = "init_character_sheet"

    return state


"""Event handlers for screens where pygame_textinput library is used so 'pygame.event.get()' can be split between pygame
events and pygame_textinput events."""

def naming_character_events(screen, state: str, mouse_pos) -> str:
    """Check and handle text input field events in functions 'custom_character()' and 'random_character' for each naming
    character state.
    ARGS:
        screen: PyGame window.
        state: program state. Entry and exit state differ based on custom or random character creation.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    # Assign 'pygame_textinput' instance stored in dict 'gui_elements' to variable.
    character_name_input = uisd.gui_elements["character_name_input"][0]
    # Get pygame events and assign it to variable to be shared between 'pygame_textinput' instance and the for-loop.
    events = pygame.event.get()

    # Check and update events for 'pygame_textinput' instance 'character_name_input' before other events are checked.
    character_name_input.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Ensures screen-specific UI elements are positioned only once per screen appearance and reset alpha transparency
        # for 'continue' and 'back' buttons.
        handle_screen_switch_reset(screen, event, mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if uisd.gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                # Different state value is checked and set depending on whether custom or random character is created.
                sd.character.reset_character()
                if state == "name_character":
                    # Check conditions to decide which state to set.
                    if uisd.language_flag:
                        state = "language_selection"
                    elif sd.character.class_name in sd.magic_classes:
                        state = "spell_selection"
                    else:
                        state = "race_class_selection"

                elif state == "name_random_character":
                    # Call method to reset shared data before returning to previous menu.
                    # Not a pretty solution, but it resolves the freezing issue when coming back from the naming screen.
                    sd.shared_data_janitor()
                    state = "character_menu"

            if uisd.gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                sd.character.set_name(character_name_input.manager.value)
                # Different state value is checked and set depending on whether custom or random character is created.
                if state == "name_character":
                    state = "select_starting_money"
                elif state == "name_random_character":
                    state = "creation_complete"

    return state


def custom_starting_money_events(screen, state: str, mouse_pos) -> str:
    """Check and handle text input field events in function 'custom_character()' for state 'custom_input_money' in
    'state_manager.py'.
    ARGS:
        screen: PyGame window.
        state: program state. Entry and exit state differ based on custom or random character creation.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    # Assign 'pygame_textinput' instance stored in dict 'gui_elements' to variable.
    starting_money_input = uisd.gui_elements["money_amount_input"][0]

    # Set of valid keys for numeric-only input.
    valid_keys: set = {pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                       pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9,
                       pygame.K_KP0, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4,
                       pygame.K_KP5, pygame.K_KP6, pygame.K_KP7, pygame.K_KP8, pygame.K_KP9,
                       pygame.K_DELETE, pygame.K_BACKSPACE, pygame.K_LEFT, pygame.K_RIGHT}
    # List for filtered events to be passed to the input field.
    filtered_keys: list = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Ensures screen-specific UI elements are positioned only once per screen appearance and reset alpha transparency
        # for 'continue' and 'back' buttons.
        handle_screen_switch_reset(screen, event, mouse_pos)

        # Allow only text input with numeric keys and populate 'filtered_key' with valid inputs.
        if event.type == pygame.KEYDOWN and event.key in valid_keys:
            filtered_keys.append(event)

        if event.type == pygame.MOUSEBUTTONUP:
            if uisd.gui_elements["back_button"].button_rect.collidepoint(mouse_pos):
                state = "name_character"

            if uisd.gui_elements["continue_button"].button_rect.collidepoint(mouse_pos):
                # Set characters starting money to '0' if input field is left empty.
                if starting_money_input.manager.value:
                    sd.character.money = int(starting_money_input.manager.value)
                else:
                    sd.character.money = 0
                state = "creation_complete"

            if uisd.gui_elements["starting_money_choices"][0].button_rect.collidepoint(mouse_pos):
                # Reset input field to empty value when switching from 'custom amount' to 'random amount', and set state
                # to basic "select_starting_money" for money selection screen.
                starting_money_input.manager.value = ""
                state = "select_starting_money"

    # Check and update events for 'pygame_textinput' instance 'starting_money_input'
    starting_money_input.update(filtered_keys)

    return state


def handle_screen_switch_reset(screen, event, mouse_pos) -> None:
    """Check for input events that switch screens, reset position flag for screen-specific UI placement, and reset alpha
    values of certain UI elements. Called in every event handler 'for event in pygame.event.get()' loop.
    ARGS:
        screen: PyGame window.
        event: PyGame event from for-loop in event handler.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """

    # Check for any 'KEYUP' or 'MOUSEBUTTONUP' event. While this leads to the block being executed every time an event
    # occurs, it trades this redundancy for overall maintainability.
    if (event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP) and screen.get_rect().collidepoint(mouse_pos):
        uisd.reset_position_flag()
        uisd.gui_elements["continue_button"].fade_alpha = 0
        uisd.gui_elements["back_button"].fade_alpha = 0


def reset_input_fields() -> None:
    """Reset text input fields to ensure each character creation process starts with empty input fields. Called in state
    'creation_complete' before initializing character sheet screen."""
    uisd.gui_elements["character_name_input"][0].manager.value = ""
    uisd.gui_elements["money_amount_input"][0].manager.value = ""
