import os
import random
"""Functions for character creation."""


def dice_roll(n, m):
    """Roll an n number of m-sided dice and return the result."""
    result = 0

    for i in range(n):
        result += random.randint(1, m)

    return result


def check_yes_no(user_input, prompt):
    """Take string 'user_input' and check for y/n answer. Return 'True' for y, 'False' for n or prompt the user for new
    input if any other character is given."""
    yes_no = ["y", "n"]

    while user_input.lower() not in yes_no:
        user_input = input(prompt)
        continue

    if user_input.lower() == "y":
        os.system('cls')
        return True
    else:
        os.system('cls')
        return False


def get_ability_score():
    """Generate random value for ability score, apply bonus/penalty and return the value."""
    base_score = dice_roll(3, 6)
    if base_score <= 3:
        return base_score - 3
    elif base_score <= 5:
        return base_score - 2
    elif base_score <= 8:
        return base_score - 1
    elif base_score <= 12:
        return base_score
    elif base_score <= 15:
        return base_score + 1
    elif base_score <= 17:
        return base_score + 2
    else:
        return base_score + 3


def build_ability_dict():
    """Build and return dictionary for character abilities"""
    abilities = ["str", "dex", "con", "int", "wis", "cha"]
    abilities_dict = {}

    for item in abilities:
        abilities_dict[item] = get_ability_score()

    return abilities_dict


def show_ability_scores(abilities_dict):
    """Print formatted table of abilities and corresponding scores from dictionary 'abilities_dict'."""
    abilities = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

    for ability, key in zip(abilities, abilities_dict):
        # 'Pre-formatting' ability name for clean left-alignment in print-statement.
        abilities_name = f"{ability}:"
        print(f"{abilities_name:<15} {abilities_dict[key]:>2}")


def check_race(dict):
    """Check character ability values for possible races to choose and return them in list 'possible_races'."""
    possible_races = ["Human"]  # Humans have no minimum requirements.

    if dict["con"] >= 9 and dict["cha"] <= 17:
        possible_races.append("Dwarf")
    if dict["int"] >= 9 and dict["con"] <= 17:
        possible_races.append("Elf")
    if dict["dex"] >= 9 and dict["str"] <= 17:
        possible_races.append("Halfling")

    return possible_races


def check_class(dict):
    """Check character ability values for possible classes to choose and return them in list 'possible_classes'."""
    possible_classes = []

    if dict["wis"] >= 9:
        possible_classes.append("Cleric")
    if dict["str"] >= 9:
        possible_classes.append("Fighter")
    if dict["int"] >= 9:
        possible_classes.append("Magic-User")
    if dict["dex"] >= 9:
        possible_classes.append("Thief")

    return possible_classes


def check_valid_race_class(race_list, class_list):
    """Check if 'class_list' is empty, return 'False' if so. If not check for valid race-class combinations and return
    valid 'race_list'."""

    # Check if class list is empty.
    if not class_list:
        return False

    # Check if 'Magic-User' is the only class available, therefor excluding Dwarves and Halflings from race selection.
    if class_list == ["Magic-User"] and "Dwarf" in race_list:
        race_list.remove("Dwarf")
    if class_list == ["Magic-User"] and "Halfling" in race_list:
        race_list.remove("Halfling")

    return race_list


def build_race_class_list(race_list, class_list):
    """Take lists of possible races and classes and return list 'possible_characters' with valid race-class
    combinations."""
    possible_characters = []
    print("Based on your scores you can choose from the following race-class combinations:\n")

    for char_race in race_list:
        for char_class in class_list:
            # Exclude Dwarves and Halflings from class 'Magic-User'.
            if (char_race == "Dwarf" or char_race == "Halfling") and char_class == "Magic-User":
                pass
            else:
                race_class = char_race + " " + char_class
                possible_characters.append(race_class)

    return possible_characters


def select_character(char_list):
    """Take list of possible race-class combinations 'char_list', print them out, let user choose a character and return
    choice 'character' as string variable."""
    selection_counter = 1

    for char in char_list:
        print(selection_counter, "-", char)
        selection_counter += 1

    while True:
        try:
            character_selection = int(input("\nSelect your character: "))
            character = char_list[character_selection - 1]
            break
        except IndexError:
            print(f"Invalid input. Choose a number between 1 and {selection_counter - 1}.")
            continue
        except ValueError:
            print(f"Invalid input. Choose a number between 1 and {selection_counter - 1}.")
            continue

    return character
