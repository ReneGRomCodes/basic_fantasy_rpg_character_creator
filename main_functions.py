import os
import character_sheet_functions as cf
import functions as func
import shop_functions as sf
import screen_objects as so

"""Main functions used in 'main.py'."""


def show_title_screen(screen):
    """Show title screen."""
    # Strings for instances of class 'TextField'.
    title_message = "BASIC FANTASY ROLE-PLAYING GAME"
    subtitle_message = "Character Creator"
    copyright_message = ("Basic Fantasy Role-Playing Game, Copyright 2006-2024 Chris Gonnerman. All Rights reserved. "
                         "Distributed under CC BY-SA license. www.basicfantasy.com")

    # Create and position title.
    title = so.TextField(screen, title_message, size=48)
    title.text_rect.centerx = screen.get_rect().centerx
    title.text_rect.bottom = screen.get_rect().centery - 20

    # Create and position subtitle.
    subtitle = so.TextField(screen, subtitle_message, size=40)
    subtitle.text_rect.centerx = screen.get_rect().centerx
    subtitle.text_rect.top = screen.get_rect().centery + 20

    # Create and position copyright notice.
    copyright_notice = so.TextField(screen, copyright_message)
    copyright_notice.text_rect.centerx = screen.get_rect().centerx
    copyright_notice.text_rect.bottom = screen.get_rect().bottom - 20

    title.draw_text()
    subtitle.draw_text()
    copyright_notice.draw_text()


def show_menu():
    """Print string 'menu' and return string 'menu_prompt'."""
    menu = ("- BASIC FANTASY RPG CHARACTER CREATOR -\n\n"
            "Do you want to customize your character or generate a random character?\n"
            "1 - Custom Character\n"
            "2 - Random Character\n\n")
    menu_prompt = "Please enter '1' or '2': "

    print(menu)

    # Return 'menu_prompt' for use in 'run_character_creator()' in 'main.py'
    return menu_prompt


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
