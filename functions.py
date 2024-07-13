import os
import random
"""Functions for character creation."""


def dice_roll(n):
    """Roll an n-sided dice and return the result."""
    return random.randint(1, n)


def get_ability_score():
    """Generate random value for ability score, apply bonus/penalty and return the value."""
    base_score = dice_roll(18)
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


def check_yes_no(user_input, prompt):
    """Take string 'user_input' and check for y/n answer. Return 'True' for y, 'False' for n or prompt the user for new
    input if any other character is given."""
    yes_no = ["y", "n"]

    while user_input.lower() not in yes_no:
        user_input = input(prompt)
        continue

    if user_input.lower() == "y":
        return True
    else:
        os.system('cls')
        return False
