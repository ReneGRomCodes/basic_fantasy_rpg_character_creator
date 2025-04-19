import os
from core.character_model import Character
from gui.credits import Credits
import gui.gui as gui
import core.rules as rls
import shop_functions as sf
import core.event_handlers as eh
from gui.cs_model import CharacterSheet
from gui.screen_objects import InteractiveText
import random
"""Main functions/state managers used in 'main.py'."""


# Variable for later instance of character object.
character: Character
# Variable for later instance of credits screen object.
credits_screen: Credits
# Variable for later instance of character sheet screen object.
cs_sheet: CharacterSheet
# Further variables for character creation.
rc_dict: dict[str, str]  # Dict with all available races/classes in the game.
possible_characters: list[str]  # List of possible race-class combinations.
selected_race: object | str = None # 'TextField' instance representing selected race in custom creation, string in random creation.
selected_class: object | str = None  # 'TextField' instance representing selected class in custom creation, string in random creation.
starting_money: int = 0  # Characters starting money.
random_money_flag: bool = False  # Flag to check money selection.
custom_money_flag: bool = False  # Flag to check money selection.


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
    # Declare global variable 'rc_dict' to allow modification of its contents within the function.
    global character

    # Call main event handler and get program state.
    state = eh.main_events(screen, state, gui_elements, mouse_pos)

    if state == "title_screen":
        # Display title screen.
        gui.show_title_screen(screen, gui_elements)

    elif state == "pre_main_menu":
        # Create/re-initialize instance of class 'Character' and reset globals to start with a clean sheet when accessing
        # main menu or returning to it from a different screen.
        character = Character()
        globals_janitor(gui_elements)

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
        state = character_sheet_state_manager(screen, state, gui_elements)

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
    # Declare global variable to assign instance of class 'Credits' and allow for easier resetting of instance when
    # appropriate.
    global credits_screen

    if state == "init_credits":
        # Initialize 'Credits()' object every time before credits screen is displayed to reset starting positions of text
        # elements and to account for changes to 'gui_elements' if window size has been changed in settings screen.
        credits_screen = Credits(screen, gui_elements)
        state = "credits"
    # Display credits screen.
    elif state == "credits":
        credits_screen.show_credits(screen, gui_elements)

    return state


def settings_screen(screen, state: str, settings, settings_gui, gui_elements: dict, mouse_pos) -> tuple[dict, str]:
    """State manager for settings screen state 'settings_screen'.
    ARGS:
        screen: PyGame window.
        state: program state.
        settings: instance of class 'Settings()'.
        settings_gui: instance of class 'SettingsGUI()'.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        gui_elements, state
    """

    # Call event handler and get program state.
    state = eh.main_events(screen, state, gui_elements, mouse_pos)

    # Display settings screen.
    gui_elements = settings_gui.show_settings(screen, settings, gui_elements, mouse_pos)

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
    # Declare global variables to allow modification of these values within the function.
    global possible_characters, rc_dict, selected_race, selected_class, starting_money, random_money_flag, custom_money_flag

    if state == "set_abilities":
        # Generate dictionary for character abilities.
        character.set_ability_dict()
        # Check if character abilities allow for any valid race-class combinations and only continue to next state if so.
        if rls.check_valid_race_class(character):
            state = "show_abilities"
        else:
            state = "set_abilities"

    elif state == "show_abilities":
        # Reset any globals in case user returns to ability score screen from race/class selection screen.
        globals_janitor(gui_elements)
        # Display ability score screen.
        gui.show_ability_scores_screen(screen, character, gui_elements, mouse_pos)
        possible_characters, state = eh.custom_character_events(screen, state, character, gui_elements, mouse_pos)

    elif state == "race_class_selection":
        # Display race/class selection screen.
        selected_race, selected_class = gui.show_race_class_selection_screen(screen, rc_dict, possible_characters,
                                                                             selected_race, selected_class, gui_elements,
                                                                             mouse_pos)
        possible_characters, state = eh.custom_character_events(screen, state, character, gui_elements, mouse_pos, possible_characters,
                                                                selected_race, selected_class)

    elif state == "name_character":
        # Display character naming screen.
        gui.show_naming_screen(screen, character, gui_elements, mouse_pos)
        state = eh.naming_character_events(screen, state, character, gui_elements, mouse_pos)

        # Unselect money flags, set variables to 'False' if user returns to naming screen from starting money screen.
        if random_money_flag or custom_money_flag:
            random_money_flag, custom_money_flag = False, False

    elif state == "set_starting_money":
        # Display starting money screen.
        random_money_flag, custom_money_flag, starting_money = gui.show_starting_money_screen(screen, gui_elements,
                                                                                              random_money_flag, custom_money_flag,
                                                                                              starting_money, mouse_pos)
        possible_characters, state = eh.custom_character_events(screen, state, character, gui_elements, mouse_pos, possible_characters,
                                                                random_money_flag, custom_money_flag, starting_money)

    elif state == "custom_input_money":
        # Special state for starting money screen to call 'custom_starting_money_events' for user input.
        random_money_flag, custom_money_flag, starting_money = gui.show_starting_money_screen(screen, gui_elements,
                                                                                              random_money_flag, custom_money_flag,
                                                                                              starting_money, mouse_pos)
        state = eh.custom_starting_money_events(screen, state, character, gui_elements, mouse_pos)

    elif state == "creation_complete":
        # Display message screen stating that basic character creation is completed.
        gui.show_character_complete_screen(screen, gui_elements, mouse_pos)
        possible_characters, state = eh.custom_character_events(screen, state, character, gui_elements, mouse_pos, possible_characters)

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
    # Declare global variables to allow modification of these values within the function.
    global possible_characters, selected_race, selected_class

    if state == "random_character":
        # Get ability scores and valid race-class combinations.
        if not possible_characters:
            # Generate dictionary for character abilities.
            character.set_ability_dict()

            # Check if character abilities allow for any valid race-class combinations.
            if rls.check_valid_race_class(character):
                # Build list of possible characters, choose an entry at random, assign race/class to character object and
                # set corresponding attributes for character.
                possible_characters = rls.build_possible_characters_list(character)
                selected_race, selected_class = random.choice(possible_characters).split()
                character.set_race(selected_race)
                character.set_class(selected_class)
                rls.set_character_values(character)
                state = "set_random_money"

            else:
                state = "random_character"

    elif state == "set_random_money":
        # Set random amount of starting money in the background without UI.
        character.money = rls.set_starting_money()
        state = "name_random_character"

    elif state == "name_random_character":
        # Display character naming screen.
        # 'creation_complete' state that follows afterward is handled in 'custom_character()' to avoid duplicate code.
        gui.show_naming_screen(screen, character, gui_elements, mouse_pos)
        state = eh.naming_character_events(screen, state, character, gui_elements, mouse_pos)

    return state


def character_sheet_state_manager(screen, state: str, gui_elements: dict) -> str:
    """'Secondary' state manager for use in 'main_state_manager' to create and return instance of class 'CharacterSheet'
    with screen elements for the character sheet, call position methods and set the state to 'character_sheet'.
    This function ensures that 'cs_sheet' is always created before the character sheet screen is displayed, reinitializing
    it each time the screen is accessed. This prevents issues such as uninitialized values or incorrect text scaling after
    a window size change.
    ARGS:
        screen: PyGame window.
        state: program state.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
    RETURNS:
        state
    """
    # Declare global variable to assign instance of class 'CharacterSheet'.
    global cs_sheet

    if state == "init_character_sheet":
        # Create instance of class 'CharacterSheet'.
        cs_sheet = CharacterSheet(screen, character, gui_elements)
        # Set positions for character sheet elements on screen.
        cs_sheet.position_cs_elements()
        cs_sheet.specials_pos_y_list = cs_sheet.get_position_dynamic_field(cs_sheet.special_ability, character.specials,
                                                                          cs_sheet.special_abilities_title, text_prefix=" - ")
        cs_sheet.class_special_pos_y_list = cs_sheet.get_position_dynamic_field(cs_sheet.class_special, character.class_specials,
                                                                          cs_sheet.class_specials_title)

        state = "character_sheet"

    elif state == "character_sheet":
        cs_sheet.show_character_sheet_screen()

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
menu from 'name_random_character' state, in addition to it's function calls in states 'pre_main_menu' and 'show_abilities'.
This resolves multiple issue that caused the program to freeze when switching between different screens or when creating
a new character after one has already been created.
"""

def globals_janitor(gui_elements: dict) -> None:
    """Reset global variables that are not automatically overwritten elsewhere with default values in case of a switch
    to a previous screen or the main menu.
    ARGS:
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
    """
    global rc_dict, possible_characters, selected_race, selected_class

    # Unselect race and class selection if user visited race/class selection screen previously. 'isinstance' check is
    # necessary as variables can hold either a screen object or a string during custom and random character creation
    # respectively.
    if isinstance(selected_race, InteractiveText):
        selected_race.selected = False
    if isinstance(selected_class, InteractiveText):
        selected_class.selected = False

    # Reset globals to 'None'.
    possible_characters = None
    selected_race = None
    selected_class = None

    # Initialize/reset dict for use in 'gui/ui_helpers.py' in function 'position_race_class_elements()' to calculate UI
    # positioning, and automatically populate dict 'rc_dict' once with all races/classes available in the game for later
    # use in race/class selection.
    rc_dict = {
        "races": [race.text for race in gui_elements["active_races"]],
        "classes": [cls.text for cls in gui_elements["active_classes"]],
    }
