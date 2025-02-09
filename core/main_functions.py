import os
import core.character_model as char
import gui.gui as gui
import core.functions as func
import shop_functions as sf
import core.event_handlers as eh
from gui.cs_model import CharacterSheet
import random
"""Main functions/state managers used in 'main.py'."""


# Create instance of class 'Character'.
character = char.Character()
# Initialize variables for settings screen.
selected_window_size = None
# Initialize variables for character creation.
possible_characters = None
selected_race = None
selected_class = None
starting_money = None
random_money_flag = False
custom_money_flag = False


def main_state_manager(screen, state, gui_elements, mouse_pos):
    """State manager for main states, i.e. 'title_screen', 'main_menu', etc."""
    # Call main event handler and get program state.
    state = eh.main_events(screen, state, gui_elements, mouse_pos)

    if state == "title_screen":
        # Display title screen.
        gui.show_title_screen(screen, gui_elements)
    elif state == "main_menu":
        # Display main menu screen.
        gui.show_main_menu(screen, gui_elements, mouse_pos)
    elif state == "credits":
        # Display credits screen.
        gui.show_credits_screen(screen, gui_elements)
    elif state == "character_menu":
        # Display character menu screen
        gui.show_character_menu(screen, gui_elements, mouse_pos)

    return state


def settings_screen(screen, state, settings, gui_elements, mouse_pos):
    """State manager for settings screen state 'settings_screen'."""
    # Declare global variables to allow modification of these values within the function.
    global selected_window_size

    # Assign default object (small window) to 'selected_window_size'.
    if not selected_window_size:
        selected_window_size = gui_elements["window_size_buttons"][0]

    # Call event handler and get program state.
    state = eh.settings_screen_events(state, gui_elements, mouse_pos)

    # Display settings screen.
    selected_window_size = gui.show_settings(screen, settings, gui_elements, selected_window_size, mouse_pos)

    return state


def custom_character(screen, state, gui_elements, mouse_pos):
    """State manager for custom character creation based on user input."""
    # Declare global variables to allow modification of these values within the function.
    global possible_characters, selected_race, selected_class, starting_money, random_money_flag, custom_money_flag

    if state == "set_abilities":
        # Generate dictionary for character abilities.
        character.set_ability_dict()
        # Check if character abilities allow for any valid race-class combinations.
        race_list, class_list = func.get_race_class_lists(character)
        if func.check_valid_race_class(race_list, class_list):
            state = "show_abilities"
        else:
            state = "set_abilities"

    elif state == "show_abilities":
        # Display ability score screen.
        gui.show_ability_scores_screen(screen, character, gui_elements, mouse_pos)
        possible_characters, state = eh.custom_character_events(state, character, gui_elements, mouse_pos)

        # Unselect race and class selection, set variables to 'None' if user returns to ability score screen from
        # race/class selection screen.
        if selected_race:
            selected_race.selected = False
            selected_race = None
        if selected_class:
            selected_class.selected = False
            selected_class = None

    elif state == "race_class_selection":
        # Display race/class selection screen.
        selected_race, selected_class = gui.show_race_class_selection_screen(screen, possible_characters, selected_race,
                                                                            selected_class, gui_elements, mouse_pos)
        possible_characters, state = eh.custom_character_events(state, character, gui_elements, mouse_pos, possible_characters,
                                                                selected_race, selected_class)

    elif state == "name_character":
        # Display character naming screen.
        gui.show_naming_screen(screen, character, gui_elements, mouse_pos)
        state = eh.naming_character_events(state, character, gui_elements, mouse_pos)

        # Unselect money flags, set variables to 'False' if user returns to naming screen from starting money screen.
        if random_money_flag or custom_money_flag:
            random_money_flag, custom_money_flag = False, False

    elif state == "set_starting_money":
        # Display starting money screen.
        random_money_flag, custom_money_flag, starting_money = gui.show_starting_money_screen(screen, gui_elements,
                                                                                              random_money_flag, custom_money_flag,
                                                                                              starting_money, mouse_pos)
        possible_characters, state = eh.custom_character_events(state, character, gui_elements, mouse_pos, possible_characters,
                                                                random_money_flag, custom_money_flag, starting_money)

    elif state == "custom_input_money":
        # Special state for starting money screen to call 'custom_starting_money_events' for user input.
        random_money_flag, custom_money_flag, starting_money = gui.show_starting_money_screen(screen, gui_elements,
                                                                                              random_money_flag, custom_money_flag,
                                                                                              starting_money, mouse_pos)
        state = eh.custom_starting_money_events(state, character, gui_elements, mouse_pos)

    elif state == "creation_complete":
        # Display message screen stating that basic character creation is completed.
        gui.show_character_complete_screen(screen, gui_elements, mouse_pos)
        possible_characters, state = eh.custom_character_events(state, character, gui_elements, mouse_pos, possible_characters)


    return state


def random_character(screen, state, gui_elements, mouse_pos):
    """State manager for random character creation."""
    # Declare global variables to allow modification of these values within the function.
    global possible_characters, selected_race, selected_class

    if state == "random_character":
        # Get ability scores and valid race-class combinations.
        if not possible_characters:
            # Generate dictionary for character abilities.
            character.set_ability_dict()

            # Check if character abilities allow for any valid race-class combinations.
            race_list, class_list = func.get_race_class_lists(character)
            if func.check_valid_race_class(race_list, class_list):
                # Build list of possible characters, choose an entry at random, assign race/class to character object and
                # set corresponding attributes for character.
                possible_characters = func.build_possible_characters_list(race_list, class_list)
                selected_race, selected_class = random.choice(possible_characters).split()
                character.set_race(selected_race)
                character.set_class(selected_class)
                func.set_character_values(character)
                state = "set_random_money"

            else:
                state = "random_character"

    elif state == "set_random_money":
        # Set random amount of starting money in the background without UI.
        character.money = func.set_starting_money()
        state = "name_random_character"

    elif state == "name_random_character":
        # Display character naming screen.
        # 'creation_complete' state that follows afterward is handled in 'custom_character()' to avoid duplicate code.
        gui.show_naming_screen(screen, character, gui_elements, mouse_pos)
        state = eh.naming_character_events(state, character, gui_elements, mouse_pos)


    return state


def initialize_character_sheet(screen, gui_elements):
    """Create and return instance of class 'CharacterSheet' with screen elements for the character sheet, call position
    methods and set the state to 'character_sheet'.
    This function ensures that 'cs_sheet' is created only once and after the character creation process is complete,
    to avoid showing empty or uninitialized values on the screen."""

    # Create instance of class 'CharacterSheet'.
    cs_sheet = CharacterSheet(screen, character, gui_elements)
    # Set positions for character sheet elements on screen.
    cs_sheet.position_cs_elements()
    cs_sheet.specials_pos_y_list = cs_sheet.get_position_dynamic_field(cs_sheet.special_ability, character.specials,
                                                                      cs_sheet.special_abilities_title, text_prefix=" - ")
    cs_sheet.class_special_pos_y_list = cs_sheet.get_position_dynamic_field(cs_sheet.class_special, character.class_specials,
                                                                      cs_sheet.class_specials_title)

    state = "character_sheet"

    return cs_sheet, state


"""
OLD MAIN SHOP FUNCTION FOR CONSOLE PART OF THE PROGRAM. DELETE WHEN MIGRATED TO PYGAME.
"""

def show_main_shop():
    """Main loop for shop 'main menu'."""
    shop_sections = ["General Items", "Weapons", "Projectiles", "Armor", "Inventory", "EXIT"]

    while True:
        print(" - SHOP -\n")
        shop_section = func.select_from_list(shop_sections, "\nWhat items do you want to buy? ")
        os.system('cls')

        if shop_section == "General Items":
            sf.set_shop(character, shop_section)
        elif shop_section == "Weapons":
            sf.set_shop(character, shop_section)
        elif shop_section == "Projectiles":
            sf.set_shop(character, shop_section)
        elif shop_section == "Armor":
            sf.set_shop(character, shop_section)
        elif shop_section == "Inventory":
            sf.set_shop(character, shop_section)
        else:
            break


"""
Following function is imported into and called in event handler 'naming_character_events()' when returning to character
menu from 'name_random_character' state. This resolves an issue that caused the program to freeze when returning from
naming screen to character menu.
"""

def fix_my_messy_globals():
    """Reset variables with default values."""
    global possible_characters, selected_race, selected_class
    possible_characters = None
    selected_race = None
    selected_class = None
