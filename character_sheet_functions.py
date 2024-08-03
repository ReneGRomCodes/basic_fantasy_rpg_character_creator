import functions as func
import random
"""Functions used to set race/class and build the character sheet."""


def get_ability_race_class(character):
    """Generate abilities for instance 'character', ask for user confirmation and return list 'race_list' and list
    'class_list'."""
    while True:
        print("Let's roll the dice!\n")

        # Generate dictionary for character abilities.
        character.build_ability_dict()

        # Check if abilities allow for valid race-class combinations.
        race_list = func.check_race(character)
        class_list = func.check_class(character)
        if not func.check_valid_race_class(race_list, class_list):
            continue

        # Print ability scores.
        func.show_ability_scores(character)

        if func.check_yes_no("\nKeep these scores and proceed to choose your race and class? (Y/N) "):
            return race_list, class_list
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
    """Prompt user to name character and set 'character.name'."""
    while True:
        char_name = input(f"Name your {character.race_name} {character.class_name}: ")

        if func.check_yes_no(f"Do you want your character to be named '{char_name}'? (Y/N) "):
            character.set_name(char_name)
            break
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
    """Create random character, prompt user for 'char_name' and set values for Character instance."""
    while True:

        # Generate dictionary for character abilities.
        character.build_ability_dict()

        # Check if abilities allow for valid race-class combinations.
        race_list = func.check_race(character)
        class_list = func.check_class(character)
        if not func.check_valid_race_class(race_list, class_list):
            continue

        # Choose random character and set values.
        character.set_race(race_list[random.randint(0, (len(race_list)-1))])
        character.set_class(class_list[random.randint(0, (len(class_list)-1))])
        character.set_saving_throws()
        character.set_specials()
        character.set_hp()
        character.set_starting_money()

        # prompt user for name.
        name_character(character)
        break


def build_character_sheet(character):
    """Take instance 'character' and string 'char_name' and print character sheet."""

    print(f"{character.name.upper():<25}Level: 1")
    print(f"{character.race_name} {character.class_name:<15}XP: 0 ({character.next_level_xp})")
    print(f"\nArmor Class: {character.armor_class:<8}HP: {character.hp:<8}"
          f"Attack Bonus: +{character.attack_bonus}")
    print("\nAbilities:")
    func.show_ability_scores(character)
    print("\nSaving Throws:")
    show_saving_throws(character)
    print("\nSpecial Abilities:")
    show_special_abilities(character)
    print(f"\nMoney: {character.money}")
    print(f"Equipment:")
