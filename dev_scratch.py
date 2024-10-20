import pygame
from settings import Settings
import sys
import gui.screen_objects
"""This file contains code in development and is meant to try out concepts or just play around with ideas."""

# TODO figure out how to implement different attacks with spear in 'item_instance.py'
# TODO Equip/unequip methods work only for armor right now in 'character_model.py'
# TODO fully implement weapons shop within 'shop_functions.py'
# TODO keep an eye on correct position of 'pygame.quit()' statements in character creation functions in 'main_functions.py'


def show_test_screen():
    """Initialize Pygame and create a window to test GUI elements."""
    # Initialize pygame and create a window.
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("TEST SCREEN")

    # Instantiate screen objects for testing.
    test_text = ("In computer programming, a string is traditionally a sequence of characters, either as a literal "
                 "constant or as some kind of variable. The latter may allow its elements to be mutated and the length "
                 "changed, or it may be fixed (after creation). A string is generally considered as a data type and is "
                 "often implemented as an array data structure of bytes (or words) that stores a sequence of elements, "
                 "typically characters, using some character encoding. String may also denote more general arrays or "
                 "other sequence (or list) data types and structures.\n"
                 "Depending on the programming language and precise data type used, a variable declared to be a string "
                 "may either cause storage in memory to be statically allocated for a predetermined maximum length or "
                 "employ dynamic allocation to allow it to hold a variable number of elements.\n"
                 "When a string appears literally in source code, it is known as a string literal or an anonymous "
                 "string.\n"
                 "In formal languages, which are used in mathematical logic and theoretical computer science, a string "
                 "is a finite sequence of symbols that are chosen from a set called an alphabet.")
    test_object = gui.screen_objects.TextField(screen, test_text, size=20, bg_color=(255,255,255), multi_line=True, image_width=400)

    # Start main loop.
    while True:
        screen.fill(settings.bg_color)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        test_object.draw_text()

        pygame.display.flip()


show_test_screen()
