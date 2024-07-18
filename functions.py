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
    """Generate random value for ability score, apply bonus/penalty and return both values in list
    'ability_score' with the base score at index 0 and the bonus/penalty at index 1."""
    ability_score = [dice_roll(3, 6)]

    if ability_score[0] <= 3:
        ability_score.append(-3)
        return ability_score
    elif ability_score[0] <= 5:
        ability_score.append(-2)
        return ability_score
    elif ability_score[0] <= 8:
        ability_score.append(-1)
        return ability_score
    elif ability_score[0] <= 12:
        ability_score.append(0)
        return ability_score
    elif ability_score[0] <= 15:
        ability_score.append(1)
        return ability_score
    elif ability_score[0] <= 17:
        ability_score.append(2)
        return ability_score
    else:
        ability_score.append(3)
        return ability_score


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
        # 'Pre-formatting' ability name and bonus/penalty for better code-readability further down in print-statement.
        abilities_name = f"{ability}:"
        bonus_penalty = f"{abilities_dict[key][1]}"

        # Check bonus/penalty for positive or negative value to apply correct prefix in output or give out an empty
        # string if bonus_penalty is 0.
        if abilities_dict[key][1] > 0:
            bonus_penalty = f"+{bonus_penalty}"
        elif abilities_dict[key][1] == 0:
            bonus_penalty = ""
        else:
            pass

        print(f"{abilities_name:<17} {abilities_dict[key][0]:>2} {bonus_penalty:>4}")


def check_race(abilities_dict):
    """Check character ability values from 'abilities_dict' for possible races to choose and return them in list
    'possible_races'."""
    possible_races = ["Human"]  # Humans have no minimum requirements.

    if abilities_dict["con"][0] >= 9 and abilities_dict["cha"][0] <= 17:
        possible_races.append("Dwarf")
    if abilities_dict["int"][0] >= 9 and abilities_dict["con"][0] <= 17:
        possible_races.append("Elf")
    if abilities_dict["dex"][0] >= 9 and abilities_dict["str"][0] <= 17:
        possible_races.append("Halfling")

    return possible_races


def check_class(abilities_dict):
    """Check character ability values from 'abilities_dict' for possible classes to choose and return them in list
    'possible_classes'."""
    possible_classes = []

    if abilities_dict["wis"][0] >= 9:
        possible_classes.append("Cleric")
    if abilities_dict["str"][0] >= 9:
        possible_classes.append("Fighter")
    if abilities_dict["int"][0] >= 9:
        possible_classes.append("Magic-User")
    if abilities_dict["dex"][0] >= 9:
        possible_classes.append("Thief")

    return possible_classes


def check_valid_race_class(race_list, class_list):
    """Check if 'class_list' is empty, return 'False' if so. If not check for valid race-class combinations and return
    valid 'race_list'. NOTE: returned list can be empty at after this function executes."""

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


def show_race_descriptions():
    """Print detailed description of playable races from 'races_description.txt'."""
    race_files = ["descr/dwarves.txt", "descr/elves.txt", "descr/halflings.txt", "descr/humans.txt"]
    # Page counter for 'book feeling' of race description output.
    page = 1

    for race in race_files:
        with open(race) as f:
            for line in f:
                output_text = line.rstrip()
                print(output_text)

            if page == 4:
                input("\n\nPRESS ENTER TO RETURN TO CHARACTER SELECTION.")
                os.system('cls')
            else:
                input(f"\n\nPAGE {page}/4 - PRESS ENTER TO GO TO NEXT PAGE.")
                os.system('cls')
                page += 1


def show_class_descriptions():
    """Print detailed description of playable classes from 'classes_description'.txt."""
    file = "descr/classes_description.txt"
    with open(file) as f:
        for line in f:
            output_text = line.rstrip()
            print(output_text)
            input()
