import os
from core.character_model import Character
from gui.credits import Credits
import gui.gui as gui
import core.rules as rls
import shop_functions as sf
import core.event_handlers as eh
from core.shared_data import shared_data as sd
from gui.settings_gui import SettingsGUI
from gui.cs_model import CharacterSheet
import random
"""Main functions/state managers used in 'main.py'."""


def main_state_manager(screen, state: str, gui_elements: dict, mouse_pos) -> str:
    """State manager for main states, i.e. 'title_screen', 'main_menu', etc.
    ARGS:
        screen: PyGame window.
        state: program state.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    # Call main event handler and get program state.
    state = eh.main_events(screen, state, gui_elements, mouse_pos)

    if state == "title_screen":
        # Display title screen.
        gui.show_title_screen(screen, gui_elements)

    elif state == "pre_main_menu":
        # Create/re-initialize instance of class 'Character' and reset shared data to start with a clean sheet when
        # accessing main menu or returning to it from a different screen.
        sd.character = Character()
        sd.shared_data_janitor(gui_elements)

        state = "main_menu"

    elif state == "main_menu":
        # Display main menu screen.
        gui.show_main_menu(screen, gui_elements, mouse_pos)

    elif state in {"init_credits", "credits"}:
        # Use of 'secondary' state manager for credits screen.
        state = credits_state_manager(screen, state, gui_elements)

    elif state == "character_menu":
        # Display character menu screen
        gui.show_character_menu(screen, gui_elements, mouse_pos)

    elif state in {"init_character_sheet", "character_sheet"}:
        # Use of 'secondary' state manager for character sheet screen.
        state = character_sheet_state_manager(screen, state, gui_elements, mouse_pos)

    return state


def credits_state_manager(screen, state: str, gui_elements: dict) -> str:
    """'Secondary' state manager for use in 'main_state_manager' to handle credits screen object.
    ARGS:
        screen: PyGame window.
        state: program state.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
    RETURNS:
        state
    """
    if state == "init_credits":
        # Initialize 'Credits()' object every time before credits screen is displayed to reset starting positions of text
        # elements and to account for changes to 'gui_elements' if window size has been changed in settings screen.
        sd.credits_screen = Credits(screen, gui_elements)
        state = "credits"
    # Display credits screen.
    elif state == "credits":
        sd.credits_screen.show_credits(screen, gui_elements)

    return state


def settings_screen(screen, state: str, gui_elements: dict, mouse_pos) -> tuple[dict, str]:
    """State manager for settings screen state 'settings_screen'.
    ARGS:
        screen: PyGame window.
        state: program state.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        gui_elements, state
    """
    # Initialize 'SettingsGUI() object the first time the settings screen is accessed.
    if not sd.settings_gui:
        sd.settings_gui = SettingsGUI(screen, gui_elements)

    # Call event handler and get program state.
    state = eh.main_events(screen, state, gui_elements, mouse_pos)

    # Display settings screen.
    gui_elements = sd.settings_gui.show_settings(screen, gui_elements, mouse_pos)

    return gui_elements, state


def custom_character(screen, state: str, gui_elements: dict, mouse_pos) -> str:
    """State manager for custom character creation based on user input.
    ARGS:
        screen: PyGame window.
        state: program state.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
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
        sd.shared_data_janitor(gui_elements)
        # Display ability score screen.
        gui.show_ability_scores_screen(screen, sd.character, gui_elements, mouse_pos)
        sd.possible_characters, state = eh.custom_character_events(screen, state, sd.character, gui_elements, mouse_pos)

    elif state == "race_class_selection":
        # Display race/class selection screen.
        sd.selected_race, sd.selected_class =(
            gui.show_race_class_selection_screen(screen, sd.rc_dict, sd.possible_characters, sd.selected_race,
                                                 sd.selected_class, gui_elements, mouse_pos))

        sd.possible_characters, state =(
            eh.custom_character_events(screen, state, sd.character, gui_elements, mouse_pos, sd.possible_characters,
                                       sd.selected_race, sd.selected_class))

    elif state == "spell_selection":
        # Display spell selection screen for Magic-Users.
        gui.show_spell_selection_screen(screen, sd.character, gui_elements, mouse_pos)
        sd.possible_characters, state =(
            eh.custom_character_events(screen, state, sd.character, gui_elements, mouse_pos, sd.possible_characters))

    elif state == "name_character":
        # Display character naming screen.
        gui.show_naming_screen(screen, sd.character, gui_elements, mouse_pos)
        state = eh.naming_character_events(screen, state, sd.character, gui_elements, mouse_pos)

        # Unselect money flags, set variables to 'False' if user returns to naming screen from starting money screen.
        if sd.random_money_flag or sd.custom_money_flag:
            sd.random_money_flag, sd.custom_money_flag = False, False

    elif state == "select_starting_money":
        # Base state for starting money screen.
        sd.random_money_flag, sd.custom_money_flag, sd.starting_money =(
            gui.show_starting_money_screen(screen, gui_elements, sd.random_money_flag, sd.custom_money_flag,
                                           sd.starting_money, mouse_pos))

        sd.possible_characters, state =(
            eh.custom_character_events(screen, state, sd.character, gui_elements, mouse_pos, sd.possible_characters,
                                       sd.random_money_flag, sd.custom_money_flag, sd.starting_money))

    elif state == "custom_input_money":
        # Special state for starting money screen to call 'custom_starting_money_events' for user input.
        sd.random_money_flag, sd.custom_money_flag, sd.starting_money =(
            gui.show_starting_money_screen(screen, gui_elements, sd.random_money_flag, sd.custom_money_flag,
                                           sd.starting_money, mouse_pos))

        state = eh.custom_starting_money_events(screen, state, sd.character, gui_elements, mouse_pos)

    elif state == "creation_complete":
        # Display message screen stating that basic character creation is completed.
        gui.show_character_complete_screen(screen, gui_elements, mouse_pos)

        sd.possible_characters, state =(
            eh.custom_character_events(screen, state, sd.character, gui_elements, mouse_pos, sd.possible_characters))

    return state


def random_character(screen, state: str, gui_elements: dict, mouse_pos) -> str:
    """State manager for random character creation.
    ARGS:
        screen: PyGame window.
        state: program state.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
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
        gui.show_naming_screen(screen, sd.character, gui_elements, mouse_pos)
        state = eh.naming_character_events(screen, state, sd.character, gui_elements, mouse_pos)

    return state


def character_sheet_state_manager(screen, state: str, gui_elements: dict, mouse_pos) -> str:
    """'Secondary' state manager for use in 'main_state_manager' to create and return instance of class 'CharacterSheet'
    with screen elements for the character sheet, call position methods and set the state to 'character_sheet'.
    This function ensures that 'cs_sheet' is always created before the character sheet screen is displayed, reinitializing
    it each time the screen is accessed. This prevents issues such as uninitialized values or incorrect text scaling after
    a window size change.
    ARGS:
        screen: PyGame window.
        state: program state.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        state
    """
    if state == "init_character_sheet":
        # Create instance of class 'CharacterSheet'.
        sd.cs_sheet = CharacterSheet(screen, sd.character, gui_elements)
        # Set positions for character sheet elements on screen.
        sd.cs_sheet.position_cs_elements()

        state = "character_sheet"

    elif state == "character_sheet":
        sd.cs_sheet.show_character_sheet_screen(mouse_pos)

    return state


"""
OLD MAIN SHOP FUNCTION FOR CONSOLE PART OF THE PROGRAM. DELETE WHEN MIGRATED TO PYGAME.
"""

def show_main_shop():
    """Main loop for shop 'main menu'."""
    shop_sections = ["General Items", "Weapons", "Projectiles", "Armor", "Inventory", "EXIT"]

    while True:
        print(" - SHOP -\n")
        shop_section = rls.select_from_list(shop_sections, "\nWhat items do you want to buy? ")
        os.system('cls')

        if shop_section == "General Items":
            sf.set_shop(sd.character, shop_section)
        elif shop_section == "Weapons":
            sf.set_shop(sd.character, shop_section)
        elif shop_section == "Projectiles":
            sf.set_shop(sd.character, shop_section)
        elif shop_section == "Armor":
            sf.set_shop(sd.character, shop_section)
        elif shop_section == "Inventory":
            sf.set_shop(sd.character, shop_section)
        else:
            break
