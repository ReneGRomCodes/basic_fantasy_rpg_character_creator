"""
Background functions for GUI, i.e. value build/retrieval and object positioning functions for pygame screens.
"""
import time

import pygame

from core.rules import roll_starting_money
from core.shared_data import shared_data as sd

from .screen_objects import TextField, Button, InteractiveText, TextInputField
from .shared_data import ui_shared_data as uisd


"""General functions."""

def draw_screen_title(screen, screen_title: TextField, title_background=True) -> None:
    """Draw 'screen_title' object on screen at default position.
    ARGS:
        screen: PyGame window.
        screen_title: instance of class 'TextField()' representing the screen title.
        title_background: bool to trigger default background image for title text. Default is 'True'.
    """
    screen_title.text_rect.top = screen.get_rect().top + uisd.ui_registry["default_edge_spacing"]
    screen_title.text_rect.centerx = screen.get_rect().centerx

    if title_background:
        draw_element_background_image(screen, screen_title, "ornate_wood")

    screen_title.draw_text()


def draw_special_button(screen, button: Button, mouse_pos, button_background=True) -> None:
    """Draw special use button (i.e. 'Roll Again' or 'Reset') at the bottom center of the screen.
    ARGS:
        screen: PyGame window.
        button: instance of class 'Button()' representing the special use button.
        mouse_pos: position of mouse on screen.
        button_background: bool to trigger default background image for button. Default is 'True'.
    """
    button.button_rect.centerx = screen.get_rect().centerx
    button.button_rect.bottom = screen.get_rect().bottom - uisd.ui_registry["default_edge_spacing"]

    if button_background:
        draw_element_background_image(screen, button, "wood")

    button.draw_button(mouse_pos)


def draw_conditional_continue_button(screen, mouse_pos, condition_1: object | bool = False, condition_2: object | bool = False,
                                     check_mode: str = "any", alt_button: str = "inactive", button_background=True) -> None:
    """Draw either active or inactive instance of continue button or skip button from module 'ui_registry' based on
    conditional parameters.
    NOTE: 'skip' button rect does not need a dedicated '.collidepoint' detection in event handler as it's position is
    identical to the standard 'continue' button rect. Just use that one for event detection and Bob's your uncle.
    ARGS:
        screen: PyGame window.
        mouse_pos: mouse position on screen.
        condition_1: first condition to be checked. Default is "False".
        condition_2: second condition to be checked. Default is "False".
        check_mode: String to determine whether one or both conditions must be met. Use "any" to require at least one condition,
                    or "all" to require both. Default is "any".
        alt_button: String to determine which conditional button alternative should be displayed. "inactive" for an
                    inactive continue button, "skip" for a skip button. Default is "inactive".
        button_background: bool to trigger default background image for button. Default is 'True'.
    """
    continue_button, inactive_continue_button, skip_button = (uisd.ui_registry["continue_button"],
                                                              uisd.ui_registry["inactive_continue_button"],
                                                              uisd.ui_registry["skip_button"])

    if check_mode == "any" and (condition_1 or condition_2):
        button = continue_button
    elif check_mode == "all" and (condition_1 and condition_2):
        button = continue_button
    else:
        if alt_button == "inactive":
            button = inactive_continue_button
        elif alt_button == "skip":
            button = skip_button

    if button_background:
        draw_element_background_image(screen, button, "wood")

    button.draw_button(mouse_pos)


def draw_screen_note(screen, note: TextField, note_background=True) -> None:
    """Position and draw screen-specific notes on default position (centered at left edge) on screen.
    ARGS:
        screen: PyGame window.
        note: 'TextField' instance for screen-specific notes.
        note_background: bool to trigger default background image for screen note. Default is 'True'.
    """
    note.text_rect.left = screen.get_rect().left + uisd.ui_registry["default_edge_spacing"]
    note.text_rect.centery = screen.get_rect().centery

    if note_background:
        draw_element_background_image(screen, note, "parchment")

    note.draw_text()


def show_info_panels(elements: list | tuple, mouse_pos) -> None:
    """Iterate over a collection of GUI elements and call their method to handle mouse interactions regarding info panels
    and display panels if applicable.
    See class definition for 'InteractiveText' and 'InfoPanel' for details.
    ARGS:
        elements: List/tuple or single instance of GUI elements.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    NOTE: This function must be called at the end of relevant screen functions to ensure info panels are drawn on top of
    other screen elements."""
    # Check if 'elements' is list/tuple or single instance and ensure that mouse interaction is only handled if element
    # is an instance of class 'InteractiveText'. Prevents errors in cases where 'elements' might contain instances of
    # other classes.
    if isinstance(elements, (list, tuple)):
        for element in elements:
            if isinstance(element, InteractiveText):
                element.handle_mouse_interaction_info_panels(mouse_pos)
    if isinstance(elements, InteractiveText):
            elements.handle_mouse_interaction_info_panels(mouse_pos)


def draw_element_background_image(screen, element: TextField | Button, background_type: str, parchment: int = 0,
                                  button_border: bool = False) -> None:
    """Resize, position and draw background image for single UI elements (use 'draw_elements_array_background_image()'
    for grouped elements).
    ARGS:
        screen: PyGame Window.
        element: Instance of class 'TextField' or 'Button' that receives the background.
        background_type: keyword string representing type of background:
            "wood"
            "ornate_wood"
            "parchment"
        parchment: index for version of parchment from list in 'ui_registry["parchment_images"]'. Default is '0'
        button_border: bool to set if default border around element is to be displayed when 'element' is instance of class
            'Button'. 'False'/deactivated by default.

    NOTE A: This function handles the background for Button instances in a way that it accommodates the "wood" background
        only. Other backgrounds will work, but might not be scaled properly. Just add additional multiplier variables
        and/or expand the 'background_type' check block if necessary.

    NOTE B: This function doesn't need to be called for elements like standard screen titles, special buttons (i.e.
        'Roll Again' or 'Reset'), conditional continue buttons or standard screen notes, which are drawn by calling their
        specialized functions 'draw_screen_title()', 'draw_special_button()', 'draw_conditional_continue_button()' and
        'draw_screen_note()' respectively, and use arguments to activate/deactivate their background image. See function
        docstrings for details.
        Info panels which are drawn by calling 'show_info_panels()' have their background image handled via class methods.
        See class 'InfoPanel' in 'gui/screen_objects.py' for details.
    """
    # Size multipliers to account for transparent background in image files.
    wood_width_mult: float = 1.7
    wood_height_mult: float = 2.0
    wood_width_button_mult: float = 1.25
    wood_height_button_mult: float = 1.6
    parchment_width_mult: float = 1.5
    parchment_height_mult: float = 2.0

    image = None
    width_mult = None
    height_mult = None
    element_center = None
    element_width = None
    element_height = None

    # Set multiplier and image variables based on 'background_type' and element class.
    if background_type == "wood":
        image = uisd.ui_registry["wood_image"]
        if isinstance(element, Button):
            width_mult = wood_width_button_mult
            height_mult = wood_height_button_mult
        else:
            width_mult = wood_width_mult
            height_mult = wood_height_mult

    elif background_type == "ornate_wood":
        image = uisd.ui_registry["wood_ornate_image"]
        width_mult = wood_width_mult
        height_mult = wood_height_mult

    elif background_type == "parchment":
        image = uisd.ui_registry["parchment_images"][parchment]
        width_mult = parchment_width_mult
        height_mult = parchment_height_mult

    # Assign values to variables based on element class.
    if isinstance(element, Button):
        element_center = element.button_rect.center
        element_width = element.button_rect.width
        element_height = element.button_rect.height
        if not button_border:
            # 'Remove' button border by setting its width to -1.
            element.border_width = -1

    elif isinstance(element, TextField):
        element_center = element.text_rect.center
        element_width = element.text_rect.width
        element_height = element.text_rect.height

    image_width = element_width * width_mult
    image_height = element_height * height_mult
    image_loaded = pygame.transform.scale(image, (image_width, image_height))
    image_rect = image_loaded.get_rect(center=element_center)

    screen.blit(image_loaded, image_rect)


def draw_elements_array_background_image(screen, elements_array, parchment=0) -> None:  # TODO general background image function.
    # Helper variables for better readability.
    screen_rect = screen.get_rect()
    ref_element = elements_array[0]
    n_elements: int = len(elements_array)
    elements_arr_mid_index: int = n_elements // 2
    # Size multipliers to account for transparent background in image files.
    image_width_mult: float = 1.5
    image_height_mult: float = 1.4

    ref_element_rect = None
    elements_arr_mid_rect = None
    elements_arr_mid_prev_rect = None
    elements_arr_last_rect = None

    # Set values to use correct rect attributes based on element types in 'elements_arrays'.
    if isinstance(ref_element, InteractiveText):
        ref_element_rect = elements_array[0].interactive_rect
        elements_arr_mid_rect = elements_array[elements_arr_mid_index].interactive_rect
        elements_arr_mid_prev_rect = elements_array[elements_arr_mid_index-1].interactive_rect
        elements_arr_last_rect = elements_array[-1].interactive_rect

    elif isinstance(ref_element, TextField):
        ref_element_rect = elements_array[0].text_rect
        elements_arr_mid_rect = elements_array[elements_arr_mid_index].text_rect
        elements_arr_mid_prev_rect = elements_array[elements_arr_mid_index - 1].text_rect
        elements_arr_last_rect = elements_array[-1].text_rect

    image_width = ref_element_rect.width * image_width_mult
    image_height = (elements_arr_last_rect.bottom - ref_element_rect.top) * image_height_mult
    image = uisd.ui_registry["parchment_images"][parchment]
    image_loaded = pygame.transform.scale(image, (image_width, image_height))
    image_rect = image_loaded.get_rect(centerx=ref_element_rect.centerx)
    # Set image y-position based on number of abilities in 'abilities_array' to assure background is properly centered.
    if n_elements % 2 == 0:
        image_center_y_offset = (elements_arr_mid_rect.top - elements_arr_mid_prev_rect.bottom) / 2
        image_rect.centery = elements_arr_mid_rect.top - image_center_y_offset
    else:
        image_rect.centery = elements_arr_mid_rect.centery

    screen.blit(image_loaded, image_rect)


"""Function for dynamic positioning."""

def set_elements_pos_y_values(screen, elements: list | tuple) -> tuple[int, int]:
    """Dynamically set starting y-position for GUI elements on screen based on number of said elements.
    Screen layout is designed to adapt and fit up to 16 elements.
    NOTE: It is advised to make use of function 'get_pos_dict()' when handling screens which make use of selectable
    instances of 'InteractiveText' and non-selectable counterparts. See function docstring for details, and it's
    implementation in language selection (simple) or race/class selection (complex) as an example.
    ARGS:
        screen: PyGame window.
        elements: List/tuple or array to store GUI elements.
    RETURNS:
        elements_pos_y: Y-position for first GUI element on screen.
        pos_y_offset: Offset value to position following elements.
    """
    # Reference variables for positioning.
    screen_center_y = screen.get_rect().centery
    n_elements: int = len(elements)
    # Check 'elements' for type and assign first element to variable as reference object for further positioning.
    ref_element = elements[0][0] if isinstance(elements[0], (list, tuple)) else elements[0]

    # Position 'ref_element' at the y-center axis for final 'element_pos_y' calculation further down.
    if n_elements % 2 == 0:
        ref_element.text_rect.top = screen_center_y
    else:
        ref_element.text_rect.centery = screen_center_y

    # Calculate offset multiplier for use in 'pos_y_offset' based on number of items in 'elements'.
    if n_elements <= 8:
        offset_multiplier: int | float = 2
    elif n_elements <= 11:
        offset_multiplier: int | float = 1.5
    else:
        offset_multiplier: int | float = 1

    # Set initial position on y-axis for elements and offset value for spacing between each element.
    pos_y_offset = ref_element.text_rect.height * offset_multiplier
    element_pos_y = ref_element.text_rect.top - (int(n_elements / 2) * pos_y_offset)

    return element_pos_y, pos_y_offset


def get_pos_y_dict(screen, active_fields: tuple[InteractiveText, ...], pos_dict: dict[str, int]) -> None:
    """Populate dict for selectable elements 'dict' with y-positions in 'ui_shared_data' for screens which use both,
    available/selectable fields and their inactive/non-selectable counterparts.
    Dict keys are the fields names. The dict can then be used for the positioning of both, active (InteractiveText)
    elements and their inactive (TextField) counterparts, if both are meant to have the same position.
    ARGS:
        screen: pygame window.
        active_fields: tuple containing instances of class 'InteractiveText' representing available fields.
        pos_dict: dict stored as attribute in 'ui_shared_data', containing y-positions for each available field.
    """
    # Get dynamic y-positions for items in 'active_fields'.
    pos_y_start, pos_y_offset = set_elements_pos_y_values(screen, active_fields)

    # Build dict with y-position values for each active field with 'field.text' attribute as keys.
    for index, field in enumerate(active_fields):
        if index == 0:
            pos_dict[field.text] = pos_y_start
        else:
            pos_dict[field.text] = pos_y_start + pos_y_offset * index


"""Background functions for title screen."""

def position_title_screen_elements(screen) -> None:
    """Position objects from 'ui_registry' for title screen.
    ARGS:
        screen: PyGame window.
    """
    screen_rect: pygame.Rect = screen.get_rect()
    spacing: int = uisd.ui_registry["title_screen_spacing"]
    title = uisd.ui_registry["title_screen_fields"][0]
    subtitle = uisd.ui_registry["title_screen_fields"][1]
    copyright_notice = uisd.ui_registry["title_screen_fields"][2]
    progress_bar = uisd.ui_registry["title_screen_fields"][3]
    continue_to_main = uisd.ui_registry["title_screen_fields"][4]

    if not uisd.position_flag:
        title.text_rect.centerx = screen_rect.centerx
        title.text_rect.bottom = screen_rect.centery - spacing
        subtitle.text_rect.centerx = screen_rect.centerx
        subtitle.text_rect.top = screen_rect.centery + spacing
        copyright_notice.text_rect.centerx = screen_rect.centerx
        copyright_notice.text_rect.bottom = screen_rect.bottom - spacing
        progress_bar.container_rect.centery = screen_rect.height * 0.7
        continue_to_main.text_rect.centery = progress_bar.container_rect.centery
        uisd.position_flag = True


"""Background functions for main menu screen."""

def position_main_menu_screen_elements(screen) -> None:
    """Format and position objects from 'ui_registry' for main menu screen.
    ARGS:
        screen: PyGame window.
    """
    screen_rect: pygame.Rect = screen.get_rect()
    spacing: int = uisd.ui_registry["title_screen_spacing"]
    button_spacing: int = uisd.ui_registry["button_spacing"]
    title = uisd.ui_registry["main_menu_title"]
    start = uisd.ui_registry["start_button"]
    menu_buttons = uisd.ui_registry["menu_buttons"]

    if not uisd.position_flag:
        title.text_rect.centery = screen_rect.height / 4
        title.text_rect.centerx = screen_rect.centerx
        start.button_rect.width = screen_rect.width / 4
        start.button_rect.centerx = screen_rect.centerx
        start.button_rect.bottom = screen_rect.centery - spacing

        for index, button in enumerate(menu_buttons):
            button.button_rect.width = screen_rect.width / 6
            button.button_rect.centerx = screen_rect.centerx

            if index == 0:
                button.button_rect.top = screen_rect.centery + spacing * 2
            else:
                button.button_rect.top = menu_buttons[index - 1].button_rect.bottom + button_spacing

        uisd.position_flag = True


"""Background functions for character menu screen."""

def position_character_menu_screen_elements(screen) -> None:
    """Position objects from 'ui_registry' for character menu screen.
    ARGS:
        screen: PyGame window.
    """
    screen_rect: pygame.Rect = screen.get_rect()
    custom = uisd.ui_registry["custom"]
    random = uisd.ui_registry["random"]
    button_spacing: int = uisd.ui_registry["button_spacing"]

    if not uisd.position_flag:
        custom.button_rect.centerx = screen_rect.centerx
        custom.button_rect.bottom = screen_rect.centery - (button_spacing / 2)
        random.button_rect.centerx = screen_rect.centerx
        random.button_rect.top = screen_rect.centery + (button_spacing / 2)

        uisd.position_flag = True


"""Background functions for ability scores screen."""

def draw_ability_scores_screen_elements(screen, abilities_array: tuple[tuple[object, list[int]], ...],
                                            mouse_pos) -> None:
    """Position, format and draw objects for ability scores screen. 'abilities_array' stores ability objects in function
    'show_ability_scores_screen()'.
    ARGS:
        screen: PyGame window.
        abilities_array: Array of screen objects representing abilities and ability scores.
            See function 'show_ability_scores_screen()' in 'gui/gui.py' for detailed description of its structure and
            purpose.
        mouse_pos: position of mouse on screen.
    """
    draw_abilities_background(screen, abilities_array)

    ability_name_x: int = screen.get_rect().width / 3
    ability_score_x: int = screen.get_rect().width / 6 * 3.7
    bonus_penalty_x: int = screen.get_rect().width / 6 * 4

    element_pos_y, pos_y_offset = set_elements_pos_y_values(screen, abilities_array)

    # Create instances of class 'TextField' to show ability scores and bonus/penalty on screen. Text string is placeholder
    # and is dynamically changed for each ability in for-loop further down.
    field_text_size: int = abilities_array[0][0].size
    ability_score_field = TextField(screen, "score", field_text_size)
    bonus_penalty_field = TextField(screen, "bonus_penalty", field_text_size)

    for ability_name, ability_score in abilities_array:
        ability_name.interactive_rect.top = element_pos_y
        ability_name.interactive_rect.left = ability_name_x

        format_ability_fields(ability_score, ability_score_field, bonus_penalty_field)

        ability_score_field.text_rect.top = ability_name.interactive_rect.top
        ability_score_field.text_rect.right = ability_score_x
        bonus_penalty_field.text_rect.top = ability_score_field.text_rect.top
        bonus_penalty_field.text_rect.right = bonus_penalty_x

        ability_name.draw_interactive_text(mouse_pos)
        ability_score_field.draw_text()
        bonus_penalty_field.draw_text()

        element_pos_y += pos_y_offset


def format_ability_fields(ability_score: list[int], ability_score_field: TextField, bonus_penalty_field: TextField)\
        -> None:
    """Format text attributes for ability score- and bonus/penalty fields text attribute, and add correct prefix or set
    empty string for bonus/penalty.
    ARGS:
        ability_score: list of ability score values with base score at index '0', and bonus/penalty at index '1'.
        ability_score_field: instance of class 'TextField' to display ability scores.
        bonus_penalty_field: instance of class 'TextField' to display bonus/penalty scores.
    """
    ability_score_field.text = str(ability_score[0])
    ability_score_field.render_new_text_surface()
    bonus_penalty_int: int = ability_score[1]
    bonus_penalty_str: str = f"{bonus_penalty_int}"

    # Check bonus/penalty for positive or negative value to apply correct prefix in text field or give out an empty
    # string if bonus_penalty is 0.
    if bonus_penalty_int > 0:
        bonus_penalty_str = f"+{bonus_penalty_str}"
    elif bonus_penalty_int == 0:
        bonus_penalty_str = ""

    bonus_penalty_field.text = bonus_penalty_str
    bonus_penalty_field.render_new_text_surface()


def draw_abilities_background(screen, abilities_array: tuple[tuple[object, list[int]], ...]) -> None:
    """Scale, position and display background for ability score block on abilities screen.
    ARGS:
        screen: PyGame Window.
        abilities_array: Array of screen objects representing abilities and ability scores.
            See function 'show_ability_scores_screen()' in 'gui/gui.py' for detailed description of its structure and
            purpose.
    """
    # Helper variables for better readability.
    screen_rect = screen.get_rect()
    n_ablts: int = len(abilities_array)
    ablts_arr_mid_index: int = n_ablts // 2
    ablts_arr_mid_rect = abilities_array[ablts_arr_mid_index][0].interactive_rect
    ablts_arr_mid_prev_rect = abilities_array[ablts_arr_mid_index-1][0].interactive_rect

    ability_field_height = ablts_arr_mid_rect.height
    image_height_multiplier = n_ablts * 2.5

    image = uisd.ui_registry["parchment_images"][1]
    image_width = screen_rect.width / 1.8
    image_height = ability_field_height * image_height_multiplier

    image_loaded = pygame.transform.scale(image, (image_width, image_height))
    image_rect = image_loaded.get_rect(centerx=screen_rect.centerx)

    # Set image y-position based on number of abilities in 'abilities_array' to assure background is properly centered.
    if n_ablts % 2 == 0:
        image_center_y_offset = (ablts_arr_mid_rect.top - ablts_arr_mid_prev_rect.bottom) / 2
        image_rect.centery = ablts_arr_mid_rect.top - image_center_y_offset
    else:
        image_rect.centery = ablts_arr_mid_rect.centery

    screen.blit(image_loaded, image_rect)


"""Background functions for race/class selection screen."""

def race_class_check(rc_options: dict[str, list[InteractiveText]], active_races: tuple[InteractiveText, ...],
                     active_classes: tuple[InteractiveText, ...], race_name: str, class_name: str)\
        -> dict[str, list[InteractiveText]]:
    """Check 'active_races' and 'active_classes' and populate/return dict 'rc_options' with allowed races and classes
    for use in function 'get_rc_options()'.
    ARGS:
        rc_options: dict for instances of 'InteractiveText' for allowed races and classes.
        active_races: tuple containing 'InteractiveText' instances for all available races in game.
        active_classes: tuple containing 'InteractiveText' instances for all available classes in game.
        race_name: name of allowed race as string for check.
        class_name: name of allowed class as string for check.
    RETURNS:
        rc_options
    """
    for race in active_races:
        if race.text == race_name and race not in rc_options["races"]:
                rc_options["races"].append(race)

    for cls in active_classes:
        if cls.text == class_name and cls not in rc_options["classes"]:
                rc_options["classes"].append(cls)

    return rc_options


def get_rc_options(active_races: tuple[InteractiveText, ...], active_classes: tuple[InteractiveText, ...])\
        -> dict[str, list[InteractiveText]]:
    """Create dict and populate it with instances from 'active_races' and 'active_classes' using function
    'race_class_check()' if their 'text' attributes match entries in 'sd.possible_characters' (first word for race,
    second for class) and return it in 'rc_options'.
    ARGS:
        active_races: entry from ui_registry dict 'ui_registry["active_races"]'.
        active_classes: entry from ui_registry dict 'ui_registry["active_classes"]'.
    RETURNS:
        rc_options: dict for instances of 'InteractiveText' for allowed races and classes.
    """
    rc_options: dict[str, list] = {
        "races": [],
        "classes": [],
    }

    for character in sd.possible_characters:
        race_name, class_name = character.split()

        # Add all available races and classes to dict if none are selected.
        if not sd.selected_race and not sd.selected_class:
            rc_options = race_class_check(rc_options, active_races, active_classes, race_name, class_name)

        # Add only classes that are compatible with selected race to dict.
        elif sd.selected_race and sd.selected_race.text == race_name:
            rc_options = race_class_check(rc_options, active_races, active_classes, race_name, class_name)

        # Add only races that are compatible with selected class to dict.
        elif sd.selected_class and sd.selected_class.text == class_name:
            rc_options = race_class_check(rc_options, active_races, active_classes, race_name, class_name)

    return rc_options


def position_race_class_elements(screen, active_races: tuple[InteractiveText, ...], inactive_races: tuple[TextField, ...],
                                     active_classes: tuple[InteractiveText, ...], inactive_classes: tuple[TextField, ...])\
        -> None:
    """Position screen elements for race/class selection screen.
    ARGS:
        screen: pygame window.
        active_races: entry from ui_registry dict 'ui_registry["active_races"]'.
        inactive_races: entry from ui_registry dict 'ui_registry["inactive_races"]'.
        active_classes: entry from ui_registry dict 'ui_registry["active_classes"]'.
        inactive_classes: entry from ui_registry dict 'ui_registry["inactive_classes"]'.
    """
    race_x_pos: int = int(screen.get_rect().width / 4)
    class_x_pos: int = race_x_pos * 3

    if not uisd.position_flag:
        get_pos_y_dict(screen, active_races, uisd.race_pos_y_dict)  # Race y-positions.
        get_pos_y_dict(screen, active_classes, uisd.class_pos_y_dict)  # Class y-positions.

        # Populate dict with instances of InteractiveText representing available race/class options.
        uisd.rc_options = get_rc_options(active_races, active_classes)
        # Create set of strings to check if inactive or selectable text field should be displayed.
        check_set: set[str] = set([r.text for r in uisd.rc_options["races"]] + [c.text for c in uisd.rc_options["classes"]])

        # Position ALL race/class elements from 'ui_registry' at default position outside the screen to avoid persistent
        # on-screen position of screen objects.
        for race_class in active_races + active_classes + inactive_races + inactive_classes:
            if isinstance(race_class, InteractiveText):
                race_class.interactive_rect.bottomright = uisd.ui_registry["off_screen_pos"]
            elif isinstance(race_class, TextField):
                race_class.text_rect.bottomright = uisd.ui_registry["off_screen_pos"]

        for race in inactive_races:
            if race.text in check_set:
                for r in uisd.rc_options["races"]:
                    r.interactive_rect.centerx, r.interactive_rect.centery = race_x_pos, uisd.race_pos_y_dict[r.text]
            else:
                race.text_rect.centerx, race.text_rect.centery = race_x_pos, uisd.race_pos_y_dict[race.text]

        for cls in inactive_classes:
            if cls.text in check_set:
                for c in uisd.rc_options["classes"]:
                    c.interactive_rect.centerx, c.interactive_rect.centery = class_x_pos, uisd.class_pos_y_dict[c.text]
            else:
                cls.text_rect.centerx, cls.text_rect.centery = class_x_pos, uisd.class_pos_y_dict[cls.text]

        uisd.position_flag = True


def draw_race_class_selection_elements(screen, active_races: tuple[InteractiveText, ...],
                                       active_classes: tuple[InteractiveText, ...], inactive_races: tuple[TextField, ...],
                                       inactive_classes: tuple[TextField, ...], mouse_pos) -> None:
    """Call positioning function and draw screen elements for race/class selection.
    ARGS:
        screen: pygame window.
        active_races: entry from ui_registry dict 'ui_registry["active_races"]'.
        inactive_races: entry from ui_registry dict 'ui_registry["inactive_races"]'.
        active_classes: entry from ui_registry dict 'ui_registry["active_classes"]'.
        inactive_classes: entry from ui_registry dict 'ui_registry["inactive_classes"]'.
        mouse_pos: position of mouse on screen.
    """
    position_race_class_elements(screen, active_races, inactive_races, active_classes, inactive_classes)
    # TODO add background image function call here!

    for race in active_races + inactive_races:
        if isinstance(race, InteractiveText):
            race.draw_interactive_text(mouse_pos)
        elif isinstance(race, TextField):
            race.draw_text()

    for cls in active_classes + inactive_classes:
        if isinstance(cls, InteractiveText):
            cls.draw_interactive_text(mouse_pos)
        elif isinstance(cls, TextField):
            cls.draw_text()


"""Background functions for spell selection screen."""

def position_spell_selection_screen_elements(screen, spells: tuple[InteractiveText, ...]) -> None:
    """Position elements for spell selection on screen.
    ARGS:
        screen: pygame window.
        spells: tuple containing instances of class 'InteractiveText' representing available spells.
    """
    if not uisd.position_flag:
        pos_y_start, pos_y_offset = set_elements_pos_y_values(screen, spells)

        for index, spell in enumerate(spells):
            spell.interactive_rect.centerx = screen.get_rect().centerx
            if index == 0:
                spell.interactive_rect.centery = pos_y_start
            else:
                spell.interactive_rect.centery = pos_y_start + pos_y_offset * index

        uisd.position_flag = True


def draw_spell_selection_screen_elements(screen, spells: tuple[InteractiveText, ...], screen_note: TextField,
                                         mouse_pos) -> None:
    """Position and draw spell selection screen elements.
    ARGS:
        screen: pygame window.
        spells: tuple containing instances of class 'InteractiveText' representing available spells.
        screen_note: 'TextField' instance showing notes for spell selection.
        mouse_pos: position of mouse on screen.
    """
    position_spell_selection_screen_elements(screen, spells)
    draw_elements_array_background_image(screen, spells)

    for spell in spells:
        spell.draw_interactive_text(mouse_pos)

    draw_screen_note(screen, screen_note)


"""Background functions for spell selection screen."""

def position_language_selection_screen_elements(screen, languages: tuple[InteractiveText, ...],
                                                    inactive_languages: tuple[TextField]) -> None:
    """Position active or inactive elements for language selection on- or off-screen based on 'selected' status and
    flag 'uisd.lang_selection_active'.
    ARGS:
        screen: pygame window.
        languages: tuple containing instances of class 'InteractiveText' representing available languages.
        inactive_languages: tuple containing instances of class 'TextField' representing non-selectable languages.
    """
    if not uisd.position_flag:
        get_pos_y_dict(screen, languages, uisd.lang_pos_y_dict)

        # Position selectable 'InteractiveText' instances from 'languages'.
        for language in languages:
            if uisd.lang_selection_active:
                # Position all selectable languages on screen if selection is still permitted (maximum number of
                # additional languages is higher than number of selected languages).
                language.interactive_rect.centerx = screen.get_rect().centerx
                language.interactive_rect.centery = uisd.lang_pos_y_dict[language.text]
            else:
                if language.selected:
                    # Position selected languages always on screen regardless of 'uisd.lang_selection_active' to
                    # ensure that they can still be deselected.
                    language.interactive_rect.centerx = screen.get_rect().centerx
                    language.interactive_rect.centery = uisd.lang_pos_y_dict[language.text]
                else:
                    language.interactive_rect.bottomright = uisd.ui_registry["off_screen_pos"]

        # Position greyed-out 'TextField' instances from 'inactive_languages'.
        for index, inactive_language in enumerate(inactive_languages):
            if languages[index].selected or uisd.lang_selection_active:
                # Move elements off-screen when corresponding selectable element has been selected or selection is still
                # permitted.
                inactive_language.text_rect.bottomright = uisd.ui_registry["off_screen_pos"]
            else:
                # Position inactive elements on screen if previous conditions do not apply.
                inactive_language.text_rect.centerx = screen.get_rect().centerx
                inactive_language.text_rect.centery = uisd.lang_pos_y_dict[inactive_language.text]

        uisd.position_flag = True


def draw_language_selection_screen_elements(screen, languages: tuple[InteractiveText, ...], inactive_languages: tuple[TextField],
                                            screen_note: TextField, mouse_pos) -> None:
    """Position and draw language selection screen elements.
    ARGS:
        screen: pygame window.
        languages: tuple containing instances of class 'InteractiveText' representing available languages.
        inactive_languages: tuple containing instances of class 'TextField' representing non-selectable languages.
        screen_note: 'TextField' instance showing notes for language selection.
        mouse_pos: position of mouse on screen.
    """
    position_language_selection_screen_elements(screen, languages, inactive_languages)
    # TODO add background image function call here!

    for language in languages + inactive_languages:
        if isinstance(language, InteractiveText):
            language.draw_interactive_text(mouse_pos)
        elif isinstance(language, TextField):
            language.draw_text()

    draw_screen_note(screen, screen_note)


"""Background functions for character naming screen."""

def build_and_position_prompt(screen, naming_prompt: TextField) -> None:
    """Create text for 'TextField' instance 'naming_prompt' to include character's race and class, and position it on
    screen.
    ARGS:
        screen: PyGame window.
        naming_prompt: instance of 'TextField' class prompting the user to input a character name.
    """
    if not uisd.position_flag:
        # Add naming prompt to 'naming_prompt.text' attribute and render text_rect.
        naming_prompt.text = f"Name your {sd.character.race_name} {sd.character.class_name}"
        naming_prompt.text_surface = naming_prompt.font.render(naming_prompt.text, True, naming_prompt.text_color)
        naming_prompt.text_rect = naming_prompt.text_surface.get_rect()

        naming_prompt.text_rect.centerx, naming_prompt.text_rect.centery = screen.get_rect().centerx, screen.get_rect().centery / 1.3

        uisd.position_flag = True


"""Background functions for starting money screen."""

def position_money_screen_elements(screen) -> None:
    """Position objects from 'ui_registry' for starting money screen.
    ARGS:
        screen: PyGame window.
    """
    if not uisd.position_flag:
        money_button_pos_y: int = screen.get_rect().height / 3
        random_money_button, custom_money_button = (uisd.ui_registry["starting_money_choices"][0],
                                                    uisd.ui_registry["starting_money_choices"][1])
        random_money_button.button_rect.top, random_money_button.button_rect.centerx = (money_button_pos_y,
                                                                                        screen.get_rect().centerx * 0.5)
        custom_money_button.button_rect.top, custom_money_button.button_rect.centerx = (money_button_pos_y,
                                                                                        screen.get_rect().centerx * 1.5)

        rolling_dice_money_field, random_money_field = (uisd.ui_registry["random_money"][0],
                                                        uisd.ui_registry["random_money"][1])
        rolling_dice_money_field.text_rect.centery, random_money_field.text_rect.centery = (screen.get_rect().centery * 1.1,
                                                                                            screen.get_rect().centery * 1.1)
        money_input_prompt: TextField = uisd.ui_registry["money_amount_input"][2]
        money_input_prompt.text_rect.centery = screen.get_rect().centery * 1.05
        money_amount_field: TextInputField = uisd.ui_registry["money_amount_input"][1]
        money_amount_field.input_bg_field.top = screen.get_rect().centery * 1.15

        uisd.position_flag = True


def choose_money_option(choices: list[Button], mouse_pos) -> None:
    """Choose option to either generate random amount of money or let user input a custom amount, return 'starting_money'
    if random amount is chosen, set and return 'random_money_flag'/'custom_money_flag' accordingly.
    ARGS:
        choices: List of instances of 'Button' class from dict 'ui_registry'.
        mouse_pos: position of mouse on screen.
    """
    random_money: pygame.Rect = choices[0].button_rect
    custom_money: pygame.Rect = choices[1].button_rect

    if pygame.mouse.get_pressed()[0]:
        if random_money.collidepoint(mouse_pos):
            sd.random_money_flag, sd.custom_money_flag = True, False
            # Set dice roll timer.
            uisd.dice_roll_start_time = time.time()
        if custom_money.collidepoint(mouse_pos):
            sd.random_money_flag, sd.custom_money_flag = False, True


def draw_chosen_money_option(screen) -> None:
    """Draw message for random amount of starting money or show input field for custom amount on screen.
    ARGS:
        screen: PyGame window.
    """
    text_large: int = uisd.ui_registry["text_large"]
    dice_roll_duration: int | float = 1

    # Random money fields.
    rolling_dice_money_field, random_money_field = (uisd.ui_registry["random_money"][0],
                                                    uisd.ui_registry["random_money"][1])
    # Money input fields.
    money_amount_field: TextInputField = uisd.ui_registry["money_amount_input"][1]
    money_input_prompt: TextField = uisd.ui_registry["money_amount_input"][2]

    if sd.random_money_flag:
        # Check timer to allow for dice roll effect.
        if time.time() - uisd.dice_roll_start_time < dice_roll_duration:
            rolling_dice_money_field.draw_text()
            # Generate random int value for 'starting_money'.
            sd.starting_money = roll_starting_money()
            starting_money_dice_roll(screen, random_money_field, text_large)
        # Show final value after timer runs out.
        else:
            random_money_field.draw_text()
            starting_money_dice_roll(screen, random_money_field, text_large, rolling=False)
            # Reset global dice roll timer. Not strictly necessary, but better safe than sorry.
            uisd.dice_roll_start_time = 0
            uisd.dice_roll_complete = True
    elif sd.custom_money_flag:
        money_input_prompt.draw_text()
        money_amount_field.draw_input_field()


def starting_money_dice_roll(screen, random_money_field: TextField, text_large: object | int, rolling: bool = True) -> None:
    """Display the rolling or final amount of starting money on screen.
    ARGS:
        screen: PyGame window.
        random_money_field: reference text field to position the money display correctly.
        text_large: font size instance for text rendering. Usually 'ui_registry["text_large"]' is used, but any 'int'
            can be passed.
        rolling: boolean flag to indicate if the dice roll is still ongoing.
            If 'True', displays a "rolling" message. If 'False', shows the final amount. Default is 'True'.
    """
    if rolling:
        starting_money_message: str = str(sd.starting_money)
    else:
        starting_money_message: str = str(sd.starting_money) + " gold pieces"

    # Create TextField instance 'random_money_result_field', and position and draw it on screen.
    random_money_result_field = TextField(screen, starting_money_message, text_large)
    random_money_result_field.text_rect.top = random_money_field.text_rect.bottom
    random_money_result_field.draw_text()


"""Background functions for creation complete screen."""

def position_completion_screen_elements(screen, completion_message: TextField, show_character_sheet: Button) -> None:
    """Position screen elements for 'character complete' screen.
    ARGS:
        screen: PyGame window.
        completion_message: instance of class 'TextField' showing completion message.
        show_character_sheet: instance of class 'Button' to proceed to character sheet.
    """
    spacing: int = uisd.ui_registry["title_screen_spacing"]

    if not uisd.position_flag:
        completion_message.text_rect.bottom = screen.get_rect().centery - spacing
        show_character_sheet.button_rect.top = screen.get_rect().centery + spacing
        show_character_sheet.button_rect.centerx = screen.get_rect().centerx

        uisd.position_flag = True
