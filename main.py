import main_functions as mf
from functions import check_yes_no as yes_no
import character_object as char
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def run_character_creator():
    """Initialize main loop for character creation."""

    # Instances of CharacterRace and CharacterClass to set and store values.
    character = char.Character()

    menu_prompt = mf.show_menu()

    while True:
        try:
            user_input = int(input(menu_prompt))

            if user_input == 1:
                # Create custom character.
                mf.custom_character(character)

                # Prompt user to create another character or exit.
                if yes_no("\n\nDO YOU WANT TO CREATE ANOTHER CHARACTER (Y/N)? "):
                    mf.show_menu()
                    continue
                else:
                    break

            elif user_input == 2:
                # Create random character.
                mf.random_character(character)

                # Prompt user to create another character or exit.
                if yes_no("\n\nDO YOU WANT TO CREATE ANOTHER CHARACTER (Y/N)? "):
                    mf.show_menu()
                    continue
                else:
                    break

        except ValueError:
            continue

    input("Press Enter to exit")


run_character_creator()
