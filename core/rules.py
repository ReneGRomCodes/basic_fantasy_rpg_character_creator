import os
import random
"""Helper and check functions to generate and return values in accordance to game rules."""


def dice_roll(n, m):
    """Roll an n number of m-sided dice and return the result."""
    result = 0

    for i in range(n):
        result += random.randint(1, m)

    return result


def get_ability_score():
    """Generate random value for ability score, apply bonus/penalty and return both values in list
    'ability_score' with the base score at index 0 and the bonus/penalty at index 1."""
    ability_score = [dice_roll(3, 6)]

    if ability_score[0] <= 3:
        ability_score.append(-3)
    elif ability_score[0] <= 5:
        ability_score.append(-2)
    elif ability_score[0] <= 8:
        ability_score.append(-1)
    elif ability_score[0] <= 12:
        ability_score.append(0)
    elif ability_score[0] <= 15:
        ability_score.append(1)
    elif ability_score[0] <= 17:
        ability_score.append(2)
    else:
        ability_score.append(3)

    return ability_score


def check_race(character):
    """Check instance 'character' abilities for possible races to choose and return them in list 'race_list'."""
    race_list = ["Human"]  # Humans have no minimum requirements.

    if character.abilities["con"][0] >= 9 and character.abilities["cha"][0] <= 17:
        race_list.append("Dwarf")
    if character.abilities["int"][0] >= 9 and character.abilities["con"][0] <= 17:
        race_list.append("Elf")
    if character.abilities["dex"][0] >= 9 and character.abilities["str"][0] <= 17:
        race_list.append("Halfling")

    return race_list


def check_class(character):
    """Check abilities from instance 'character' for possible classes to choose and return them in list
    'class_list'."""
    class_list = []

    if character.abilities["wis"][0] >= 9:
        class_list.append("Cleric")
    if character.abilities["str"][0] >= 9:
        class_list.append("Fighter")
        if character.abilities["int"][0] >= 9:
            class_list.append("Fighter/Magic-User")
    if character.abilities["int"][0] >= 9:
        class_list.append("Magic-User")
        if character.abilities["dex"][0] >= 9:
            class_list.append("Magic-User/Thief")
    if character.abilities["dex"][0] >= 9:
        class_list.append("Thief")

    return class_list


def get_race_class_lists(character):
    """Generate race and class based on abilities scores for instance 'character' and return lists 'race_list' and
    'class_list'."""
    race_list = check_race(character)
    class_list = check_class(character)

    return race_list, class_list


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


def build_possible_characters_list(race_list, class_list):
    """Take lists of possible races and classes and return list 'possible_characters' with valid race-class
    combinations."""
    possible_characters = []

    for char_race in race_list:
        for char_class in class_list:
            # Exclude Dwarves and Halflings from class 'Magic-User'.
            if char_race in {"Dwarf", "Halfling"} and char_class == "Magic-User":
                pass
            # Assure that combination classes are only shown for Elves.
            elif char_race != "Elf" and char_class in {"Fighter/Magic-User", "Magic-User/Thief"}:
                pass
            else:
                race_class = char_race + " " + char_class
                possible_characters.append(race_class)

    return possible_characters


def set_character_values(character):
    """Set values for instance 'character' of class 'Character'."""
    character.set_saving_throws()
    character.set_specials()
    character.set_hp()
    character.set_armor_class()
    character.set_carrying_capacity()


def set_starting_money():
    """Generate and return random amount of starting money."""
    starting_money = dice_roll(3, 6) * 10

    return starting_money



"""
Functions still in use by console part of the program. DELETE WHEN OBSOLETE!!!
"""

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
