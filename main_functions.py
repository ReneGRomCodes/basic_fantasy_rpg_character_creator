import functions as func
import random
"""Main functions for character creation used in 'main.py'."""


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


def ability_score():
    """Generate dictionary 'ability_scores', ask for user confirmation and return 'ability_scores', list 'race_list' and
     list 'class_list'."""
    while True:
        print("Let's roll the dice!\n")

        # Generate dictionary for character abilities.
        ability_scores = func.build_ability_dict()

        # Check if abilities allow for valid race-class combinations.
        race_list = func.check_race(ability_scores)
        class_list = func.check_class(ability_scores)
        if not func.check_valid_race_class(race_list, class_list):
            continue

        # Print ability scores.
        func.show_ability_scores(ability_scores)

        ability_prompt = "Keep these scores and proceed to choose your race and class? (Y/N) "
        ability_proceed = input("\n" + ability_prompt)

        if func.check_yes_no(ability_proceed, ability_prompt):
            return ability_scores, race_list, class_list
        else:
            continue


def race_class_selection(race_list, class_list):
    """Take lists of possible races and classes, 'race_list' and 'class_list', check for allowed combination, let user
    choose a race/class combination and return string 'char_race' and string 'char_class'."""
    while True:
        possible_characters = func.build_race_class_list(race_list, class_list)
        character = func.select_character(possible_characters)

        # Split selected 'character' into variables for race and class.
        char_race = character.split(" ")[0]
        char_class = character.split(" ")[1]
        # Show description of selected race and class.
        func.show_char_race_descr(char_race)
        func.show_char_class_descr(char_class)

        # if-else block to assure grammatically correct prompt... because it would bother me to no end.
        if char_race == "Elf":
            char_prompt = f"\n\n\n\n\tDO YOU WANT TO BE AN '{character}'? (Y/N) "
            char_proceed = input("\n" + char_prompt)
        else:
            char_prompt = f"\n\n\n\n\tDO YOU WANT TO BE A '{character}'? (Y/N) "
            char_proceed = input("\n" + char_prompt)

        if func.check_yes_no(char_proceed, char_prompt):
            return char_race, char_class
        else:
            continue


def name_character(prompt="Name your character: "):
    """Prompt user to name character and return string 'char_name'."""
    while True:
        char_name = input(prompt)

        name_prompt = f"Do you want your character to be named '{char_name}'? (Y/N) "
        name_proceed = input(name_prompt)

        if func.check_yes_no(name_proceed, name_prompt):
            return char_name
        else:
            continue


def random_character_generator():
    """Create random character, prompt user for 'char_name' and return 'ability_scores', 'char_race', 'char_class' and
    'char_name'."""
    while True:
        # Generate dictionary for character abilities.
        ability_scores = func.build_ability_dict()

        # Check if abilities allow for valid race-class combinations.
        race_list = func.check_race(ability_scores)
        class_list = func.check_class(ability_scores)
        if not func.check_valid_race_class(race_list, class_list):
            continue

        # Choose random race and class and assign default character name "ADVENTURER".
        char_race = race_list[random.randint(0, (len(race_list)-1))]
        char_class = class_list[random.randint(0, (len(class_list)-1))]
        char_name = name_character(f"Name your {char_race} {char_class}: ")

        return char_class, char_race, char_name, ability_scores


def build_character_sheet(char_class, char_race, char_name, ability_scores):
    """Take strings 'char_class', 'char_race', 'char_name' and dictionary 'ability_scores', define remaining variables
    and print character sheet."""
    # Get remaining character variables.
    armor_class = 0  # Value changes with ARMOR after implementation of the shop.
    attack_bonus = 1  # Default for level 1 characters.

    # Build Character Sheet.
    print(f"{char_name.upper():<25}Level: 1")
    print(f"{char_race} {char_class:<15}XP: 0 ({func.get_next_level_xp(char_class)})")
    print(f"\nArmor Class: {armor_class:<8}HP: {func.get_hp(char_race, char_class, ability_scores):<8}"
          f"Attack Bonus: +{attack_bonus}")
    print("\nAbilities:")
    func.show_ability_scores(ability_scores)
    print("\nSaving Throws:")
    func.show_saving_throws(char_race, char_class)
    print("\nSpecial Abilities:")
    func.show_special_abilities(char_race, char_class)
    print(f"\nMoney: {func.dice_roll(3, 6) * 10}")
    print(f"Equipment:")
