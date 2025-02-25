import pygame.font
import gui.screen_objects as so
from descr import abilities, races, classes
import pygame_textinput
"""Initialize instances of classes from 'screen_objects.py' for use in GUI."""


def initialize_screen_elements(screen, settings):
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
    title_size = int(screen_height / 24)
    text_standard = int(screen_height / 45)
    text_large = int(screen_height / 30)
    text_medium = int(screen_height / 37)
    text_small = int(screen_height / 70)
    info_panel_width = int(screen_width / 4)
    title_screen_spacing = int(screen_height / 60)  # Spacing between main title and subtitle on title screen.
    menu_title_spacing = int(screen_height / 45)  # Default spacing between menu title and GUI objects.
    spacing_screen_edge = screen_width / 37  # Default value for distance to edge of screen for GUI objects.
    # Standard buttons, size.
    button_width = screen_width / 6
    continue_button = so.Button(screen, "Continue", text_medium)
    continue_button.button_rect.width = button_width
    continue_button.button_rect.bottomright = (screen.get_rect().right - spacing_screen_edge,
                                               screen.get_rect().bottom - spacing_screen_edge)
    inactive_continue_button = so.Button(screen, "Continue", text_medium)
    inactive_continue_button.button_rect.width = button_width
    inactive_continue_button.button_rect.bottomright = continue_button.button_rect.bottomright
    inactive_continue_button.rect_hover_color = settings.inactive_continue_button_hover_color
    inactive_continue_button.rect_clicked_color = settings.inactive_continue_button_click_color
    back_button = so.Button(screen, "Back", text_medium)
    back_button.button_rect.width = button_width
    back_button.button_rect.bottomleft = (screen.get_rect().left + spacing_screen_edge,
                                          screen.get_rect().bottom - spacing_screen_edge)


    # Title screen.
    title = so.TextField(screen, "BASIC FANTASY ROLE-PLAYING GAME", title_size)
    subtitle = so.TextField(screen, "Character Creator", text_large)
    copyright_notice = so.TextField(screen, "Basic Fantasy Role-Playing Game, Copyright 2006-2025 Chris Gonnerman. All"
                                            "Rights reserved. Distributed under CC BY-SA license. www.basicfantasy.com",
                                    text_small)


    # Main Menu.
    main_menu_screen_title = so.TextField(screen, "- MAIN MENU -", title_size)
    start_button = so.Button(screen, "Create a Character", text_medium)
    settings_button = so.Button(screen, "Settings", text_medium)
    credits_button = so.Button(screen, "Credits", text_medium)
    quit_button = so.Button(screen, "Quit", text_medium)


    # Settings.
    settings_title = so.TextField(screen, "- SETTINGS -", title_size)
    window_size_field = so.TextField(screen, "Window Size", text_large)
    window_size_button_small = so.InteractiveText(screen, "1280x720", text_medium, select=True)
    window_size_button_medium = so.InteractiveText(screen, "1600x900", text_medium, select=True)
    window_size_button_large = so.InteractiveText(screen, "1920x1080", text_medium, select=True)
    window_size_button_full = so.InteractiveText(screen, "Full Screen", text_medium, select=True)


    # Credits.
    # 'gui_elements["credits"]' is an array of tuples. Each inner tuple representing a credit category, with the element
    # at index [0] being the category title and the following elements being the credited names.
    credits_title = so.TextField(screen, "- CREDITS -", title_size)
    programmer_title = so.TextField(screen, "Programming & UI Design", text_large)
    programmer_name = so.TextField(screen, "René Grewe Romero", text_medium)
    concept_creator_title = so.TextField(screen, "Based on 'Basic Tabletop RPG'", text_large)
    concept_creator_name = so.TextField(screen, "by Chris Gonnerman", text_medium)
    font_creator_title = so.TextField(screen, "Font 'Eagle Lake'", text_large)
    font_creator_name = so.TextField(screen, "by Brian J. Bonislawsky", text_medium)


    # Character menu.
    custom = so.Button(screen, "Create Custom Character", text_medium)
    random = so.Button(screen, "Create Random Character", text_medium)


    # Ability scores screen.
    ability_scores_screen_title = so.TextField(screen, "- ABILITIES -", text_large)
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
    race_class_selection_screen_title = so.TextField(screen, "- RACE / CLASS SELECTION -", text_large)
    reset_button = so.Button(screen, "RESET", text_medium)
    # Race info Panels.
    humans_info = so.InfoPanel(screen, race_descr["humans"][0], text_small, multi_line=True, image_width=info_panel_width,
                               surface_pos="center")
    humans_info_table = so.InfoPanel(screen, race_descr["humans"][1], text_small, multi_line=True, image_width=info_panel_width,
                                     surface_pos="topleft")
    elves_info = so.InfoPanel(screen, race_descr["elves"][0], text_small, multi_line=True, image_width=info_panel_width,
                               surface_pos="center")
    elves_info_table = so.InfoPanel(screen, race_descr["elves"][1], text_small, multi_line=True, image_width=info_panel_width,
                                    surface_pos="topleft")
    dwarves_info = so.InfoPanel(screen, race_descr["dwarves"][0], text_small, multi_line=True, image_width=info_panel_width,
                               surface_pos="center")
    dwarves_info_table = so.InfoPanel(screen, race_descr["dwarves"][1], text_small, multi_line=True, image_width=info_panel_width,
                                      surface_pos="topleft")
    halflings_info= so.InfoPanel(screen, race_descr["halflings"][0], text_small, multi_line=True, image_width=info_panel_width,
                               surface_pos="center")
    halflings_info_table = so.InfoPanel(screen, race_descr["halflings"][1], text_small, multi_line=True, image_width=info_panel_width,
                                        surface_pos="topleft")
    # Class info panels.
    fighter_info = so.InfoPanel(screen, class_descr["fighter"][0], text_small, multi_line=True, image_width=info_panel_width,
                               surface_pos="center")
    fighter_info_table = so.InfoPanel(screen, class_descr["fighter"][1], text_small, multi_line=True, image_width=info_panel_width,
                                      surface_pos="topleft")
    cleric_info = so.InfoPanel(screen, class_descr["cleric"][0], text_small, multi_line=True, image_width=info_panel_width,
                               surface_pos="center")
    cleric_info_table = so.InfoPanel(screen, class_descr["cleric"][1], text_small, multi_line=True, image_width=info_panel_width,
                                     surface_pos="topleft")
    magic_user_info = so.InfoPanel(screen, class_descr["magic-user"][0], text_small, multi_line=True, image_width=info_panel_width,
                               surface_pos="center")
    magic_user_info_table = so.InfoPanel(screen, class_descr["magic-user"][1], text_small, multi_line=True, image_width=info_panel_width,
                                         surface_pos="topleft")
    thief_info = so.InfoPanel(screen, class_descr["thief"][0], text_small, multi_line=True, image_width=info_panel_width,
                               surface_pos="center")
    thief_info_table = so.InfoPanel(screen, class_descr["thief"][1], text_small, multi_line=True, image_width=info_panel_width,
                                    surface_pos="topleft")
    fighter_magic_user_info = so.InfoPanel(screen, class_descr["fighter_magic-user"][0], text_small, multi_line=True,
                                           image_width=info_panel_width, surface_pos="center")
    fighter_magic_user_info_table = so.InfoPanel(screen, class_descr["fighter_magic-user"][1], text_small, multi_line=True,
                                                 image_width=info_panel_width, surface_pos="topleft")
    magic_user_thief_info = so.InfoPanel(screen, class_descr["magic-user_thief"][0], text_small, multi_line=True,
                                         image_width=info_panel_width, surface_pos="center")
    magic_user_thief_info_table = so.InfoPanel(screen, class_descr["magic-user_thief"][1], text_small, multi_line=True,
                                               image_width=info_panel_width, surface_pos="topleft")
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
    # NOTE: 'character_naming_prompt' has an empty string as text attribute. The final text will be assigned in function
    # 'ui_helpers.py/build_and_position_prompt()' for the naming screen to include character race/class. This allows the
    # function to reset the prompt and prevents it from retaining previous race/class selections if user goes back and
    # forth between selection and naming screen. Shit gets out of hand otherwise.
    character_naming_prompt = so.TextField(screen, "", text_medium)
    # 'pygame_textinput' and 'TextInputField' instances.
    character_input_font = pygame.font.Font(settings.font, text_medium)
    character_name_input = pygame_textinput.TextInputVisualizer(font_object=character_input_font)
    character_name_field = so.TextInputField(screen, character_name_input, screen_width/2)


    # Starting money screen.
    starting_money_screen_title = so.TextField(screen, "- STARTING MONEY -", text_large)
    # Choice buttons.
    random_money_button = so.Button(screen, "Roll the dice for your starting money (3d6 x 10)", text_standard)
    custom_money_button = so.Button(screen, "Choose your own amount of gold pieces", text_standard)
    # Random money message field.
    random_money_field = so.TextField(screen, "You receive", text_medium)
    # 'pygame_textinput' and 'TextInputField' instances.
    money_input_prompt = so.TextField(screen, "Enter amount of gold for your character", text_standard)
    money_input_font = pygame.font.Font(settings.font, text_medium)
    money_amount_input = pygame_textinput.TextInputVisualizer(font_object=money_input_font)
    money_amount_field = so.TextInputField(screen, money_amount_input, screen_width / 4)


    # Character creation complete screen.
    completion_message_field = so.TextField(screen, "CHARACTER CREATION COMPLETE", text_large)
    show_character_sheet_button = so.Button(screen, "Show Character Sheet", text_medium)


    # Dict to be returned containing instances and size/spacing values (for positioning) for GUI objects.
    gui_elements = {
        # Default values for text sizes.
        "title_size": title_size,
        "text_standard": text_standard,
        "text_large": text_large,
        "text_medium": text_medium,
        "text_small": text_small,
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
        "start_button": start_button,
        "menu_buttons": (settings_button, credits_button, quit_button),

        # Settings.
        "settings_title": settings_title,
        "window_size": window_size_field,
        "window_size_buttons": (window_size_button_small, window_size_button_medium, window_size_button_large,
                                window_size_button_full),
        # Credits.
        "credits_title": credits_title,
        "credits": ((programmer_title, programmer_name),
                    (concept_creator_title, concept_creator_name),
                    (font_creator_title, font_creator_name)),
        # Character menu.
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
        "possible_races": (race_human_field, race_elf_field, race_dwarf_field, race_halfling_field),
        "possible_classes": (class_fighter_field, class_cleric_field, class_magic_user_field, class_thief_field,
                              class_fighter_magic_user_field, class_magic_user_thief_field),
        "inactive_races": (inactive_human_field, inactive_elf_field, inactive_dwarf_field, inactive_halfling_field),
        "inactive_classes": (inactive_fighter_field, inactive_cleric_field, inactive_magic_user_field, inactive_thief_field,
                             inactive_fighter_magic_user_field, inactive_magic_user_thief_field),
        # Character naming screen.
        "naming_prompt": character_naming_prompt,
        "character_name_input": (character_name_input, character_name_field),
        # Starting money screen.
        "starting_money_title": starting_money_screen_title,
        "starting_money_choices": (random_money_button, custom_money_button),
        "random_money": random_money_field,
        "money_amount_input": (money_amount_input, money_amount_field, money_input_prompt),
        # Character completion screen.
        "completion_message": completion_message_field,
        "show_character_sheet": show_character_sheet_button,
    }

    return gui_elements
