import os
import character_creation_functions as cf
import functions as func
import shop_functions as sf
import event_handlers as eh
import pygame
"""Main functions used in 'main.py'."""


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
    main_menu = gui_elements["main_menu_title"]
    custom = gui_elements["custom"]
    random = gui_elements["random"]

    # Positioning.
    custom.button_rect.width = screen.get_rect().width / 3
    custom.button_rect.centerx = screen.get_rect().centerx
    custom.button_rect.bottom = screen.get_rect().centery
    random.button_rect.width = screen.get_rect().width / 3
    random.button_rect.centerx = screen.get_rect().centerx
    random.button_rect.top = screen.get_rect().centery
    main_menu.text_rect.bottom = custom.button_rect.top - spacing

    # Draw elements on screen.
    main_menu.draw_text()
    custom.draw_button(mouse_pos)
    random.draw_button(mouse_pos)


def custom_character(screen, state, character, race_list, class_list, gui_elements, mouse_pos):
    """Create custom character based on user input and return state for main loop."""
    if state == "set_abilities":
        # Generate dictionary for character abilities.
        character.set_ability_dict()
        # Check if character abilities allow for any valid race-class combinations.
        race_list, class_list = cf.get_race_class_lists(character)
        if func.check_valid_race_class(race_list, class_list):
            state = "show_abilities"
        else:
            state = "set_abilities"

    elif state == "show_abilities":
        # Display ability score screen.
        cf.show_ability_scores_screen(screen, character, gui_elements, mouse_pos)
        race_list, class_list, state = eh.custom_character_events(state, character, race_list, class_list, gui_elements, mouse_pos)

    elif state == "race_class_selection":
        # Display race/class selection screen.
        cf.show_race_class_selection_screen(screen, character, gui_elements, race_list, class_list, mouse_pos)
        # Race and class selection.
        cf.race_class_selection(character, race_list, class_list)
        # Set values in character instance based on race and class.
        cf.set_character_values(character)

        race_list, class_list, state = eh.custom_character_events(state, character, race_list, class_list, gui_elements, mouse_pos)

    elif state == "custom_character_4":
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

    return race_list, class_list, state


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
