import pygame.font
import gui.screen_objects as so
from descr import abilities, races, classes
import pygame_textinput
"""Initialize instances of classes from 'screen_objects.py' for use in GUI."""


def initialize_screen_elements(screen):
    """Initialize instances of classes from 'screen_objects.py' for use in GUI in addition to default size and spacing
    values for automatic scalability of screen objects. Return dict of instances 'gui_elements'.
    NOTE: Instances created have to be then added manually to dict 'gui_elements'!


    Class overview (imported as 'so'):
    TextField(screen, text, size, bg_color=False, text_color="default", multi_line=False, image_width=0, text_pos=(0,0):
        Basic text field.

    Button(screen, text, size, bg_color=False):
        Interactive button field.

    InteractiveText(screen, text, size, bg_color=False, panel=False, select=False):
        Interactive text field for info panel and/or option to toggle between selected/unselected states based on user
        input like mouse collision or mouse button event.

    InfoPanel(screen, text, size, bg_color=settings.info_panel_bg_color, text_color="default", multi_line=False, image_width=0,
        text_pos=(0,0), surface_pos="topright"):
        Info panel for use in conjunction with an instance of class 'InteractiveText()'.

    TextInputField(screen, input_field_instance, field_width):
        Text input field for use with 'pygame_textinput' library.
        NOTE: this class does not create the actual instance for a 'pygame_textinput' object, but instead streamlines the
        process of drawing it on screen with a white background field and having the input centered in said field.
    """

    # Size and spacing variables that are calculated based on screen size for scalability.
    screen_height, screen_width = screen.get_rect().height, screen.get_rect().width
    title_size = int(screen_height / 16)
    text_standard = int(screen_height / 30)
    text_large = int(screen_height / 20)
    text_medium = int(screen_height / 25)
    text_small = int(screen_height / 40)
    info_panel_width = int(screen_width / 4)
    title_screen_spacing = int(screen_height / 40)  # Spacing between main title and subtitle on title screen.
    menu_title_spacing = int(screen_height / 30)  # Default spacing between menu title and GUI objects.
    spacing_screen_edge = screen_width / 25  # Default value for distance to edge of screen for GUI objects.
    # Standard buttons, size and default positions.
    button_width = screen_width / 6
    continue_button = so.Button(screen, "Continue", text_medium)
    continue_button.button_rect.width = button_width
    continue_button.button_rect.bottomright = (screen.get_rect().right - spacing_screen_edge,
                                               screen.get_rect().bottom - spacing_screen_edge)
    inactive_continue_button = so.Button(screen, "Continue", text_medium)
    inactive_continue_button.button_rect.width = button_width
    inactive_continue_button.button_rect.bottomright = continue_button.button_rect.bottomright
    inactive_continue_button.rect_hover_color = (220, 150, 150)
    inactive_continue_button.rect_clicked_color = (200, 50, 50)
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
    reroll_button = so.Button(screen, "Roll Again", text_medium)
    # Initialize dictionaries from 'descr' package.
    ability_descr = abilities.get_ability_descr()
    race_descr = races.get_race_descr()
    class_descr = classes.get_class_descr()
    # Info panels.
    strength_info = so.InfoPanel(screen, ability_descr["str_descr"], text_small, multi_line=True, image_width=info_panel_width)
    dexterity_info = so.InfoPanel(screen, ability_descr["dex_descr"], text_small, multi_line=True, image_width=info_panel_width)
    constitution_info = so.InfoPanel(screen, ability_descr["con_descr"], text_small, multi_line=True, image_width=info_panel_width)
    intelligence_info = so.InfoPanel(screen, ability_descr["int_descr"], text_small, multi_line=True, image_width=info_panel_width)
    wisdom_info = so.InfoPanel(screen, ability_descr["wis_descr"], text_small, multi_line=True, image_width=info_panel_width)
    charisma_info = so.InfoPanel(screen, ability_descr["cha_descr"], text_small, multi_line=True, image_width=info_panel_width)
    # Ability text fields.
    strength_field = so.InteractiveText(screen, "Strength", text_medium, panel=[strength_info])
    dexterity_field = so.InteractiveText(screen, "Dexterity", text_medium, panel=[dexterity_info])
    constitution_field = so.InteractiveText(screen, "Constitution", text_medium, panel=[constitution_info])
    intelligence_field = so.InteractiveText(screen, "Intelligence", text_medium, panel=[intelligence_info])
    wisdom_field = so.InteractiveText(screen, "Wisdom", text_medium, panel=[wisdom_info])
    charisma_field = so.InteractiveText(screen, "Charisma", text_medium, panel=[charisma_info])


    # Race/class selection screen.
    race_class_selection_title_text = "- RACE / CLASS SELECTION -"
    race_class_selection_screen_title = so.TextField(screen, race_class_selection_title_text, text_large)
    reset_button = so.Button(screen, "RESET", text_medium)
    # Race info Panels.
    humans_info = so.InfoPanel(screen, race_descr["humans"][0], text_small, multi_line=True, image_width=info_panel_width)
    humans_info_table = so.InfoPanel(screen, race_descr["humans"][1], text_small, multi_line=True, image_width=info_panel_width,
                                     surface_pos="topleft")
    elves_info = so.InfoPanel(screen, race_descr["elves"][0], text_small, multi_line=True, image_width=info_panel_width)
    elves_info_table = so.InfoPanel(screen, race_descr["elves"][1], text_small, multi_line=True, image_width=info_panel_width,
                                    surface_pos="topleft")
    dwarves_info = so.InfoPanel(screen, race_descr["dwarves"][0], text_small, multi_line=True, image_width=info_panel_width)
    dwarves_info_table = so.InfoPanel(screen, race_descr["dwarves"][1], text_small, multi_line=True, image_width=info_panel_width,
                                      surface_pos="topleft")
    halflings_info= so.InfoPanel(screen, race_descr["halflings"][0], text_small, multi_line=True, image_width=info_panel_width)
    halflings_info_table = so.InfoPanel(screen, race_descr["halflings"][1], text_small, multi_line=True, image_width=info_panel_width,
                                        surface_pos="topleft")
    # Class info panels.
    fighter_info = so.InfoPanel(screen, class_descr["fighter"][0], text_small, multi_line=True, image_width=info_panel_width)
    fighter_info_table = so.InfoPanel(screen, class_descr["fighter"][1], text_small, multi_line=True, image_width=info_panel_width,
                                      surface_pos="topleft")
    cleric_info = so.InfoPanel(screen, class_descr["cleric"][0], text_small, multi_line=True, image_width=info_panel_width)
    cleric_info_table = so.InfoPanel(screen, class_descr["cleric"][1], text_small, multi_line=True, image_width=info_panel_width,
                                     surface_pos="topleft")
    magic_user_info = so.InfoPanel(screen, class_descr["magic-user"][0], text_small, multi_line=True, image_width=info_panel_width)
    magic_user_info_table = so.InfoPanel(screen, class_descr["magic-user"][1], text_small, multi_line=True, image_width=info_panel_width,
                                         surface_pos="topleft")
    thief_info = so.InfoPanel(screen, class_descr["thief"][0], text_small, multi_line=True, image_width=info_panel_width)
    thief_info_table = so.InfoPanel(screen, class_descr["thief"][1], text_small, multi_line=True, image_width=info_panel_width,
                                    surface_pos="topleft")
    fighter_magic_user_info = so.InfoPanel(screen, class_descr["fighter_magic-user"][0], text_small, multi_line=True,
                                           image_width=info_panel_width)
    fighter_magic_user_info_table = so.InfoPanel(screen, class_descr["fighter_magic-user"][1], text_small, multi_line=True,
                                                 image_width=info_panel_width, surface_pos="topleft")
    magic_user_thief_info = so.InfoPanel(screen, class_descr["magic-user_thief"][0], text_small, multi_line=True,
                                         image_width=info_panel_width)
    magic_user_thief_info_table = so.InfoPanel(screen, class_descr["magic-user_thief"][1], text_small, multi_line=True,
                                               image_width=info_panel_width, surface_pos="topleft")
    # Position for race and class info panels.
    humans_info.background_rect.center = screen.get_rect().center
    elves_info.background_rect.center = screen.get_rect().center
    dwarves_info.background_rect.center = screen.get_rect().center
    halflings_info.background_rect.center = screen.get_rect().center
    fighter_info.background_rect.center = screen.get_rect().center
    cleric_info.background_rect.center = screen.get_rect().center
    magic_user_info.background_rect.center = screen.get_rect().center
    thief_info.background_rect.center = screen.get_rect().center
    fighter_magic_user_info.background_rect.center = screen.get_rect().center
    magic_user_thief_info.background_rect.center = screen.get_rect().center
    # Race and class text fields.
    race_human_field = so.InteractiveText(screen, "Human", text_medium, panel=[humans_info, humans_info_table], select=True)
    race_elf_field = so.InteractiveText(screen, "Elf", text_medium, panel=[elves_info, elves_info_table], select=True)
    race_dwarf_field = so.InteractiveText(screen, "Dwarf", text_medium, panel=[dwarves_info, dwarves_info_table], select=True)
    race_halfling_field = so.InteractiveText(screen, "Halfling", text_medium, panel=[halflings_info, halflings_info_table], select=True)
    class_fighter_field = so.InteractiveText(screen, "Fighter", text_medium, panel=[fighter_info, fighter_info_table], select=True)
    class_cleric_field = so.InteractiveText(screen, "Cleric", text_medium, panel=[cleric_info, cleric_info_table], select=True)
    class_magic_user_field = so.InteractiveText(screen, "Magic-User", text_medium, panel=[magic_user_info, magic_user_info_table], select=True)
    class_thief_field = so.InteractiveText(screen, "Thief", text_medium, panel=[thief_info, thief_info_table], select=True)
    class_fighter_magic_user_field = so.InteractiveText(screen, "Fighter/Magic-User", text_medium,
                                                        panel=[fighter_magic_user_info, fighter_magic_user_info_table], select=True)
    class_magic_user_thief_field = so.InteractiveText(screen, "Magic-User/Thief", text_medium,
                                                      panel=[magic_user_thief_info, magic_user_thief_info_table], select=True)
    # Inactive race/class text fields.
    inactive_human_field = so.TextField(screen, "Human", text_medium, text_color="inactive")
    inactive_elf_field = so.TextField(screen, "Elf", text_medium, text_color="inactive")
    inactive_dwarf_field = so.TextField(screen, "Dwarf", text_medium, text_color="inactive")
    inactive_halfling_field = so.TextField(screen, "Halfling", text_medium, text_color="inactive")
    inactive_fighter_field = so.TextField(screen, "Fighter", text_medium, text_color="inactive")
    inactive_cleric_field = so.TextField(screen, "Cleric", text_medium, text_color="inactive")
    inactive_magic_user_field = so.TextField(screen, "Magic-User", text_medium, text_color="inactive")
    inactive_thief_field = so.TextField(screen, "Thief", text_medium, text_color="inactive")
    inactive_fighter_magic_user_field = so.TextField(screen, "Fighter/Magic-User", text_medium, text_color="inactive")
    inactive_magic_user_thief_field = so.TextField(screen, "Magic-User/Thief", text_medium, text_color="inactive")


    # Character naming screen.
    character_naming_title_text = "- NAME YOUR CHARACTER -"
    character_naming_screen_title = so.TextField(screen, character_naming_title_text, text_large)
    # 'pygame_textinput' and 'TextInputField' instances.
    character_input_font = pygame.font.SysFont(None, text_medium)
    character_name_input = pygame_textinput.TextInputVisualizer(font_object=character_input_font)
    character_name_field = so.TextInputField(screen, character_name_input, screen_width/2)


    # Starting money screen.
    starting_money_screen_title_text = "- STARTING MONEY -"
    starting_money_screen_title = so.TextField(screen, starting_money_screen_title_text, text_large)
    # Choice buttons.
    random_money_button_text = "Roll the dice for your starting money (3d6 x 10)"
    custom_money_button_text = "Choose your own amount of gold pieces"
    random_money_button = so.Button(screen, random_money_button_text, text_standard)
    custom_money_button = so.Button(screen, custom_money_button_text, text_standard)
    # Random money message field.
    random_money_message = "You receive"
    random_money_field = so.TextField(screen, random_money_message, text_standard)
    # 'pygame_textinput' and 'TextInputField' instances.
    money_input_prompt_message = "Enter amount of gold for your character"
    money_input_prompt = so.TextField(screen, money_input_prompt_message, text_standard)
    money_input_font = pygame.font.SysFont(None, text_medium)
    money_amount_input = pygame_textinput.TextInputVisualizer(font_object=money_input_font)
    money_amount_field = so.TextInputField(screen, money_amount_input, screen_width / 4)


    # Dict to be returned containing instances and size/spacing values (for positioning) for GUI objects.
    gui_elements = {
        # Default values for spacing.
        "title_screen_spacing": title_screen_spacing,
        "menu_title_spacing": menu_title_spacing,
        "default_button_width": button_width,
        "default_edge_spacing": spacing_screen_edge,
        # Standard buttons.
        "continue_button": continue_button,
        "inactive_continue_button": inactive_continue_button,
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
        "reset_button": reset_button,
        "possible_races": [race_human_field, race_elf_field, race_dwarf_field, race_halfling_field],
        "possible_classes": [class_fighter_field, class_cleric_field, class_magic_user_field, class_thief_field,
                              class_fighter_magic_user_field, class_magic_user_thief_field],
        "inactive_races": [inactive_human_field, inactive_elf_field, inactive_dwarf_field, inactive_halfling_field],
        "inactive_classes": [inactive_fighter_field, inactive_cleric_field, inactive_magic_user_field, inactive_thief_field,
                             inactive_fighter_magic_user_field, inactive_magic_user_thief_field],
        # Character naming screen.
        "naming_title": character_naming_screen_title,
        "character_name_input": [character_name_input, character_name_field],
        # Starting money screen.
        "starting_money_title": starting_money_screen_title,
        "starting_money_choices": [random_money_button, custom_money_button],
        "random_money": random_money_field,
        "money_amount_input": [money_amount_input, money_amount_field, money_input_prompt],
    }

    return gui_elements
