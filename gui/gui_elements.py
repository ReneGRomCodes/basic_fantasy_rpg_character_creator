import gui.screen_objects as so
"""Initialize instances of classes from 'screen_objects.py' for use in GUI."""


def initialize_screen_elements(screen):
    """Initialize instances of classes from 'screen_objects.py' for use in GUI in addition to default size and spacing
    values for automatic scalability of screen objects. Return dict of instances 'gui_elements'.
    NOTE: Instances created have to be then added manually to dict 'gui_elements'!"""
    # Size and spacing variables that are calculated based on screen size for scalability.
    screen_height, screen_width = screen.get_rect().height, screen.get_rect().width
    title_size = int(screen_height / 16)
    text_large = int(screen_height / 20)
    text_medium = int(screen_height / 25)
    text_small = int(screen_height / 40)
    button_spacing = screen_width / 25
    button_width = screen_width / 6
    # Standard buttons, size and default positions.
    continue_button = so.Button(screen, "Continue", text_medium)
    continue_button.button_rect.width = button_width
    continue_button.button_rect.bottomright = (screen.get_rect().right - button_spacing,
                                               screen.get_rect().bottom - button_spacing)
    back_button = so.Button(screen, "Back", text_medium)
    back_button.button_rect.width = button_width
    back_button.button_rect.bottomleft = (screen.get_rect().left + button_spacing,
                                          screen.get_rect().bottom - button_spacing)


    # Title screen.
    title_message = "BASIC FANTASY ROLE-PLAYING GAME"
    subtitle_message = "Character Creator"
    copyright_message = ("Basic Fantasy Role-Playing Game, Copyright 2006-2024 Chris Gonnerman. All Rights reserved. "
                         "Distributed under CC BY-SA license. www.basicfantasy.com")
    title = so.TextField(screen, title_message, title_size)
    subtitle = so.TextField(screen, subtitle_message, text_large)
    copyright_notice = so.TextField(screen, copyright_message, text_small)

    # Main menu.
    main_menu_title = "- MAIN MENU -"
    main_menu = so.TextField(screen, main_menu_title, text_large)
    custom = so.Button(screen, "Create Custom Character", text_medium)
    random = so.Button(screen, "Create Random Character", text_medium)

    # Ability scores screen.
    strength_field = so.LabeledText(screen, "Strength", text_small)
    dexterity_field = so.LabeledText(screen, "Dexterity", text_small)
    constitution_field = so.LabeledText(screen, "Constitution", text_small)
    intelligence_field = so.LabeledText(screen, "Intelligence", text_small)
    wisdom_field = so.LabeledText(screen, "Wisdom", text_small)
    charisma_field = so.LabeledText(screen, "Charisma", text_small)
    reroll_button = so.Button(screen, "Roll Again", text_medium)


    # Dict to be returned containing instances and size/spacing values (for positioning) for GUI objects.
    gui_elements = {
        # Default variables for spacing.
        "title_screen_spacing": int(screen.get_rect().height / 40),
        "menu_title_spacing": int(screen.get_rect().height / 30),
        "default_button_width": button_width,
        "default_button_spacing": button_spacing,
        # Standard buttons.
        "continue_button": continue_button,
        "back_button": back_button,

        # Title screen.
        "title": title,
        "subtitle": subtitle,
        "copyright_notice": copyright_notice,
        # Main menu.
        "main_menu": main_menu,
        "custom": custom,
        "random": random,
        # Ability scores screen.
        "strength": strength_field,
        "dexterity": dexterity_field,
        "constitution": constitution_field,
        "intelligence": intelligence_field,
        "wisdom": wisdom_field,
        "charisma": charisma_field,
        "reroll_button": reroll_button,
    }

    return gui_elements
