import os
import character_sheet_functions as cf
import functions as func
import shop_functions as sf
import pygame
import sys
"""Main functions used in 'main.py'."""


def handle_events(screen, character, state, gui_elements):
    """Check and handle pygame events for 'run_character_creator()' in 'main.py'. Set and return 'state'"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "title_screen":
            if event.type == pygame.KEYDOWN:
                return "main_menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if screen.get_rect().collidepoint(mouse_position):
                    return "main_menu"

        elif state == "main_menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if gui_elements["custom"].text_rect.collidepoint(mouse_pos):
                    custom_character(character)

                if gui_elements["random"].text_rect.collidepoint(mouse_pos):
                    random_character(character)

    return state


def show_title_screen(screen, gui_elements):
    """Show title screen."""

    # Assign gui_elements to variables.
    title = gui_elements["title"]
    subtitle = gui_elements["subtitle"]
    copyright_notice = gui_elements["copyright_notice"]

    # Position title, subtitle and copyright notice.
    title.text_rect.centerx = screen.get_rect().centerx
    title.text_rect.bottom = screen.get_rect().centery - 20
    subtitle.text_rect.centerx = screen.get_rect().centerx
    subtitle.text_rect.top = screen.get_rect().centery + 20
    copyright_notice.text_rect.centerx = screen.get_rect().centerx
    copyright_notice.text_rect.bottom = screen.get_rect().bottom - 20

    title.draw_text()
    subtitle.draw_text()
    copyright_notice.draw_text()


def show_menu(screen, gui_elements):
    """Display main menu."""

    # Assign gui_elements to variables.
    custom = gui_elements["custom"]
    random = gui_elements["random"]

    # Positioning.
    custom.text_rect.centerx = screen.get_rect().centerx
    custom.text_rect.bottom = screen.get_rect().centery - 20
    random.text_rect.centerx = screen.get_rect().centerx
    random.text_rect.top = screen.get_rect().centery + 20

    # Draw elements on screen.
    custom.draw_text()
    random.draw_text()


def custom_character(character):
    """Create custom character with user input and print character sheet."""
    os.system('cls')
    # Get ability scores and lists with available races and classes.
    race_list, class_list = cf.get_ability_race_class(character)

    # Race and class selection.
    cf.race_class_selection(character, race_list, class_list)

    # Set values in character instance based on race and class.
    cf.set_character_values(character)

    # Name the character.
    cf.name_character(character)

    # Set amount of starting money.
    cf.set_starting_money(character)
    os.system('cls')

    print("\n\n\t\tCharacter creation complete. Press ENTER to show character sheet.")
    input()
    os.system('cls')

    # Build character sheet.
    cf.build_character_sheet(character)


def random_character(character):
    """Create character with random values and print character sheet."""
    os.system('cls')
    # Get random class, race, name and ability scores.
    cf.random_character_generator(character)

    print("\n\n\t\tCharacter creation complete. Press ENTER to show character sheet.")
    input()
    os.system('cls')

    # Build character sheet.
    cf.build_character_sheet(character)


def show_main_shop(character):
    """Main loop for shop 'main menu'."""
    shop_sections = ["General Items", "Weapons", "Projectiles", "Armor", "Inventory", "EXIT"]

    while True:
        print(" - SHOP -\n")
        shop_section = func.select_from_list(shop_sections, "\nWhat items do you want to buy? ")
        os.system('cls')

        if shop_section == "General Items":
            sf.set_shop(character, shop_section)
        elif shop_section == "Weapons":
            sf.set_shop(character, shop_section)
        elif shop_section == "Projectiles":
            sf.set_shop(character, shop_section)
        elif shop_section == "Armor":
            sf.set_shop(character, shop_section)
        elif shop_section == "Inventory":
            sf.set_shop(character, shop_section)
        else:
            break
