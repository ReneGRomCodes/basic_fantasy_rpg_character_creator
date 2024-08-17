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
            # Assure that combination classes are only shown for Elves.
            if char_race != "Elf" and (char_class == "Fighter/Magic-User" or char_class == "Magic-User/Thief"):
                pass
            else:
                race_class = char_race + " " + char_class
                possible_characters.append(race_class)

    return possible_characters


def select_character(char_list):
    """Take list of possible race-class combinations 'char_list', print them out, let user choose a character and return
    choice 'selected_character' as string."""
    selection_counter = 1

    for char in char_list:
        print(f"{selection_counter:>2} - {char}")
        selection_counter += 1

    while True:
        try:
            character_selection = int(input("\nSelect a character to show race and class description: "))
            selected_character = char_list[character_selection - 1]
            break
        except IndexError:
            print(f"Invalid input. Choose a number between 1 and {selection_counter - 1}.")
            continue
        except ValueError:
            print(f"Invalid input. Choose a number between 1 and {selection_counter - 1}.")
            continue

    return selected_character


def show_char_race_descr(character):
    """Take instance 'character' and print detailed description of character race."""
    os.system('cls')

    with open(character.race_description) as f:
        for line in f:
            output_text = line.rstrip()
            print(output_text)

    input(f"\n\n\n\n\tPRESS ENTER TO SHOW '{character.class_name}' CLASS.")


def show_char_class_descr(character):
    """Take instance 'character' and print detailed description of character class."""
    os.system('cls')

    with open(character.class_description) as f:
        for line in f:
            output_text = line.rstrip()
            print(output_text)

    input("\n\n\n\n\tPRESS ENTER TO CONTINUE.")
