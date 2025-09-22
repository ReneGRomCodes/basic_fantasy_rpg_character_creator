"""
Main functions/state managers used in 'main.py'.
"""
import random

import gui.gui as gui
from gui.credits import Credits
from gui.shared_data import ui_shared_data as uisd
from gui.settings_gui import SettingsGUI
from gui.cs_model import CharacterSheet
from gui.sl_model import SaveLoadScreen

import core.rules as rls
import core.event_handlers as eh
from .shared_data import shared_data as sd
from .character_model import Character


def main_state_manager(screen, state: str, mouse_pos) -> str:
    """State manager for main states, i.e. 'title_screen', 'main_menu', etc.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    state = eh.main_events(screen, state, mouse_pos)

    if state == "title_screen":
        gui.show_title_screen(screen)

    elif state == "pre_main_menu":
        sd.character = Character()
        sd.shared_data_janitor()
        state = "main_menu"

    elif state == "main_menu":
        gui.show_main_menu(screen, mouse_pos)

    elif state == "settings_screen":
        state = settings_screen_state_manager(screen, state, mouse_pos)

    elif state in {"init_credits", "credits"}:
        state = credits_state_manager(screen, state)

    elif state == "character_menu":
        gui.show_character_menu(screen, mouse_pos)

    return state

def save_load_screen_state_manager(screen, state: str, mouse_pos) -> str:
    """State manager for 'save/load screen'.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    if state == "init_save_load_screen":
        sd.save_load_screen = SaveLoadScreen(screen)
        sd.save_load_screen.position_sl_elements()
        state = "save_load_screen"

    elif state == "save_load_screen":
        sd.save_load_screen.show_sl_screen(mouse_pos)
        state = eh.save_load_events(screen, state, mouse_pos)

    elif state in {"char_not_saved", "char_delete", "char_overwrite"}:
        sd.save_load_screen.format_confirm_message(state)
        sd.save_load_screen.show_confirm_message(mouse_pos)
        state = eh.save_load_events(screen, state, mouse_pos)

    return state


def settings_screen_state_manager(screen, state: str, mouse_pos) -> str:
    """State manager for settings screen state 'settings_screen'.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    if not sd.settings_gui:
        sd.settings_gui = SettingsGUI(screen)

    state = eh.main_events(screen, state, mouse_pos)
    sd.settings_gui.show_settings(screen, mouse_pos)

    return state


def credits_state_manager(screen, state: str) -> str:
    """'Secondary' state manager for use in 'main_state_manager' to handle credits screen object.
    ARGS:
        screen: PyGame window.
        state: program state.
    RETURNS:
        state
    """
    if state == "init_credits":
        sd.credits_screen = Credits(screen)
        state = "credits"

    elif state == "credits":
        sd.credits_screen.show_credits(screen)

    return state


def custom_character_state_manager(screen, state: str, mouse_pos) -> str:
    """State manager for custom character creation based on user input.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    if state == "set_abilities":
        sd.character.set_ability_dict()
        if rls.check_valid_race_class(sd.character):
            state = "show_abilities"
        else:
            state = "set_abilities"

    elif state == "show_abilities":
        sd.shared_data_janitor()
        gui.show_ability_scores_screen(screen, mouse_pos)
        state = eh.custom_character_events(screen, state, mouse_pos)

    elif state == "race_class_selection":
        gui.show_race_class_selection_screen(screen, mouse_pos)
        state = eh.custom_character_events(screen, state,  mouse_pos)

    elif state == "spell_selection":
        sd.set_default_spell(uisd.ui_registry["spell_fields"])
        gui.show_spell_selection_screen(screen, mouse_pos)
        state = eh.custom_character_events(screen, state, mouse_pos)

    elif state == "language_selection":
        sd.set_default_languages(uisd.ui_registry["lang_fields"])

        if not uisd.language_flag:
            sd.character.set_languages(uisd.ui_registry["lang_fields"])
            return "name_character"
        else:
            gui.show_language_selection_screen(screen, mouse_pos)

        state = eh.custom_character_events(screen, state, mouse_pos)

    elif state == "name_character":
        if uisd.language_flag:
            sd.clear_language_selection()

        gui.show_naming_screen(screen, mouse_pos)
        state = eh.naming_character_events(screen, state, mouse_pos)

        if sd.random_money_flag or sd.custom_money_flag or uisd.dice_roll_complete:
            sd.random_money_flag, sd.custom_money_flag, uisd.dice_roll_complete = False, False, False

    elif state == "select_starting_money":
        gui.show_starting_money_screen(screen, mouse_pos)
        state = eh.custom_character_events(screen, state, mouse_pos)

    elif state == "custom_input_money":
        gui.show_starting_money_screen(screen, mouse_pos)
        state = eh.custom_starting_money_events(screen, state, mouse_pos)

    elif state == "confirm_character":
        gui.show_created_character_confirmation_screen(screen, mouse_pos)
        state = eh.custom_character_events(screen,state, mouse_pos)

    elif state == "creation_complete":
        gui.show_character_complete_screen(screen, mouse_pos)
        state = eh.custom_character_events(screen, state, mouse_pos)

    return state


def random_character_state_manager(screen, state: str, mouse_pos) -> str:
    """State manager for random character creation.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    if state == "random_character":
        if not sd.possible_characters:
            sd.character.set_ability_dict()

            if rls.check_valid_race_class(sd.character):
                sd.possible_characters = rls.build_possible_characters_list(sd.character)
                sd.selected_race, sd.selected_class = random.choice(sd.possible_characters).split()
                sd.character.set_race(sd.selected_race)
                sd.character.set_class(sd.selected_class)
                sd.character.set_character_values()
                sd.character.set_random_selections(uisd.ui_registry["spell_fields"], rls.set_language_flag(sd.character),
                                                   uisd.ui_registry["lang_fields"])
                state = "set_random_money"

            else:
                state = "random_character"

    elif state == "set_random_money":
        sd.character.money = rls.roll_starting_money()
        state = "name_random_character"

    elif state == "name_random_character":
        # 'creation_complete' state that follows afterward is handled in 'custom_character()' to avoid duplicate code.
        gui.show_naming_screen(screen, mouse_pos)
        state = eh.naming_character_events(screen, state, mouse_pos)

    return state


def character_sheet_state_manager(screen, state: str, mouse_pos) -> str:
    """State manager character sheet screen.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    if state == "init_character_sheet":
        sd.cs_sheet = CharacterSheet(screen)
        sd.cs_sheet.position_cs_elements()

        if uisd.is_loaded:
            sd.cs_sheet.is_saved = uisd.is_loaded
            uisd.is_loaded = False

        state = "character_sheet"

    elif state == "character_sheet":
        sd.cs_sheet.show_character_sheet_screen(mouse_pos)
        state = eh.cs_sheet_events(screen, state, mouse_pos)

    elif state == "sheet_confirmation":
        sd.cs_sheet.show_exit_confirm_message(screen, mouse_pos)
        state = eh.cs_sheet_events(screen, state, mouse_pos)

    return state
