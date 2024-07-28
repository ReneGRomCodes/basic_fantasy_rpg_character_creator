import main_functions as mf
import functions as func
import os
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def run_character_creator():
    """Initialize main loop for character creation."""
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
                char_race, char_class = mf.race_class_selection(race_list, class_list)

                # Name the character.
                char_name = mf.name_character()

                # Build character sheet.
                mf.build_character_sheet(char_class, char_race, char_name, ability_scores)

                # Prompt user to create another character or exit.
                another_character = input(another_character_prompt)
                if func.check_yes_no(another_character, another_character_prompt):
                    mf.show_menu()
                    continue
                else:
                    break

            elif user_input == 2:
                os.system('cls')
                # Get random class, race, name and ability scores.
                char_class, char_race, char_name, ability_scores = mf.random_character_generator()

                # Build character sheet.
                mf.build_character_sheet(char_class, char_race, char_name, ability_scores)

                # Prompt user to create another character or exit.
                another_character = input(another_character_prompt)
                if func.check_yes_no(another_character, another_character_prompt):
                    mf.show_menu()
                    continue
                else:
                    break

        except ValueError:
            continue

    input("Press Enter to exit")


run_character_creator()
