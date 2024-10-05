import os
import character_creation_functions as cf
import functions as func
import shop_functions as sf
import pygame
import sys
"""Main functions used in 'main.py'."""


def handle_events(screen, character, state, gui_elements, mouse_pos):
    """Check and handle pygame events for 'run_character_creator()' in 'main.py'. Set and return 'state'"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "title_screen":
            if event.type == pygame.KEYUP:
                return "main_menu"
            elif event.type == pygame.MOUSEBUTTONUP:
                if screen.get_rect().collidepoint(mouse_pos):
                    return "main_menu"

        elif state == "main_menu":
            if event.type == pygame.MOUSEBUTTONUP:
                if gui_elements["custom"].button_rect.collidepoint(mouse_pos):
                    pygame.quit()  # TODO REMOVE AFTER FURTHER GUI SCREENS ARE IMPLEMENTED!!!
                    return "custom_character"

                if gui_elements["random"].button_rect.collidepoint(mouse_pos):
                    pygame.quit()  # TODO REMOVE AFTER FURTHER GUI SCREENS ARE IMPLEMENTED!!!
                    return "random_character"


    return state


def show_title_screen(screen, gui_elements):
    """Show title screen."""

    # Assign gui_elements to variables.
    spacing = gui_elements["title_screen_spacing"]
    title = gui_elements["title"]
    subtitle = gui_elements["subtitle"]
    copyright_notice = gui_elements["copyright_notice"]

    # Position title, subtitle and copyright notice.
    title.text_rect.centerx = screen.get_rect().centerx
    title.text_rect.bottom = screen.get_rect().centery - spacing
    subtitle.text_rect.centerx = screen.get_rect().centerx
    subtitle.text_rect.top = screen.get_rect().centery + spacing
    copyright_notice.text_rect.centerx = screen.get_rect().centerx
    copyright_notice.text_rect.bottom = screen.get_rect().bottom - spacing

    title.draw_text()
    subtitle.draw_text()
    copyright_notice.draw_text()


def show_menu(screen, gui_elements, mouse_pos):
    """Display main menu."""

    # Assign gui_elements to variables.
    spacing = gui_elements["menu_title_spacing"]
    main_menu = gui_elements["main_menu"]
    custom = gui_elements["custom"]
    random = gui_elements["random"]

    # Positioning.
    custom.button_rect.centerx = screen.get_rect().centerx
    custom.button_rect.bottom = screen.get_rect().centery
    random.button_rect.centerx = screen.get_rect().centerx
    random.button_rect.top = screen.get_rect().centery
    main_menu.text_rect.bottom = custom.button_rect.top - spacing

    # Draw elements on screen.
    main_menu.draw_text()
    custom.draw_button(mouse_pos)
    random.draw_button(mouse_pos)


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

    # Proceed to shop and show final character sheet when finished.
    input("\n\nPress ENTER to proceed to shop.")
    os.system('cls')
    show_main_shop(character)
    cf.build_character_sheet(character)
    input("\n\nPress ENTER to exit.")


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

    # Proceed to shop and show final character sheet when finished.
    input("\n\nPress ENTER to proceed to shop.")
    os.system('cls')
    show_main_shop(character)
    cf.build_character_sheet(character)
    input("\n\nPress ENTER to exit.")


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
