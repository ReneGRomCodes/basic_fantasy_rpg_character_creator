import os
import character_sheet_functions as cf
"""Main functions used in 'main.py'."""


def show_menu():
    """Print string 'menu' and return string 'menu_prompt'."""
    menu = ("- BASIC FANTASY RPG CHARACTER CREATOR - \n\n"
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
    character.set_saving_throws()
    character.set_specials()
    character.set_hp()
    character.set_starting_money()

    # Name the character.
    char_name = cf.name_character(character)

    # Build character sheet.
    cf.build_character_sheet(character, char_name)


def random_character(character):
    """Create character with random values and print character sheet."""
    os.system('cls')
    # Get random class, race, name and ability scores.
    char_name = cf.random_character_generator(character)

    # Build character sheet.
    cf.build_character_sheet(character, char_name)
