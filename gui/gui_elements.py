import gui.screen_objects as so
"""Initialize instances of classes from 'screen_objects.py' for use in GUI."""


def initialize_screen_elements(screen):
    """Initialize instances of classes from 'screen_objects.py' for use in GUI. Return dict of instances 'gui_elements'.
    NOTE: Instances created have to be then added manually to dict 'gui_elements'!"""
    # Text sizes.
    screen_height = screen.get_rect().height
    title = int(screen_height / 16)
    large = int(screen_height / 20)
    medium = int(screen_height / 25)
    small = int(screen_height / 40)

    # Title screen.
    title_message = "BASIC FANTASY ROLE-PLAYING GAME"
    subtitle_message = "Character Creator"
    copyright_message = ("Basic Fantasy Role-Playing Game, Copyright 2006-2024 Chris Gonnerman. All Rights reserved. "
                         "Distributed under CC BY-SA license. www.basicfantasy.com")
    title = so.TextField(screen, title_message, title)
    subtitle = so.TextField(screen, subtitle_message, large)
    copyright_notice = so.TextField(screen, copyright_message, small)

    # Main menu.
    custom = so.Button(screen, "Custom Character", medium)
    random = so.Button(screen, "Random Character", medium)


    # Dict to be returned containing instances for GUI objects.
    gui_elements = {
        "title": title,
        "subtitle": subtitle,
        "copyright_notice": copyright_notice,
        "custom": custom,
        "random": random,
    }

    return gui_elements
