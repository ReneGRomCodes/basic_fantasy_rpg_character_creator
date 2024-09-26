import gui.screen_objects as so
"""Initialize instances of classes from 'screen_objects.py' for use in GUI."""


def initialize_screen_elements(screen):
    """Initialize instances of classes from 'screen_objects.py' for use in GUI. Return dict of instances 'gui_elements'.
    NOTE: Instances created have to be then added manually to dict 'gui_elements'!"""

    # Title screen.
    title_message = "BASIC FANTASY ROLE-PLAYING GAME"
    subtitle_message = "Character Creator"
    copyright_message = ("Basic Fantasy Role-Playing Game, Copyright 2006-2024 Chris Gonnerman. All Rights reserved. "
                         "Distributed under CC BY-SA license. www.basicfantasy.com")

    title = so.TextField(screen, title_message, size=48)
    subtitle = so.TextField(screen, subtitle_message, size=40)
    copyright_notice = so.TextField(screen, copyright_message)


    # Main menu.
    custom = so.TextField(screen, "Custom Character")
    random = so.TextField(screen, "Random Character")


    # Dict to be returned containing instances for GUI objects.
    gui_elements = {
        "title": title,
        "subtitle": subtitle,
        "copyright_notice": copyright_notice,
        "custom": custom,
        "random": random,
    }

    return gui_elements
