import functions as func
import random
"""Functions used to set race/class and build the character sheet."""


def get_ability_score():
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

        if func.check_yes_no("\nKeep these scores and proceed to choose your race and class? (Y/N) "):
            return ability_scores, race_list, class_list
        else:
            continue


def race_class_selection(character, race_list, class_list):
    """Take lists of possible races and classes, 'race_list' and 'class_list', check for allowed combination, let user
    choose a race/class combination and set race and class in instance 'character'."""
    while True:
        possible_characters = func.build_race_class_list(race_list, class_list)
        selected_character = func.select_character(possible_characters)

        # Split selected 'character' into variables for race and class and call class methods 'set_race()' and
        # 'set_class()'.
        character.set_race(selected_character.split(" ")[0])
        character.set_class(selected_character.split(" ")[1])
        # Show description of selected race and class.
        func.show_char_race_descr(character)
        func.show_char_class_descr(character)

        # if-else block to assure grammatically correct prompt... because it would bother me to no end.
        if character.race_name == "Elf":
            if func.check_yes_no(f"\n\n\n\n\n\tDO YOU WANT TO BE AN '{selected_character}'? (Y/N) "):
                break
            else:
                continue
        else:
            if func.check_yes_no(f"\n\n\n\n\n\tDO YOU WANT TO BE A '{selected_character}'? (Y/N) "):
                break
            else:
                continue


def name_character(character):
    """Prompt user to name character and return string 'char_name'."""
    while True:
        char_name = input(f"Name your {character.race_name} {character.class_name}: ")

        if func.check_yes_no(f"Do you want your character to be named '{char_name}'? (Y/N) "):
            return char_name
        else:
            continue


def show_saving_throws(character):
    """Print formatted output of dict 'saving_throws' from instance 'character'."""
    for k, v in character.saving_throws.items():
        print(f"{k:<22} +{v:>2}")


def show_special_abilities(character):
    """Print formatted output of list 'specials' from instance 'character'."""
    for special in character.specials:
        print(f" - {special}")


def random_character_generator(character):
    """Create random character, prompt user for 'char_name' and return 'ability_scores' and 'char_name'."""
    while True:
        # Generate dictionary for character abilities.
        ability_scores = func.build_ability_dict()

        # Check if abilities allow for valid race-class combinations.
        race_list = func.check_race(ability_scores)
        class_list = func.check_class(ability_scores)
        if not func.check_valid_race_class(race_list, class_list):
            continue

        # Choose random character and set values.
        character.set_race(race_list[random.randint(0, (len(race_list)-1))])
        character.set_class(class_list[random.randint(0, (len(class_list)-1))])
        character.set_saving_throws()
        character.set_specials()
        character.set_hp(ability_scores)
        character.set_starting_money()

        # prompt user for name.
        char_name = name_character(character)

        return char_name, ability_scores


def build_character_sheet(character, char_name, ability_scores):
    """Take instance 'character', string 'char_name' and dictionary 'ability_scores', define remaining variables and
    print character sheet."""
    # Get remaining character variables.
    armor_class = 0  # Value changes with ARMOR after implementation of the shop.
    attack_bonus = 1  # Default for level 1 characters.

    # Build Character Sheet.
    print(f"{char_name.upper():<25}Level: 1")
    print(f"{character.race_name} {character.class_name:<15}XP: 0 ({character.next_level_xp})")
    print(f"\nArmor Class: {armor_class:<8}HP: {character.hp:<8}"
          f"Attack Bonus: +{attack_bonus}")
    print("\nAbilities:")
    func.show_ability_scores(ability_scores)
    print("\nSaving Throws:")
    show_saving_throws(character)
    print("\nSpecial Abilities:")
    show_special_abilities(character)
    print(f"\nMoney: {character.starting_money}")
    print(f"Equipment:")
