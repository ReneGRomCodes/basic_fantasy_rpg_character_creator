import pygame
import sys
import main_functions as mf
import character_sheet_functions as cf
from functions import check_yes_no
import character_model as char
import threading
"""Main module for the 'Basic Fantasy RPG Character Creator'. This module serves as the entry point for the application.
It initializes the program and starts the main functionality."""


def pygame_setup():
    """Initialize Pygame and create a window."""
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Basic Fantasy RPG Character Creator")

    # Loop to keep Pygame running and responsive during migration
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # screen.fill((30, 30, 30))
        pygame.display.flip()


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


# Run Pygame setup in a separate thread so it doesn’t block the console logic
pygame_thread = threading.Thread(target=pygame_setup)
pygame_thread.start()

# Run the character creator in the main thread
run_character_creator()
