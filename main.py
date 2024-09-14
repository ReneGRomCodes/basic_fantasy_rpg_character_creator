import main_functions as mf
import character_sheet_functions as cf
from functions import check_yes_no
import character_model as char
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def run_character_creator():
    """Initialize main loop for character creation."""

    # Initialize instance of class 'Character' to set and store values.
    character = char.Character()

    menu_prompt = mf.show_menu()
    keep_char_prompt = "\n\nDO YOU WANT TO KEEP THIS CHARACTER AND PROCEED TO THE SHOP (Y/N)? "

    while True:
        try:
            user_input = int(input(menu_prompt))

            if user_input == 1:
                # Create custom character.
                mf.custom_character(character)

                # Prompt user to create another character or exit.
                if not check_yes_no(keep_char_prompt):
                    character.reset_character()
                    mf.show_menu()
                    continue
                else:
                    break

            elif user_input == 2:
                # Create random character.
                mf.random_character(character)

                # Prompt user to create another character or exit.
                if not check_yes_no(keep_char_prompt):
                    character.reset_character()
                    mf.show_menu()
                    continue
                else:
                    break

        except ValueError:
            continue

    # Show item shop.
    mf.show_main_shop(character)

    # Show final character sheet.
    cf.build_character_sheet(character)
    input("\nPress Enter to exit")


run_character_creator()
