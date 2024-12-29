import os
import core.character_model as char
import character_creation_functions as cf
import gui.gui as gui
import core.functions as func
import shop_functions as sf
import core.event_handlers as eh
"""Main functions used in 'main.py'."""


# Create instance of class 'Character' .
character = char.Character()
# Initialize variables and set starting values for character creation.
possible_characters = None
selected_race = None
selected_class = None
starting_money = None
random_money_flag = False
custom_money_flag = False


def custom_character(screen, state, gui_elements, mouse_pos):
    """Create custom character based on user input. Check and return state for main loop."""
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
        gui.show_naming_screen(screen, gui_elements, mouse_pos)
        state = eh.naming_character_events(state, character, gui_elements, mouse_pos)

        # Unselect money flags, set variables to 'False' if user returns to naming screen from starting money screen.
        if random_money_flag or custom_money_flag:
            random_money_flag, custom_money_flag = False, False

    elif state == "set_starting_money":
        # Display starting money screen.
        random_money_flag, custom_money_flag, starting_money = gui.show_starting_money_screen(screen, gui_elements, character,
                                                                                              random_money_flag, custom_money_flag,
                                                                                              starting_money, mouse_pos)
        possible_characters, state = eh.custom_character_events(state, character, gui_elements, mouse_pos, possible_characters,
                                                                random_money_flag, custom_money_flag)

    elif state == "custom_money":
        # Special state for starting money screen to call 'custom_starting_money_events' for user input.
        random_money_flag, custom_money_flag, starting_money = gui.show_starting_money_screen(screen, gui_elements, character,
                                                                                              random_money_flag, custom_money_flag,
                                                                                              starting_money, mouse_pos)
        starting_money, state = eh.custom_starting_money_events(state, gui_elements, starting_money, mouse_pos)

    # State for code that has yet to be migrated to Pygame.
    elif state == "TODO":
        os.system('cls')

        print("\n\n\t\tCharacter creation complete. Press ENTER to show character sheet.")
        input()
        os.system('cls')

        # Build character sheet.
        cf.build_character_sheet(character)

        # Proceed to shop and show final character sheet when finished.
        input("\n\nPress ENTER to proceed to shop.")
        os.system('cls')
        show_main_shop()
        cf.build_character_sheet(character)
        input("\n\nPress ENTER to exit.")

    return state


def random_character():
    """Create character with random values and print character sheet."""
    os.system('cls')
    # Get random class, race, name and ability scores.
    cf.random_character_generator(character)

    print("\n\n\t\tCharacter creation complete. Press ENTER to show character sheet.")
    input()
    os.system('cls')

    # Build character sheet.
    cf.build_character_sheet(character)

    # Proceed to shop and show final character sheet when finished.
    input("\n\nPress ENTER to proceed to shop.")
    os.system('cls')
    show_main_shop()
    cf.build_character_sheet(character)
    input("\n\nPress ENTER to exit.")


def show_main_shop():
    """Main loop for shop 'main menu'."""
    global character
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
