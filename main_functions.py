import os
import character_sheet_functions as cf
import functions as func
import shop_functions as sf
"""Main functions used in 'main.py'."""


def show_menu():
    """Print string 'menu' and return string 'menu_prompt'."""
    menu = ("- BASIC FANTASY RPG CHARACTER CREATOR -\n\n"
            "Do you want to customize your character or generate a random character?\n"
            "1 - Custom Character\n"
            "2 - Random Character\n\n")
    menu_prompt = "Please enter '1' or '2': "

    print(menu)

    # Return 'menu_prompt' for use in 'run_character_creator()' in 'main.py'
    return menu_prompt


def custom_character(character):
    """Create custom character with user input and print character sheet."""
    os.system('cls')
    # Get ability scores and lists with available races and classes.
    race_list, class_list = cf.get_ability_race_class(character)

    # Race and class selection.
    cf.race_class_selection(character, race_list, class_list)

    # Set values in character instance based on race and class.
    cf.set_character_values(character)

    # Name the character.
    cf.name_character(character)

    # Set amount of starting money.
    cf.set_starting_money(character)
    os.system('cls')

    print("\n\n\t\tCharacter creation complete. Press ENTER to show character sheet.")
    input()
    os.system('cls')

    # Build character sheet.
    cf.build_character_sheet(character)


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


def show_shop():
    """Main loop for shop 'main menu'."""
    shop_sections = ["General Items", "Weapons", "Projectiles", "Armor", "EXIT"]

    while True:
        print(" - SHOP -\n")
        shop_section = func.select_from_list(shop_sections, "\nWhat items do you want to buy? ")
        os.system('cls')

        if shop_section == "General Items":
            sf.show_general_items()
        elif shop_section == "Weapons":
            sf.show_weapons()
        elif shop_section == "Projectiles":
            sf.show_projectiles()
        elif shop_section == "Armor":
            sf.show_armor()
        else:
            break
