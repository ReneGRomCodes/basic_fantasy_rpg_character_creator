import os
import character_creation_functions as cf
import functions as func
import shop_functions as sf
import event_handlers as eh
"""Main functions used in 'main.py'."""


def custom_character(screen, state, character, possible_characters, selected_race, selected_class, character_name_input,
                     gui_elements, mouse_pos):
    """Create custom character based on user input and return state for main loop."""
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
        cf.show_ability_scores_screen(screen, character, gui_elements, mouse_pos)
        possible_characters, state = eh.custom_character_events(state, character, possible_characters, gui_elements, mouse_pos)

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
        selected_race, selected_class = cf.show_race_class_selection_screen(screen, possible_characters, selected_race,
                                                                            selected_class, gui_elements, mouse_pos)
        possible_characters, state = eh.custom_character_events(state, character, possible_characters, gui_elements, mouse_pos,
                                                                selected_race, selected_class)

    elif state == "name_character":
        # Display character naming screen.
        cf.show_naming_screen(screen, gui_elements, mouse_pos)
        state = eh.naming_character_events(state, character, character_name_input, gui_elements, mouse_pos)

    elif state == "set_starting_money":
        # Display starting money screen.
        cf.show_starting_money_screen(screen, gui_elements, mouse_pos)
        possible_characters, state = eh.custom_character_events(state, character, possible_characters, gui_elements, mouse_pos,
                                                                selected_race, selected_class)

    # State for code that has yet to be migrated to Pygame.
    elif state == "TODO":
        # Set amount of starting money.
        cf.set_starting_money(character)
        os.system('cls')

        print("\n\n\t\tCharacter creation complete. Press ENTER to show character sheet.")
        input()
        os.system('cls')

        # Build character sheet.
        cf.build_character_sheet(character)

        # Proceed to shop and show final character sheet when finished.
        input("\n\nPress ENTER to proceed to shop.")
        os.system('cls')
        show_main_shop(character)
        cf.build_character_sheet(character)
        input("\n\nPress ENTER to exit.")

    return possible_characters, state, selected_race, selected_class


def random_character(character):
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
    show_main_shop(character)
    cf.build_character_sheet(character)
    input("\n\nPress ENTER to exit.")


def show_main_shop(character):
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
