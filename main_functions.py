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


def custom_character(char_race, char_class):
    """Create custom character with user input and print character sheet."""
    os.system('cls')
    # Get ability scores and lists with available races and classes.
    ability_scores, race_list, class_list = cf.ability_score()

    # Race and class selection.
    cf.race_class_selection(char_race, char_class, race_list, class_list)

    # Name the character.
    char_name = cf.name_character()

    # Build character sheet.
    cf.build_character_sheet(char_race, char_class, char_name, ability_scores)


def random_character(char_race, char_class):
    """Create character with random values and print character sheet."""
    os.system('cls')
    # Get random class, race, name and ability scores.
    char_name, ability_scores = cf.random_character_generator(char_race, char_class)

    # Build character sheet.
    cf.build_character_sheet(char_race, char_class, char_name, ability_scores)
