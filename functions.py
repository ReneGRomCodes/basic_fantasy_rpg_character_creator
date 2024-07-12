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


def check_race(con, cha, int, dex, str):
    """Check character ability values for possible races to choose and return them in list 'possible_races'."""
    possible_races = ["Humans"]  # Humans have no minimum requirements.

    if con >= 9 and cha <= 17:
        possible_races.append("Dwarf")
    if int >= 9 and con <= 17:
        possible_races.append("Elf")
    if dex >= 9 and str <= 17:
        possible_races.append("Halfling")

    return possible_races


def check_class(wis, str, int, dex):
    """Check character ability values for possible classes to choose and return them in list 'possible_classes'."""
    possible_classes = []

    if wis >= 9:
        possible_classes.append("Cleric")
    if str >= 9:
        possible_classes.append("Fighter")
    if int >= 9:
        possible_classes.append("Magic-User")
    if dex >= 9:
        possible_classes.append("Thief")

    return possible_classes


def check_valid_race_class(race_list, class_list):
    """Check if 'class_list' is empty, return 'False' if so. If not check for valid race-class combinations and return
    valid 'race_list' or 'False' if 'race_list' is emptied after check."""
    if not class_list:
        return False
    if class_list == ["Magic-User"] and "Dwarf" in race_list:
        race_list.remove("Dwarf")
    if class_list == ["Magic-User"] and "Halfling" in race_list:
        race_list.remove("Halfling")
    if not race_list:
        return False

    return race_list
