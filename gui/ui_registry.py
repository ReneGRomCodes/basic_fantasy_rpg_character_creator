import pygame.font
import gui.screen_objects as so
from core.settings import settings
from descr import abilities, races, classes, spells
import pygame_textinput
from gui.screen_objects import Button, TextField, ProgressBar, InfoPanel, InteractiveText, TextInputField

"""Initialize instances of classes from 'screen_objects.py' for use in GUI."""


def initialize_ui_registry(screen) -> dict:
    """Initialize instances of classes from 'screen_objects.py' for use in GUI in addition to default size and spacing
    values for automatic scalability of screen objects. Return dict of instances 'ui_registry'.
    NOTE: Instances created have to be then added manually to dict 'ui_registry'!
    Function is first called from function 'initialize_character_creator()' in 'main.py' with the returned dict being
    stored in instance 'ui_shared_data' of class 'UISharedData', from where it can be accessed when necessary.
    'initialize_ui_registry()' needs to be called again if changes to screen size (i.e. in settings screen) are made.


    Class overview (imported as 'so'):
    TextField(screen, text, size, bg_color=False, text_color="default", multi_line=False, surface_width=0, text_pos=(0,0):
        Basic text field.

    Button(screen, text, size, bg_color=False):
        Interactive button field.

    InteractiveText(screen, text, size, bg_color=False, panel=False, select=False):
        Interactive text field for info panel and/or option to toggle between selected/unselected states based on user
        input like mouse collision or mouse button event.

    InfoPanel(screen, text, size, bg_color=settings.info_panel_bg_color, text_color="default", multi_line=False, surface_width=0,
        text_pos=(0,0), pos=None, slide=True):
        Info panel for use in conjunction with an instance of class 'InteractiveText()'.
        NOTE: SEE CLASS DEFINITION IN 'gui/screen_objects.py' ON HOW TO IMPLEMENT INFO PANELS.

    TextInputField(screen, input_field_instance, field_width):
        Text input field for use with 'pygame_textinput' library.
        NOTE 1: this class does not create the actual instance for a 'pygame_textinput' object, but instead streamlines the
        process of drawing a 'pygame_textinput' instance on screen with a colored background and having the input centered
        in said field. Further modifications (size, position, etc.) can then be handled via this class.
        NOTE 2: For details on the required 'pygame_textinput' instance creation see its documentation.

    ProgressBar(screen, height, length, time=5)
        Visual-only loading progress bar.
        NOTE: This class creates a progress bar that 'simulates' loading without reflecting actual data processing or task
        completion. It is purely for visual effect to enhance the user experience.


    Art Asset/image implementation:
        Load and scale image files, creating Pygame Surface objects that are assigned to variables. These surfaces can
        then be positioned and blitted to the screen using the following method::
        image_surface = pygame.transform.scale(pygame.image.load(enter_your_image_here).convert(), (width, height))
        'enter_your_image_here' has to be added to and retrieved from 'Settings' instance 'settings'.
        Example:
        background_image = pygame.transform.scale(pygame.image.load(settings.bg_image).convert(), (screen_width, screen_height))


    ARGS:
        screen: PyGame window.
    RETURNS:
        gui_elements: dict containing screen objects and important size values.
    """

    # Size and spacing variables that are calculated based on screen size for scalability.
    screen_height: int = screen.get_rect().height
    screen_width: int = screen.get_rect().width
    title_size: int = int(screen_height / 24)
    text_standard: int = int(screen_height / 45)
    text_large: int = int(screen_height / 30)
    text_medium: int = int(screen_height / 37)
    text_small: int = int(screen_height / 70)
    info_panel_width: int = int(screen_width / 4)
    title_screen_spacing: int = int(screen_height / 60)  # Spacing between main title and subtitle on title screen.
    menu_title_spacing: int = int(screen_height / 45)  # Default spacing between menu title and GUI objects.
    default_edge_spacing: int = int(screen_width / 37)  # Default value for distance to between most GUI objects edges.
    button_spacing: int = int(screen_height / 200)  # Default spacing between buttons. Works best for 'grouped' buttons.
    button_width: int = int(screen_width / 6)  # Width for buttons like 'Continue', 'Back', etc. .
    # Default coordinates for buttons that are positioned at the screen's bottom corners.
    # Assign 'button_bottomright_pos' to button's rect '.bottomright' or 'button_bottomleft_pos' to '.bottomleft'
    # respectively for proper positioning.
    button_bottomright_pos: tuple[int, int] = (screen.get_rect().right - default_edge_spacing,
                                               screen.get_rect().bottom - default_edge_spacing)
    button_bottomleft_pos: tuple[int, int] = (screen.get_rect().left + default_edge_spacing,
                                              screen.get_rect().bottom - default_edge_spacing)

    # Off-Screen position for screen objects.
    # Assign 'off_screen_position' to screen object's rect '.bottomright' if object has to be positioned outside the
    # screen... for whatever reason.
    off_screen_position: tuple[int, int] = screen.get_rect().topleft

    # Standard buttons.
    continue_button: Button = so.Button(screen, "Continue", text_medium)
    inactive_continue_button = so.Button(screen, "Continue", text_medium, text_color="inactive")
    inactive_continue_button.rect_hover_color = settings.inactive_continue_button_hover_color
    inactive_continue_button.rect_clicked_color = settings.inactive_continue_button_click_color
    skip_button: Button = so.Button(screen, "Skip", text_medium)
    back_button: Button = so.Button(screen, "Back", text_medium)
    reset_button: Button = so.Button(screen, "CLEAR SELECTION", text_medium)
    # Tuple of 'Button' instances for resizing in for-loop below.
    button_fields: tuple[Button, ...] = (continue_button, inactive_continue_button, skip_button, back_button, reset_button)
    # Resize button rects.
    for button in button_fields:
        button.button_rect.width = button_width
    # Button positions.
    continue_button.button_rect.bottomright = button_bottomright_pos
    inactive_continue_button.button_rect.bottomright = button_bottomright_pos
    skip_button.button_rect.bottomright = button_bottomright_pos
    back_button.button_rect.bottomleft = button_bottomleft_pos

    # Art assets.
    background_image: pygame.transform.scale = pygame.transform.scale(pygame.image.load(settings.bg_image).convert(),
                                                                      (screen_width, screen_height))

    # Title screen.
    title: TextField = so.TextField(screen, "BASIC FANTASY ROLE-PLAYING GAME", title_size)
    subtitle: TextField = so.TextField(screen, "Character Creator", text_large)
    copyright_notice: TextField = so.TextField(screen, "Basic Fantasy Role-Playing Game, Copyright 2006-2025 Chris "
                                                       "Gonnerman. All Rights reserved. Distributed under CC BY-SA license. "
                                                       "www.basicfantasy.com", text_small)
    title_progress_bar: ProgressBar = so.ProgressBar(screen)
    continue_to_main_menu: TextField = so.TextField(screen, "Press any key to continue", text_medium)


    # Main Menu.
    main_menu_screen_title: TextField = so.TextField(screen, "- MAIN MENU -", title_size)
    start_button: Button = so.Button(screen, "Create a Character", text_medium)
    load_char: Button = so.Button(screen, "Load Character", text_medium)
    settings_button: Button = so.Button(screen, "Settings", text_medium)
    credits_button: Button = so.Button(screen, "Credits", text_medium)
    quit_button: Button = so.Button(screen, "Quit", text_medium)


    # Character menu.
    custom: Button = so.Button(screen, "Create Custom Character", text_medium)
    random: Button = so.Button(screen, "Create Random Character", text_medium)
    custom_random_button_width: int = int(screen.get_rect().width / 3)
    custom.button_rect.width, random.button_rect.width = custom_random_button_width, custom_random_button_width


    # Ability scores screen.
    # NOTE: Ability score fields have to be added to tuple 'abilities_array' in function 'show_ability_scores_screen'
    # from module 'gui/gui.py' in addition to the dict in this module. Otherwise, the fields won't show up on screen.
    # Screen layout is designed to adapt and fit up to 16 abilities.
    ability_scores_screen_title: TextField = so.TextField(screen, "- ABILITIES -", text_large)
    reroll_button: Button = so.Button(screen, "Roll Again", text_medium)
    reroll_button.button_rect.width = button_width
    # Initialize dictionaries from 'descr' package for info panels.
    ability_descr = abilities.get_ability_descr()
    race_descr = races.get_race_descr()
    class_descr = classes.get_class_descr()
    # Info panels.
    ability_01_info: InfoPanel = so.InfoPanel(screen, ability_descr["str_descr"], text_small, multi_line=True,
                                              surface_width=info_panel_width, pos="topright")
    ability_02_info: InfoPanel = so.InfoPanel(screen, ability_descr["dex_descr"], text_small, multi_line=True,
                                              surface_width=info_panel_width, pos="topright")
    ability_03_info: InfoPanel = so.InfoPanel(screen, ability_descr["con_descr"], text_small, multi_line=True,
                                              surface_width=info_panel_width, pos="topright")
    ability_04_info: InfoPanel = so.InfoPanel(screen, ability_descr["int_descr"], text_small, multi_line=True,
                                              surface_width=info_panel_width, pos="topright")
    ability_05_info: InfoPanel = so.InfoPanel(screen, ability_descr["wis_descr"], text_small, multi_line=True,
                                              surface_width=info_panel_width, pos="topright")
    ability_06_info: InfoPanel = so.InfoPanel(screen, ability_descr["cha_descr"], text_small, multi_line=True,
                                              surface_width=info_panel_width, pos="topright")
    # Ability text fields.
    ability_01_field: InteractiveText = so.InteractiveText(screen, "Strength", text_medium, panel=(ability_01_info, ))
    ability_02_field: InteractiveText = so.InteractiveText(screen, "Dexterity", text_medium, panel=(ability_02_info, ))
    ability_03_field: InteractiveText = so.InteractiveText(screen, "Constitution", text_medium, panel=(ability_03_info, ))
    ability_04_field: InteractiveText = so.InteractiveText(screen, "Intelligence", text_medium, panel=(ability_04_info, ))
    ability_05_field: InteractiveText = so.InteractiveText(screen, "Wisdom", text_medium, panel=(ability_05_info, ))
    ability_06_field: InteractiveText = so.InteractiveText(screen, "Charisma", text_medium, panel=(ability_06_info, ))


    # Race/class selection screen.
    # Screen layout is designed to adapt and fit up to 16 races/classes.
    race_class_selection_screen_title: TextField = so.TextField(screen, "- RACE / CLASS -", text_large)
    # Race info Panels.
    race_01_info: InfoPanel = so.InfoPanel(screen, race_descr["humans"][0], text_small, multi_line=True,
                                           surface_width=info_panel_width)
    race_01_info_table: InfoPanel = so.InfoPanel(screen, race_descr["humans"][1], text_small, multi_line=True,
                                                 surface_width=info_panel_width, pos="right")
    race_02_info: InfoPanel = so.InfoPanel(screen, race_descr["elves"][0], text_small, multi_line=True,
                                           surface_width=info_panel_width)
    race_02_info_table: InfoPanel = so.InfoPanel(screen, race_descr["elves"][1], text_small, multi_line=True,
                                                 surface_width=info_panel_width, pos="right")
    race_03_info: InfoPanel = so.InfoPanel(screen, race_descr["dwarves"][0], text_small, multi_line=True,
                                           surface_width=info_panel_width)
    race_03_info_table: InfoPanel = so.InfoPanel(screen, race_descr["dwarves"][1], text_small, multi_line=True,
                                                 surface_width=info_panel_width, pos="right")
    race_04_info: InfoPanel = so.InfoPanel(screen, race_descr["halflings"][0], text_small, multi_line=True,
                                           surface_width=info_panel_width)
    race_04_info_table: InfoPanel = so.InfoPanel(screen, race_descr["halflings"][1], text_small, multi_line=True,
                                                 surface_width=info_panel_width, pos="right")
    # Class info panels.
    class_01_info: InfoPanel = so.InfoPanel(screen, class_descr["fighter"][0], text_small, multi_line=True,
                                            surface_width=info_panel_width)
    class_01_info_table: InfoPanel = so.InfoPanel(screen, class_descr["fighter"][1], text_small, multi_line=True,
                                                  surface_width=info_panel_width, pos="left")
    class_02_info: InfoPanel = so.InfoPanel(screen, class_descr["cleric"][0], text_small, multi_line=True,
                                            surface_width=info_panel_width)
    class_02_info_table: InfoPanel = so.InfoPanel(screen, class_descr["cleric"][1], text_small, multi_line=True,
                                                  surface_width=info_panel_width, pos="left")
    class_03_info: InfoPanel = so.InfoPanel(screen, class_descr["magic-user"][0], text_small, multi_line=True,
                                            surface_width=info_panel_width)
    class_03_info_table: InfoPanel = so.InfoPanel(screen, class_descr["magic-user"][1], text_small, multi_line=True,
                                                  surface_width=info_panel_width, pos="left")
    class_04_info: InfoPanel = so.InfoPanel(screen, class_descr["thief"][0], text_small, multi_line=True,
                                            surface_width=info_panel_width)
    class_04_info_table: InfoPanel = so.InfoPanel(screen, class_descr["thief"][1], text_small, multi_line=True,
                                                  surface_width=info_panel_width, pos="left")
    class_05_info: InfoPanel = so.InfoPanel(screen, class_descr["fighter_magic-user"][0], text_small,
                                            multi_line=True, surface_width=info_panel_width)
    class_05_info_table: InfoPanel = so.InfoPanel(screen, class_descr["fighter_magic-user"][1], text_small,
                                                  multi_line=True, surface_width=info_panel_width, pos="left")
    class_06_info: InfoPanel = so.InfoPanel(screen, class_descr["magic-user_thief"][0], text_small,
                                            multi_line=True, surface_width=info_panel_width)
    class_06_info_table: InfoPanel = so.InfoPanel(screen, class_descr["magic-user_thief"][1], text_small,
                                                  multi_line=True, surface_width=info_panel_width, pos="left")
    # Active race/class text fields. Used when a race/class can be chosen in the race/class selection.
    race_01_field: InteractiveText = so.InteractiveText(screen, "Human", text_medium,
                                                        panel=(race_01_info, race_01_info_table), select=True)
    race_02_field: InteractiveText = so.InteractiveText(screen, "Elf", text_medium,
                                                        panel=(race_02_info, race_02_info_table), select=True)
    race_03_field: InteractiveText = so.InteractiveText(screen, "Dwarf", text_medium,
                                                        panel=(race_03_info, race_03_info_table), select=True)
    race_04_field: InteractiveText = so.InteractiveText(screen, "Halfling", text_medium,
                                                        panel=(race_04_info, race_04_info_table), select=True)
    class_01_field: InteractiveText = so.InteractiveText(screen, "Fighter", text_medium,
                                                         panel=(class_01_info, class_01_info_table), select=True)
    class_02_field: InteractiveText = so.InteractiveText(screen, "Cleric", text_medium,
                                                         panel=(class_02_info, class_02_info_table), select=True)
    class_03_field: InteractiveText = so.InteractiveText(screen, "Magic-User", text_medium,
                                                         panel=(class_03_info, class_03_info_table), select=True)
    class_04_field: InteractiveText = so.InteractiveText(screen, "Thief", text_medium,
                                                         panel=(class_04_info, class_04_info_table), select=True)
    class_05_field: InteractiveText = so.InteractiveText(screen, "Fighter/Magic-User", text_medium,
                                                         panel=(class_05_info, class_05_info_table), select=True)
    class_06_field: InteractiveText = so.InteractiveText(screen, "Magic-User/Thief", text_medium,
                                                         panel=(class_06_info, class_06_info_table), select=True)
    # Tuple of race and class fields for resizing in for-loop below.
    race_class_fields: tuple[InteractiveText, ...] = (race_01_field, race_02_field, race_03_field, race_04_field,
                                                      class_01_field, class_02_field, class_03_field, class_04_field,
                                                      class_05_field, class_06_field)
    # Resize race and class field rects.
    for race_class in race_class_fields:
        race_class.interactive_rect.width = int(screen_width / 5)
    # Inactive race/class text fields. Used when a race/class is unavailable in the race/class selection.
    # NOTE: every instance has to have the same 'text' attribute as their active counterpart.
    race_01_inactive_field: TextField = so.TextField(screen, "Human", text_medium, text_color="inactive")
    race_02_inactive_field: TextField = so.TextField(screen, "Elf", text_medium, text_color="inactive")
    race_03_inactive_field: TextField = so.TextField(screen, "Dwarf", text_medium, text_color="inactive")
    race_04_inactive_field: TextField = so.TextField(screen, "Halfling", text_medium, text_color="inactive")
    class_01_inactive_field: TextField = so.TextField(screen, "Fighter", text_medium, text_color="inactive")
    class_02_inactive_field: TextField = so.TextField(screen, "Cleric", text_medium, text_color="inactive")
    class_03_inactive_field: TextField = so.TextField(screen, "Magic-User", text_medium, text_color="inactive")
    class_04_inactive_field: TextField = so.TextField(screen, "Thief", text_medium, text_color="inactive")
    class_05_inactive_field: TextField = so.TextField(screen, "Fighter/Magic-User", text_medium, text_color="inactive")
    class_06_inactive_field: TextField = so.TextField(screen, "Magic-User/Thief", text_medium, text_color="inactive")


    # Spell selection screen.
    # Screen layout is designed to adapt and fit up to 16 spells.
    spell_selection_screen_title: TextField = so.TextField(screen, "- CHOOSE   A   FIRST   LEVEL   SPELL -", text_large)
    spell_selection_note_01_str: str = ("All Magic-Users begin knowing 'Read Magic'.\n"
                                           "Spells with an '*' are reversible after casting.")
    spell_selection_note_01: TextField = so.TextField(screen, spell_selection_note_01_str, text_standard,
                                                      bg_color=settings.info_panel_bg_color, multi_line=True,
                                                      surface_width=info_panel_width)
    # Initialize dictionary from 'descr' package for info panels.
    spell_descr = spells.get_spell_descr()
    # Spell info panels.
    spell_01_info: InfoPanel = so.InfoPanel(screen, spell_descr["read_magic"], text_small, multi_line=True,
                                                 surface_width=info_panel_width, pos="right")
    spell_02_info: InfoPanel = so.InfoPanel(screen, spell_descr["charm_person"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    spell_03_info: InfoPanel = so.InfoPanel(screen, spell_descr["detect_magic"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    spell_04_info: InfoPanel = so.InfoPanel(screen, spell_descr["floating_disc"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    spell_05_info: InfoPanel = so.InfoPanel(screen, spell_descr["hold_portal"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    spell_06_info: InfoPanel = so.InfoPanel(screen, spell_descr["light"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    spell_07_info: InfoPanel = so.InfoPanel(screen, spell_descr["magic_missile"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    spell_08_info: InfoPanel = so.InfoPanel(screen, spell_descr["magic_mouth"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    spell_09_info: InfoPanel = so.InfoPanel(screen, spell_descr["protection_from_evil"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    spell_10_info: InfoPanel = so.InfoPanel(screen, spell_descr["read_languages"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    spell_11_info: InfoPanel = so.InfoPanel(screen, spell_descr["shield"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    spell_12_info: InfoPanel = so.InfoPanel(screen, spell_descr["sleep"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    spell_13_info: InfoPanel = so.InfoPanel(screen, spell_descr["ventriloquism"], text_small, multi_line=True,
                                            surface_width=info_panel_width, pos="right")
    # Selectable spell fields.
    spell_01_field: InteractiveText = so.InteractiveText(screen, "Read Magic", text_medium, panel=(spell_01_info,), select=True)
    spell_02_field: InteractiveText = so.InteractiveText(screen, "Charm Person", text_medium, panel=(spell_02_info, ), select=True)
    spell_03_field: InteractiveText = so.InteractiveText(screen, "Detect Magic", text_medium, panel=(spell_03_info, ), select=True)
    spell_04_field: InteractiveText = so.InteractiveText(screen, "Floating Disc", text_medium, panel=(spell_04_info, ), select=True)
    spell_05_field: InteractiveText = so.InteractiveText(screen, "Hold Portal", text_medium, panel=(spell_05_info, ), select=True)
    spell_06_field: InteractiveText = so.InteractiveText(screen, "Light *", text_medium, panel=(spell_06_info, ), select=True)
    spell_07_field: InteractiveText = so.InteractiveText(screen, "Magic Missile", text_medium, panel=(spell_07_info, ), select=True)
    spell_08_field: InteractiveText = so.InteractiveText(screen, "Magic Mouth", text_medium, panel=(spell_08_info, ), select=True)
    spell_09_field: InteractiveText = so.InteractiveText(screen, "Protection from Evil *", text_medium, panel=(spell_09_info, ), select=True)
    spell_10_field: InteractiveText = so.InteractiveText(screen, "Read Languages", text_medium, panel=(spell_10_info, ), select=True)
    spell_11_field: InteractiveText = so.InteractiveText(screen, "Shield", text_medium, panel=(spell_11_info, ), select=True)
    spell_12_field: InteractiveText = so.InteractiveText(screen, "Sleep", text_medium, panel=(spell_12_info, ), select=True)
    spell_13_field: InteractiveText = so.InteractiveText(screen, "Ventriloquism", text_medium, panel=(spell_13_info, ), select=True)
    # Tuple of spell fields for resizing in for-loop below.
    spell_fields: tuple[InteractiveText, ...] = (spell_01_field, spell_02_field, spell_03_field, spell_04_field,
                                                 spell_05_field, spell_06_field, spell_07_field, spell_08_field,
                                                 spell_09_field, spell_10_field, spell_11_field, spell_12_field,
                                                 spell_13_field)
    # Resize spell field rects.
    for spell in spell_fields:
        spell.interactive_rect.width = int(screen_width / 4)


    # Language selection screen.
    # Screen layout is designed to adapt and fit up to 16 languages.
    language_selection_screen_title: TextField = so.TextField(screen, "- LANGUAGES -", text_large)
    language_selection_note_01_str: str = "All Characters begin knowing 'Common' and their race-specific language."
    language_selection_note_01: TextField = so.TextField(screen, language_selection_note_01_str, text_standard,
                                                         bg_color=settings.info_panel_bg_color, multi_line=True,
                                                         surface_width=info_panel_width)
    # Selectable language fields.
    language_01_field: InteractiveText = so.InteractiveText(screen, "Common", text_medium, select=True)
    language_02_field: InteractiveText = so.InteractiveText(screen, "Elvish", text_medium, select=True)
    language_03_field: InteractiveText = so.InteractiveText(screen, "Dwarvish", text_medium, select=True)
    language_04_field: InteractiveText = so.InteractiveText(screen, "Halfling", text_medium, select=True)
    # Tuple of language fields for resizing in for-loop below.
    lang_fields: tuple[InteractiveText, ...] = (language_01_field, language_02_field, language_03_field, language_04_field)
    # Resizing language field rects.
    for lang in lang_fields:
        lang.interactive_rect.width = int(screen_width / 4)
    # Inactive language text fields. Used when maximum of additional languages has been reached in language selection.
    # NOTE: every instance has to have the same 'text' attribute as their active counterpart.
    language_01_field_inactive: TextField = so.TextField(screen, "Common", text_medium, text_color="inactive")
    language_02_field_inactive: TextField = so.TextField(screen, "Elvish", text_medium, text_color="inactive")
    language_03_field_inactive: TextField = so.TextField(screen, "Dwarvish", text_medium, text_color="inactive")
    language_04_field_inactive: TextField = so.TextField(screen, "Halfling", text_medium, text_color="inactive")


    # Character naming screen.
    # NOTE: 'character_naming_prompt' has an empty string as text attribute. The final text will be assigned in function
    # 'ui_helpers.py/build_and_position_prompt()' for the naming screen to include character race/class. This allows the
    # function to reset the prompt and prevents it from retaining previous race/class selections if user goes back and
    # forth between selection and naming screen. Shit gets out of hand otherwise.
    character_naming_prompt: TextField = so.TextField(screen, "", text_large)
    # 'pygame_textinput' and 'TextInputField' instances.
    character_input_font: pygame.font.Font = pygame.font.Font(settings.font, text_medium)
    character_name_input: pygame_textinput.TextInputVisualizer = pygame_textinput.TextInputVisualizer(font_object=character_input_font)
    character_name_field: TextInputField = so.TextInputField(screen, character_name_input, int(screen_width/2))


    # Starting money screen.
    starting_money_screen_title: TextField = so.TextField(screen, "- STARTING MONEY -", text_large)
    # Choice buttons.
    random_money_button: Button = so.Button(screen, "Roll the dice for your starting money (3d6 x 10)", text_standard)
    custom_money_button: Button = so.Button(screen, "Choose your own amount of gold pieces", text_standard)
    money_button_width: int = int(screen.get_rect().width / 2.5)
    random_money_button.button_rect.width, custom_money_button.button_rect.width = money_button_width, money_button_width
    # Random money message field.
    rolling_dice_money_field: TextField = so.TextField(screen, "Rolling the dice!", text_large)
    random_money_field: TextField = so.TextField(screen, "You receive", text_medium)
    # 'pygame_textinput' and 'TextInputField' instances.
    money_input_prompt: TextField = so.TextField(screen, "Enter amount of gold for your character", text_medium)
    money_input_font: pygame.font.Font = pygame.font.Font(settings.font, text_medium)
    money_amount_input: pygame_textinput.TextInputVisualizer = pygame_textinput.TextInputVisualizer(font_object=money_input_font)
    money_amount_field: TextInputField = so.TextInputField(screen, money_amount_input, int(screen_width / 4))


    # Character creation complete screen.
    completion_message_field: TextField = so.TextField(screen, "CHARACTER CREATION COMPLETE", text_large)
    show_character_sheet_button: Button = so.Button(screen, "Show Character Sheet", text_medium)


    # Dict to be returned containing instances and size/spacing values (for positioning) for GUI objects.
    ui_registry = {
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
        "default_edge_spacing": default_edge_spacing,
        "button_spacing": button_spacing,
        # Standard buttons.
        "continue_button": continue_button,
        "inactive_continue_button": inactive_continue_button,
        "skip_button": skip_button,
        "back_button": back_button,
        "reset_button": reset_button,
        # Standard button positions.
        "bottom_right_pos": button_bottomright_pos,
        "bottom_left_pos": button_bottomleft_pos,
        # Off-Screen position for special uses.
        "off_screen_pos": off_screen_position,
        # Art assets.
        "background_image": background_image,

        # Title screen.
        "title_screen_fields": (title, subtitle, copyright_notice, title_progress_bar, continue_to_main_menu),

        # Main menu.
        "main_menu_title": main_menu_screen_title,
        "start_button": start_button,
        "menu_buttons": (load_char, settings_button, credits_button, quit_button),

        # Character menu.
        "custom": custom,
        "random": random,
        # Ability scores screen.
        "abilities_title": ability_scores_screen_title,
        "ability_fields": (ability_01_field, ability_02_field, ability_03_field, ability_04_field, ability_05_field,
                           ability_06_field),
        "reroll_button": reroll_button,
        # Race/class selection screen.
        "race_class_title": race_class_selection_screen_title,
        "active_races": (race_01_field, race_02_field, race_03_field, race_04_field),
        "active_classes": (class_01_field, class_02_field, class_03_field, class_04_field, class_05_field, class_06_field),
        "inactive_races": (race_01_inactive_field, race_02_inactive_field, race_03_inactive_field, race_04_inactive_field),
        "inactive_classes": (class_01_inactive_field, class_02_inactive_field, class_03_inactive_field, class_04_inactive_field,
                             class_05_inactive_field, class_06_inactive_field),
        # Spell selection screen.
        "spell_title": spell_selection_screen_title,
        "spell_note": spell_selection_note_01,
        "spell_fields": (spell_01_field, spell_02_field, spell_03_field, spell_04_field, spell_05_field, spell_06_field,
                         spell_07_field, spell_08_field, spell_09_field, spell_10_field, spell_11_field, spell_12_field,
                         spell_13_field),
        # Language selection screen.
        "lang_title": language_selection_screen_title,
        "lang_note": language_selection_note_01,
        "lang_fields": (language_01_field, language_02_field, language_03_field, language_04_field),
        "inactive_language_fields": (language_01_field_inactive, language_02_field_inactive, language_03_field_inactive,
                                     language_04_field_inactive),
        # Character naming screen.
        "naming_prompt": character_naming_prompt,
        "character_name_input": (character_name_input, character_name_field),
        # Starting money screen.
        "starting_money_title": starting_money_screen_title,
        "starting_money_choices": (random_money_button, custom_money_button),
        "random_money": (rolling_dice_money_field, random_money_field),
        "money_amount_input": (money_amount_input, money_amount_field, money_input_prompt),
        # Character completion screen.
        "completion_message": completion_message_field,
        "show_character_sheet": show_character_sheet_button,
    }

    return ui_registry
