import gui.screen_objects as so
import descr.abilities
from character_creation_functions import race_class_selection

"""Initialize instances of classes from 'screen_objects.py' for use in GUI."""


def initialize_screen_elements(screen):
    """Initialize instances of classes from 'screen_objects.py' for use in GUI in addition to default size and spacing
    values for automatic scalability of screen objects. Return dict of instances 'gui_elements'.
    NOTE: Instances created have to be then added manually to dict 'gui_elements'!"""

    # Initialize dictionaries from 'descr' package.
    ability_descr = descr.abilities.get_ability_descr()

    # Size and spacing variables that are calculated based on screen size for scalability.
    screen_height, screen_width = screen.get_rect().height, screen.get_rect().width
    title_size = int(screen_height / 16)
    text_standard = int(screen_height / 30)
    text_large = int(screen_height / 20)
    text_medium = int(screen_height / 25)
    text_small = int(screen_height / 40)
    info_panel_width = int(screen_width / 5)
    title_screen_spacing = int(screen_height / 40)  # Spacing between main title and subtitle on title screen.
    menu_title_spacing = int(screen_height / 30)  # Default spacing between menu title and GUI objects.
    spacing_screen_edge = screen_width / 25  # Default value for distance to edge of screen for GUI objects.
    # Standard buttons, size and default positions.
    button_width = screen_width / 6
    continue_button = so.Button(screen, "Continue", text_medium)
    continue_button.button_rect.width = button_width
    continue_button.button_rect.bottomright = (screen.get_rect().right - spacing_screen_edge,
                                               screen.get_rect().bottom - spacing_screen_edge)
    back_button = so.Button(screen, "Back", text_medium)
    back_button.button_rect.width = button_width
    back_button.button_rect.bottomleft = (screen.get_rect().left + spacing_screen_edge,
                                          screen.get_rect().bottom - spacing_screen_edge)


    # Title screen.
    title_message = "BASIC FANTASY ROLE-PLAYING GAME"
    subtitle_message = "Character Creator"
    copyright_message = ("Basic Fantasy Role-Playing Game, Copyright 2006-2024 Chris Gonnerman. All Rights reserved. "
                         "Distributed under CC BY-SA license. www.basicfantasy.com")
    title = so.TextField(screen, title_message, title_size)
    subtitle = so.TextField(screen, subtitle_message, text_large)
    copyright_notice = so.TextField(screen, copyright_message, text_small)

    # Main menu.
    main_menu_title_text = "- MAIN MENU -"
    main_menu_screen_title = so.TextField(screen, main_menu_title_text, text_large)
    custom = so.Button(screen, "Create Custom Character", text_medium)
    random = so.Button(screen, "Create Random Character", text_medium)

    # Ability scores screen.
    ability_scores_title_text = "- ABILITIES -"
    ability_scores_screen_title = so.TextField(screen, ability_scores_title_text, text_large)
    # Info panels.
    strength_info = so.InfoPanel(screen, ability_descr["str_descr"], text_small, multi_line=True, image_width=info_panel_width)
    dexterity_info = so.InfoPanel(screen, ability_descr["dex_descr"], text_small, multi_line=True, image_width=info_panel_width)
    constitution_info = so.InfoPanel(screen, ability_descr["con_descr"], text_small, multi_line=True, image_width=info_panel_width)
    intelligence_info = so.InfoPanel(screen, ability_descr["int_descr"], text_small, multi_line=True, image_width=info_panel_width)
    wisdom_info = so.InfoPanel(screen, ability_descr["wis_descr"], text_small, multi_line=True, image_width=info_panel_width)
    charisma_info = so.InfoPanel(screen, ability_descr["cha_descr"], text_small, multi_line=True, image_width=info_panel_width)
    # Ability text fields.
    strength_field = so.InteractiveText(screen, "Strength", text_medium, panel=strength_info)
    dexterity_field = so.InteractiveText(screen, "Dexterity", text_medium, panel=dexterity_info)
    constitution_field = so.InteractiveText(screen, "Constitution", text_medium, panel=constitution_info)
    intelligence_field = so.InteractiveText(screen, "Intelligence", text_medium, panel=intelligence_info)
    wisdom_field = so.InteractiveText(screen, "Wisdom", text_medium, panel=wisdom_info)
    charisma_field = so.InteractiveText(screen, "Charisma", text_medium, panel=charisma_info)
    reroll_button = so.Button(screen, "Roll Again", text_medium)

    # Race/class selection screen.
    race_class_selection_title_text = "- RACE / CLASS SELECTION -"
    race_class_selection_screen_title = so.TextField(screen, race_class_selection_title_text, text_large)
    # Race and class text fields.
    race_human_field = so.InteractiveText(screen, "Human", text_medium)
    race_elf_field = so.InteractiveText(screen, "Elf", text_medium)
    race_dwarf_field = so.InteractiveText(screen, "Dwarf", text_medium)
    race_halfling_field = so.InteractiveText(screen, "Halfling", text_medium)
    class_cleric_field = so.InteractiveText(screen, "Cleric", text_medium)
    class_fighter_field = so.InteractiveText(screen, "Fighter", text_medium)
    class_fighter_magic_user_field = so.InteractiveText(screen, "Fighter/Magic-User", text_medium)
    class_magic_user_field = so.InteractiveText(screen, "Magic-User", text_medium)
    class_magic_user_thief_field = so.InteractiveText(screen, "Magic-User/Thief", text_medium)
    class_thief_field = so.InteractiveText(screen, "Thief", text_medium)

    # Dict to be returned containing instances and size/spacing values (for positioning) for GUI objects.
    gui_elements = {
        # Default values for spacing.
        "title_screen_spacing": title_screen_spacing,
        "menu_title_spacing": menu_title_spacing,
        "default_button_width": button_width,
        "default_edge_spacing": spacing_screen_edge,
        # Standard buttons.
        "continue_button": continue_button,
        "back_button": back_button,

        # Title screen.
        "title": title,
        "subtitle": subtitle,
        "copyright_notice": copyright_notice,
        # Main menu.
        "main_menu_title": main_menu_screen_title,
        "custom": custom,
        "random": random,
        # Ability scores screen.
        "abilities_title": ability_scores_screen_title,
        "strength": strength_field,
        "dexterity": dexterity_field,
        "constitution": constitution_field,
        "intelligence": intelligence_field,
        "wisdom": wisdom_field,
        "charisma": charisma_field,
        "reroll_button": reroll_button,
        # Race/class selection screen.
        "race_class_title": race_class_selection_screen_title,
        "possible_races": [race_human_field, race_elf_field, race_dwarf_field, race_halfling_field],
        "possible_classes": [class_cleric_field, class_fighter_field, class_fighter_magic_user_field,
                             class_magic_user_field, class_magic_user_thief_field, class_thief_field],
    }

    return gui_elements
