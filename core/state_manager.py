from core.character_model import Character
from gui.credits import Credits
import gui.gui as gui
import core.rules as rls
import core.event_handlers as eh
from core.shared_data import shared_data as sd
from gui.shared_data import ui_shared_data as uisd
from gui.settings_gui import SettingsGUI
from gui.cs_model import CharacterSheet
from gui.sl_model import SaveLoadScreen
import random
"""Main functions/state managers used in 'main.py'."""


def main_state_manager(screen, state: str, mouse_pos) -> str:
    """State manager for main states, i.e. 'title_screen', 'main_menu', etc.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    # Call main event handler and get program state.
    state = eh.main_events(screen, state, mouse_pos)

    if state == "title_screen":
        # Display title screen.
        gui.show_title_screen(screen)

    elif state == "pre_main_menu":
        # Create/re-initialize instance of class 'Character' and reset shared data to start with a clean sheet when
        # accessing main menu or returning to it from a different screen.
        sd.character = Character()
        sd.shared_data_janitor()

        state = "main_menu"

    elif state == "main_menu":
        # Display main menu screen.
        gui.show_main_menu(screen, mouse_pos)

    elif state in {"init_save_load_screen", "save_load_screen"}:
        state = save_load_screen_state_manager(screen, state, mouse_pos)

    elif state in {"init_credits", "credits"}:
        # Use of 'secondary' state manager for credits screen.
        state = credits_state_manager(screen, state)

    elif state == "character_menu":
        # Display character menu screen
        gui.show_character_menu(screen, mouse_pos)

    elif state in {"init_character_sheet", "character_sheet"}:
        # Use of 'secondary' state manager for character sheet screen.
        state = character_sheet_state_manager(screen, state, mouse_pos)

    return state


def save_load_screen_state_manager(screen, state: str, mouse_pos) -> str:
    if state == "init_save_load_screen":
        sd.save_load_screen = SaveLoadScreen(screen)
        sd.save_load_screen.position_sl_elements()
        state = "save_load_screen"

    elif state == "save_load_screen":
        sd.save_load_screen.show_sl_screen(screen, mouse_pos)
        state = eh.main_events(screen, state, mouse_pos)

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
    # Initialize 'SettingsGUI() object the first time the settings screen is accessed.
    if not sd.settings_gui:
        sd.settings_gui = SettingsGUI(screen)

    # Call event handler and get program state.
    state = eh.main_events(screen, state, mouse_pos)

    # Display settings screen.
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
        # Initialize 'Credits()' object every time before credits screen is displayed to reset starting positions of text
        # elements and to account for changes to 'gui_elements' if window size has been changed in settings screen.
        sd.credits_screen = Credits(screen)
        state = "credits"
    # Display credits screen.
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
        # Generate dictionary for character abilities.
        sd.character.set_ability_dict()
        # Check if character abilities allow for any valid race-class combinations and only continue to next state if so.
        if rls.check_valid_race_class(sd.character):
            state = "show_abilities"
        else:
            state = "set_abilities"

    elif state == "show_abilities":
        # Reset any shared data in case user returns to ability score screen from race/class selection screen.
        sd.shared_data_janitor()
        # Display ability score screen.
        gui.show_ability_scores_screen(screen, mouse_pos)
        state = eh.custom_character_events(screen, state, mouse_pos)

    elif state == "race_class_selection":
        # Display race/class selection screen.
        gui.show_race_class_selection_screen(screen, mouse_pos)
        state = eh.custom_character_events(screen, state,  mouse_pos)

    elif state == "spell_selection":
        # Display spell selection screen for Magic-Users.
        sd.set_default_spell(uisd.gui_elements["spell_fields"])
        gui.show_spell_selection_screen(screen, mouse_pos)
        state = eh.custom_character_events(screen, state, mouse_pos)

    elif state == "language_selection":
        # Set default languages for character's race.
        sd.set_default_languages(uisd.gui_elements["lang_fields"])
        # Display language selection screen if conditions are met.
        if uisd.language_flag:
            gui.show_language_selection_screen(screen, mouse_pos)
        state = eh.custom_character_events(screen, state, mouse_pos)

    elif state == "name_character":
        # Display character naming screen.
        gui.show_naming_screen(screen, mouse_pos)
        state = eh.naming_character_events(screen, state, mouse_pos)

        # Unselect 'shared_data' money flags, set variables to 'False' if user returns to naming screen from starting
        # money screen. Also ensures that flags are 'False' before switching to starting money screen.
        if sd.random_money_flag or sd.custom_money_flag or uisd.dice_roll_complete:
            sd.random_money_flag, sd.custom_money_flag, uisd.dice_roll_complete = False, False, False

    elif state == "select_starting_money":
        # Base state for starting money screen.
        gui.show_starting_money_screen(screen, mouse_pos)
        state = eh.custom_character_events(screen, state, mouse_pos)

    elif state == "custom_input_money":
        # Special state for starting money screen to call 'custom_starting_money_events' for user input.
        gui.show_starting_money_screen(screen, mouse_pos)
        state = eh.custom_starting_money_events(screen, state, mouse_pos)

    elif state == "creation_complete":
        # Display message screen stating that basic character creation is completed.
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
        # Get ability scores and valid race-class combinations.
        if not sd.possible_characters:
            # Generate dictionary for character abilities.
            sd.character.set_ability_dict()

            # Check if character abilities allow for any valid race-class combinations.
            if rls.check_valid_race_class(sd.character):
                # Build list of possible characters, choose an entry at random, assign race/class to character object and
                # set corresponding attributes for character.
                sd.possible_characters = rls.build_possible_characters_list(sd.character)
                sd.selected_race, sd.selected_class = random.choice(sd.possible_characters).split()
                sd.character.set_race(sd.selected_race)
                sd.character.set_class(sd.selected_class)
                sd.character.set_character_values()
                # Select and set various additional character attributes like spells and languages.
                sd.character.set_random_selections(uisd.gui_elements["spell_fields"], rls.set_language_flag(sd.character),
                                                   uisd.gui_elements["lang_fields"])

                state = "set_random_money"

            else:
                state = "random_character"

    elif state == "set_random_money":
        # Set random amount of starting money in the background without UI.
        sd.character.money = rls.roll_starting_money()
        state = "name_random_character"

    elif state == "name_random_character":
        # Display character naming screen.
        # 'creation_complete' state that follows afterward is handled in 'custom_character()' to avoid duplicate code.
        gui.show_naming_screen(screen, mouse_pos)
        state = eh.naming_character_events(screen, state, mouse_pos)

    return state


def character_sheet_state_manager(screen, state: str, mouse_pos) -> str:
    """'Secondary' state manager for use in 'main_state_manager' to create and return instance of class 'CharacterSheet'
    with screen elements for the character sheet, call position methods and set the state to 'character_sheet'.
    This function ensures that 'cs_sheet' is always created before the character sheet screen is displayed, reinitializing
    it each time the screen is accessed. This prevents issues such as uninitialized values or incorrect text scaling after
    a window size change.
    ARGS:
        screen: PyGame window.
        state: program state.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    if state == "init_character_sheet":
        # Create instance of class 'CharacterSheet'.
        sd.cs_sheet = CharacterSheet(screen)
        # Set positions for character sheet elements on screen.
        sd.cs_sheet.position_cs_elements()

        state = "character_sheet"

    elif state == "character_sheet":
        sd.cs_sheet.show_character_sheet_screen(mouse_pos)

    return state
