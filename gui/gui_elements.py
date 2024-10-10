import gui.screen_objects as so
"""Initialize instances of classes from 'screen_objects.py' for use in GUI."""


def initialize_screen_elements(screen):
    """Initialize instances of classes from 'screen_objects.py' for use in GUI. Return dict of instances 'gui_elements'.
    NOTE: Instances created have to be then added manually to dict 'gui_elements'!"""
    # Text sizes from biggest to smallest. Sizes are calculated based on screen size for scalability.
    screen_height = screen.get_rect().height
    title_size = int(screen_height / 16)
    large = int(screen_height / 20)
    medium = int(screen_height / 25)
    small = int(screen_height / 40)

    # Title screen.
    title_message = "BASIC FANTASY ROLE-PLAYING GAME"
    subtitle_message = "Character Creator"
    copyright_message = ("Basic Fantasy Role-Playing Game, Copyright 2006-2024 Chris Gonnerman. All Rights reserved. "
                         "Distributed under CC BY-SA license. www.basicfantasy.com")
    title = so.TextField(screen, title_message, title_size)
    subtitle = so.TextField(screen, subtitle_message, large)
    copyright_notice = so.TextField(screen, copyright_message, small)

    # Buttons.
    continue_button = so.Button(screen, "Continue", medium)
    back_button = so.Button(screen, "Back", medium)

    # Main menu.
    main_menu_title = "MAIN MENU"
    main_menu = so.TextField(screen, main_menu_title, large)
    custom = so.Button(screen, "Create Custom Character", medium)
    random = so.Button(screen, "Create Random Character", medium)

    # Ability scores screen.
    strength_field = so.LabeledText(screen, "Strength", small)
    dexterity_field = so.LabeledText(screen, "Dexterity", small)
    constitution_field = so.LabeledText(screen, "Constitution", small)
    intelligence_field = so.LabeledText(screen, "Intelligence", small)
    wisdom_field = so.LabeledText(screen, "Wisdom", small)
    charisma_field = so.LabeledText(screen, "Charisma", small)
    reroll_button = so.Button(screen, "Roll Again", medium)


    # Dict to be returned containing instances and spacing values (for positioning) for GUI objects.
    gui_elements = {
        # Variables for spacing.
        "title_screen_spacing": int(screen.get_rect().height / 40),
        "menu_title_spacing": int(screen.get_rect().height / 30),
        # Buttons.
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
