import main_functions as mf
from functions import check_yes_no as yes_no
import races_classes as rc
import os
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def run_character_creator():
    """Initialize main loop for character creation."""

    # Instances of CharacterRace and CharacterClass to set and store values.
    char_race = rc.CharacterRace()
    char_class = rc.CharacterClass()

    menu_prompt = mf.show_menu()
    another_character_prompt = "\n\nDO YOU WANT TO CREATE ANOTHER CHARACTER (Y/N)? "

    while True:
        try:
            user_input = int(input(menu_prompt))
            if user_input == 1:
                os.system('cls')
                # Get ability scores and lists with available races and classes.
                ability_scores, race_list, class_list = mf.ability_score()

                # Race and class selection.
                mf.race_class_selection(char_race, char_class, race_list, class_list)

                # Name the character.
                char_name = mf.name_character()

                # Build character sheet.
                mf.build_character_sheet(char_race, char_class, char_name, ability_scores)

                # Prompt user to create another character or exit.
                another_character = input(another_character_prompt)
                if yes_no(another_character, another_character_prompt):
                    mf.show_menu()
                    continue
                else:
                    break

            elif user_input == 2:
                os.system('cls')
                # Get random class, race, name and ability scores.
                char_name, ability_scores = mf.random_character_generator(char_race, char_class)

                # Build character sheet.
                mf.build_character_sheet(char_race, char_class, char_name, ability_scores)

                # Prompt user to create another character or exit.
                another_character = input(another_character_prompt)
                if yes_no(another_character, another_character_prompt):
                    mf.show_menu()
                    continue
                else:
                    break

        except ValueError:
            continue

    input("Press Enter to exit")


run_character_creator()
