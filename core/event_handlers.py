"""
Contains event handler functions.
"""
import sys

import pygame

from gui.shared_data import ui_shared_data as uisd

import core.rules as rls
from .shared_data import shared_data as sd

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
    # Standard button rects.
    back_button = uisd.ui_registry["back_button"].button_rect
    # Main menu button rects.
    start_button = uisd.ui_registry["start_button"].button_rect
    load_button = uisd.ui_registry["menu_buttons"][0].button_rect
    settings_button = uisd.ui_registry["menu_buttons"][1].button_rect
    credits_button = uisd.ui_registry["menu_buttons"][2].button_rect
    quit_button = uisd.ui_registry["menu_buttons"][3].button_rect
    # Character creation menu button rects.
    custom_creation_button = uisd.ui_registry["custom"].button_rect
    random_creation_button = uisd.ui_registry["random"].button_rect

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        handle_screen_switch_reset(screen, event, mouse_pos)

        if state == "title_screen":
            if event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP and screen.get_rect().collidepoint(mouse_pos)\
                    and uisd.ui_registry["title_screen_fields"][3].finished:
                state = "pre_main_menu"

        elif state == "main_menu":
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.collidepoint(mouse_pos):
                    state = "character_menu"

                if load_button.collidepoint(mouse_pos):
                    uisd.load_only_flag = True
                    state = "init_save_load_screen"

                if settings_button.collidepoint(mouse_pos):
                    state = "settings_screen"

                if credits_button.collidepoint(mouse_pos):
                    state = "init_credits"

                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        elif state == "settings_screen":
            if event.type == pygame.MOUSEBUTTONUP:
                if back_button.collidepoint(mouse_pos):
                    state = "main_menu"

                # Window size selection logic.
                for option in sd.settings_gui.window_size_buttons:
                    if option.interactive_rect.collidepoint(mouse_pos):
                        sd.settings_gui.select_window_size(screen, mouse_pos)

        elif state == "credits":
            if (event.type == pygame.KEYUP or event.type == pygame.MOUSEBUTTONUP) and screen.get_rect().collidepoint(mouse_pos):
                state = "main_menu"

        elif state == "character_menu":
            if event.type == pygame.MOUSEBUTTONUP:
                if custom_creation_button.collidepoint(mouse_pos):
                    state = "set_abilities"

                if random_creation_button.collidepoint(mouse_pos):
                    state = "random_character"

                if back_button.collidepoint(mouse_pos):
                    state = "main_menu"

    return state


def save_load_events(screen, state: str, mouse_pos) -> str:
    """Check and handle events in function 'save_load_screen_state_manager()' in 'state_manager.py' and return 'state'.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    # Button rects.
    save_button = sd.save_load_screen.save_button.button_rect
    load_button = sd.save_load_screen.load_button.button_rect
    delete_button = sd.save_load_screen.delete_button.button_rect
    exit_button = sd.save_load_screen.exit_button.button_rect
    confirm_proceed_button = sd.save_load_screen.confirm_proceed_button.button_rect
    confirm_delete_button = sd.save_load_screen.confirm_delete_button.button_rect
    confirm_overwrite_button = sd.save_load_screen.confirm_overwrite_button.button_rect
    cancel_button = sd.save_load_screen.cancel_button.button_rect

    confirm_states: set[str] = {"char_not_saved", "char_delete", "char_overwrite"}

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        handle_screen_switch_reset(screen, event, mouse_pos)

        if state == "save_load_screen":
            if event.type == pygame.MOUSEBUTTONUP:
                # Save/load slot selection logic.
                for slot_id, slot in sd.save_load_screen.slots.items():
                    if slot.interactive_rect.collidepoint(mouse_pos):
                        sd.save_load_screen.select_character_slot(slot_id, slot)

                if save_button.collidepoint(mouse_pos):
                    state = sd.save_load_screen.save_character(state)

                if load_button.collidepoint(mouse_pos):
                    state = sd.save_load_screen.load_character()

                if delete_button.collidepoint(mouse_pos):
                    state = sd.save_load_screen.delete_character(state)

                if exit_button.collidepoint(mouse_pos):
                    if uisd.load_only_flag:
                        state = "pre_main_menu"
                    else:
                        state = "character_sheet"

        elif state in confirm_states:
            if event.type == pygame.MOUSEBUTTONUP:
                if cancel_button.collidepoint(mouse_pos):
                    state = "init_save_load_screen"

                if confirm_proceed_button.collidepoint(mouse_pos):
                    # Set 'is_saved' to 'True' to allow for loading of saved character if current one isn't saved.
                    sd.cs_sheet.is_saved = True
                    state = sd.save_load_screen.load_character()

                if confirm_delete_button.collidepoint(mouse_pos):
                    state = sd.save_load_screen.delete_character(state)

                if confirm_overwrite_button.collidepoint(mouse_pos):
                    state = sd.save_load_screen.save_character(state)

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
    # Button rects.
    continue_button = uisd.ui_registry["continue_button"].button_rect
    back_button = uisd.ui_registry["back_button"].button_rect
    reroll_button = uisd.ui_registry["reroll_button"].button_rect
    reset_button = uisd.ui_registry["reset_button"].button_rect
    show_sheet_button = uisd.ui_registry["show_character_sheet"].button_rect

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        handle_screen_switch_reset(screen, event, mouse_pos)

        if state == "show_abilities":
            if event.type == pygame.MOUSEBUTTONUP:
                if back_button.collidepoint(mouse_pos):
                    state = "character_menu"

                if reroll_button.collidepoint(mouse_pos):
                    state = "set_abilities"

                if continue_button.collidepoint(mouse_pos):
                    sd.possible_characters = rls.build_possible_characters_list(sd.character)
                    uisd.language_flag = rls.set_language_flag(sd.character)
                    state = "race_class_selection"

        elif state == "race_class_selection":
            if event.type == pygame.MOUSEBUTTONUP:
                # Race/class selection logic.
                for option in uisd.ui_registry["active_races"] + uisd.ui_registry["active_classes"]:
                    if option.interactive_rect.collidepoint(mouse_pos):
                        sd.select_race_class(option)

                if reset_button.collidepoint(mouse_pos):
                    sd.clear_race_class_selection()

                if back_button.collidepoint(mouse_pos):
                    state = "show_abilities"

                if sd.selected_race and sd.selected_class:
                    if continue_button.collidepoint(mouse_pos):
                        sd.character.set_race(sd.selected_race.text)
                        sd.character.set_class(sd.selected_class.text)
                        sd.character.set_character_values()
                        if sd.character.class_name in rls.CLASS_CATEGORIES["magic_classes"]:
                            state = "spell_selection"
                        else:
                            state = "language_selection"

        elif state == "spell_selection":
            if event.type == pygame.MOUSEBUTTONUP:
                # Spell selection logic.
                for option in uisd.ui_registry["spell_fields"]:
                    if option.interactive_rect.collidepoint(mouse_pos):
                        sd.select_spell(option)

                if back_button.collidepoint(mouse_pos):
                    state = "race_class_selection"

                if continue_button.collidepoint(mouse_pos):
                    sd.character.set_starting_spell(uisd.ui_registry["spell_fields"])
                    state = "language_selection"

        elif state == "language_selection":
            if event.type == pygame.MOUSEBUTTONUP:
                # Language selection logic.
                for option in uisd.ui_registry["lang_fields"]:
                    if option.interactive_rect.collidepoint(mouse_pos):
                        sd.select_languages(option)

                if reset_button.collidepoint(mouse_pos):
                    sd.clear_language_selection()

                if back_button.collidepoint(mouse_pos):
                    sd.clear_language_selection()
                    if sd.character.class_name in rls.CLASS_CATEGORIES["magic_classes"]:
                        state = "spell_selection"
                    else:
                        state = "race_class_selection"

                if continue_button.collidepoint(mouse_pos):
                    sd.character.set_languages(uisd.ui_registry["lang_fields"])
                    state = "name_character"

        elif state == "select_starting_money":
            if event.type == pygame.MOUSEBUTTONUP:
                if back_button.collidepoint(mouse_pos):
                    state = "name_character"

                if sd.random_money_flag and uisd.dice_roll_complete:
                    if continue_button.collidepoint(mouse_pos):
                        sd.character.money = sd.starting_money
                        state = "creation_complete"

                if sd.custom_money_flag:
                    state = "custom_input_money"

        elif state == "creation_complete":
            if event.type == pygame.MOUSEBUTTONUP:
                if show_sheet_button.collidepoint(mouse_pos):
                    uisd.reset_input_fields()
                    state = "init_character_sheet"

    return state


"""Event handlers for screens where pygame_textinput library is used so 'pygame.event.get()' can be split between pygame
events and pygame_textinput events."""

def naming_character_events(screen, state: str, mouse_pos) -> str:
    """Check and handle text input field events in functions 'custom_character()' and 'random_character()' for each
    naming character state.
    ARGS:
        screen: PyGame window.
        state: program state. Entry and exit state differ based on custom or random character creation.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    # Button rects.
    continue_button = uisd.ui_registry["continue_button"].button_rect
    back_button = uisd.ui_registry["back_button"].button_rect

    character_name_input = uisd.ui_registry["character_name_input"][0]
    events = pygame.event.get()
    character_name_input.update(events)

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        handle_screen_switch_reset(screen, event, mouse_pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if back_button.collidepoint(mouse_pos):
                sd.character.reset_character()
                if state == "name_character":
                    if uisd.language_flag:
                        state = "language_selection"
                    elif sd.character.class_name in rls.CLASS_CATEGORIES["magic_classes"]:
                        state = "spell_selection"
                    else:
                        state = "race_class_selection"

                elif state == "name_random_character":
                    # Call method to reset shared data before returning to previous menu.
                    # Not a pretty solution, but it resolves the freezing issue when coming back from the naming screen.
                    sd.shared_data_janitor()
                    state = "character_menu"

            if continue_button.collidepoint(mouse_pos):
                sd.character.set_name(character_name_input.manager.value)
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
    # Button rects.
    continue_button = uisd.ui_registry["continue_button"].button_rect
    back_button = uisd.ui_registry["back_button"].button_rect
    random_money_button = uisd.ui_registry["starting_money_choices"][0].button_rect

    starting_money_input = uisd.ui_registry["money_amount_input"][0]

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

        handle_screen_switch_reset(screen, event, mouse_pos)

        if event.type == pygame.KEYDOWN and event.key in valid_keys:
            filtered_keys.append(event)

        if event.type == pygame.MOUSEBUTTONUP:
            if back_button.collidepoint(mouse_pos):
                state = "name_character"

            if continue_button.collidepoint(mouse_pos):
                if starting_money_input.manager.value:
                    sd.character.money = int(starting_money_input.manager.value)
                else:
                    sd.character.money = 0
                state = "creation_complete"

            if random_money_button.collidepoint(mouse_pos):
                starting_money_input.manager.value = ""
                state = "select_starting_money"

    starting_money_input.update(filtered_keys)

    return state


def cs_sheet_events(screen, state: str, mouse_pos) -> str:
    """Check and handle events in function 'character_sheet_state_manager()' in 'state_manager.py' and return 'state'.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    # Button rects.
    save_load_button = sd.cs_sheet.save_load_button.button_rect
    main_menu_button = sd.cs_sheet.main_menu_button.button_rect
    exit_button = sd.cs_sheet.exit_button.button_rect
    cancel_button = sd.cs_sheet.cancel_button.button_rect
    save_button = sd.cs_sheet.save_button.button_rect

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        handle_screen_switch_reset(screen, event, mouse_pos)

        if state == "character_sheet":
            if event.type == pygame.MOUSEBUTTONUP:
                if save_load_button.collidepoint(mouse_pos):
                    uisd.load_only_flag = False
                    state = "init_save_load_screen"

                if main_menu_button.collidepoint(mouse_pos):
                    if sd.cs_sheet.is_saved:
                        state = "pre_main_menu"
                    else:
                        state = "sheet_confirmation"

        if state == "sheet_confirmation":
            if event.type == pygame.MOUSEBUTTONUP:
                if exit_button.collidepoint(mouse_pos):
                    state = "pre_main_menu"

                if cancel_button.collidepoint(mouse_pos):
                    state = "character_sheet"

                if save_button.collidepoint(mouse_pos):
                    uisd.load_only_flag = False
                    state = "init_save_load_screen"

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
        uisd.ui_registry["continue_button"].fade_alpha = 0
        uisd.ui_registry["skip_button"].fade_alpha = 0
        uisd.ui_registry["back_button"].fade_alpha = 0
