import os
import random
"""Helper and check value functions."""


def dice_roll(n, m):
    """Roll an n number of m-sided dice and return the result."""
    result = 0

    for i in range(n):
        result += random.randint(1, m)

    return result


def check_yes_no(prompt):
    """Take string 'prompt' for user input and check for y/n answer. Return 'True' for y, 'False'
    for n or prompt the user again if any other character is given."""
    user_input = input(prompt)

    while user_input.lower() not in ["y", "n"]:
        user_input = input(prompt)
        continue

    if user_input.lower() == "y":
        os.system('cls')
        return True
    elif user_input.lower() == "n":
        os.system('cls')
        return False


def check_race(character):
    """Check instance 'character' abilities for possible races to choose and return them in list 'possible_races'."""
    possible_races = ["Human"]  # Humans have no minimum requirements.

    if character.abilities["con"][0] >= 9 and character.abilities["cha"][0] <= 17:
        possible_races.append("Dwarf")
    if character.abilities["int"][0] >= 9 and character.abilities["con"][0] <= 17:
        possible_races.append("Elf")
    if character.abilities["dex"][0] >= 9 and character.abilities["str"][0] <= 17:
        possible_races.append("Halfling")

    return possible_races


def check_class(character):
    """Check abilities from instance 'character' for possible classes to choose and return them in list
    'possible_classes'."""
    possible_classes = []

    if character.abilities["wis"][0] >= 9:
        possible_classes.append("Cleric")
    if character.abilities["str"][0] >= 9:
        possible_classes.append("Fighter")
        if character.abilities["int"][0] >= 9:
            possible_classes.append("Fighter/Magic-User")
    if character.abilities["int"][0] >= 9:
        possible_classes.append("Magic-User")
        if character.abilities["dex"][0] >= 9:
            possible_classes.append("Magic-User/Thief")
    if character.abilities["dex"][0] >= 9:
        possible_classes.append("Thief")

    return possible_classes


def check_valid_race_class(race_list, class_list):
    """Check if 'class_list' is empty, return 'False' if so. If not check for valid race-class combinations and remove
     invalid races from 'race_list'. Return 'False' if 'race_list' is empty, 'True' if items remain in 'race_list'
     afterward."""

    # Check if class list is empty.
    if not class_list:
        return False

    # Check if 'Magic-User' is the only class available, therefor excluding Dwarves and Halflings from race selection.
    if class_list == ["Magic-User"] and "Dwarf" in race_list:
        race_list.remove("Dwarf")
    if class_list == ["Magic-User"] and "Halfling" in race_list:
        race_list.remove("Halfling")

    # Check if race list is empty after 'Magic-User' check above and return 'False' or modified 'race_list'.
    if not race_list:
        return False
    else:
        return race_list


def select_from_list(list, prompt):
    """Print out items from list 'list' in numbered and formatted output, prompts for input via string 'prompt' and
    return list item 'selected_item'."""
    invalid_input_message = f"Invalid input. Choose a number between 1 and {len(list)}."

    for index, item in enumerate(list, start=1):
        print(f"{index:>2} - {item}")

    while True:
        try:
            selection = int(input(prompt))
            selected_item = list[selection - 1]
            break
        except IndexError:
            print(invalid_input_message)
            continue
        except ValueError:
            print(invalid_input_message)
            continue

    return selected_item
