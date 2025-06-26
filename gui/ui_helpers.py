import pygame
from core.rules import roll_starting_money
import gui.screen_objects as so
import time
from gui.screen_objects import TextField, Button, InteractiveText, TextInputField
from core.shared_data import shared_data as sd
from gui.shared_data import ui_shared_data as uisd

"""Background functions for GUI, i.e. value build/retrieval and object positioning functions for pygame screens."""


"""General functions."""

def draw_screen_title(screen, screen_title: TextField) -> None:
    """Draw 'screen_title' object on screen at default position.
    ARGS:
        screen: PyGame window.
        screen_title: instance of class 'TextField()' representing the screen title.
    """
    screen_title.text_rect.top = screen.get_rect().top + uisd.gui_elements["default_edge_spacing"]
    screen_title.text_rect.centerx = screen.get_rect().centerx
    screen_title.draw_text()


def draw_special_button(screen, button: Button, mouse_pos) -> None:
    """Draw special use button (i.e. 'Roll Again' or 'Reset') at the bottom center of the screen.
    ARGS:
        screen: PyGame window.
        button: instance of class 'Button()' representing the special use button.
        mouse_pos: position of mouse on screen.
    """
    button.button_rect.centerx = screen.get_rect().centerx
    button.button_rect.bottom = screen.get_rect().bottom - uisd.gui_elements["default_edge_spacing"]
    button.draw_button(mouse_pos)


def draw_conditional_continue_button(mouse_pos, condition_1: object | bool = False, condition_2: object | bool = False,
                                     check_mode: str = "any", alt_button: str = "inactive") -> None:
    """Draw either active or inactive instance of continue button or skip button from module 'gui_elements' based on
    conditional parameters.
    NOTE: 'skip' button rect does not need a dedicated '.collidepoint' detection in event handler as it's position is
    identical to the standard 'continue' button rect. Just use that one for event detection and Bob's your uncle.
    ARGS:
        mouse_pos: mouse position on screen.
        condition_1: first condition to be checked. Default is "False".
        condition_2: second condition to be checked. Default is "False".
        check_mode: String to determine whether one or both conditions must be met. Use "any" to require at least one condition,
                    or "all" to require both. Default is "any".
        alt_button: String to determine which conditional button alternative should be displayed. "inactive" for an
                    inactive continue button, "skip" for a skip button. Default is "inactive".
    """
    # Assign buttons from dict 'gui_elements' to variables.
    continue_button, inactive_continue_button, skip_button = (uisd.gui_elements["continue_button"],
                                                              uisd.gui_elements["inactive_continue_button"],
                                                              uisd.gui_elements["skip_button"])

    # Check if condition_1 and/or condition_2 have valid values and draw appropriate (active/inactive) continue or skip
    # button on screen.
    if check_mode == "any" and (condition_1 or condition_2):
        continue_button.draw_button(mouse_pos)
    elif check_mode == "all" and (condition_1 and condition_2):
        continue_button.draw_button(mouse_pos)
    else:
        # Check which alternative button should be displayed if no previous conditions are met.
        if alt_button == "inactive":
            inactive_continue_button.draw_button(mouse_pos)
        elif alt_button == "skip":
            skip_button.draw_button(mouse_pos)


def draw_screen_note(screen, note: TextField) -> None:
    """Position and draw screen-specific notes on screen.
    ARGS:
        screen: PyGame window.
        note: 'TextField' instance for screen-specific notes.
    """
    # Position notes at the screens left.
    note.text_rect.left = screen.get_rect().left + uisd.gui_elements["default_edge_spacing"]
    note.text_rect.centery = screen.get_rect().bottom - screen.get_rect().height / 2
    # Draw note on screen.
    note.draw_text()


def set_elements_pos_y_values(screen, elements: list | tuple) -> tuple[int, int]:
    """Dynamically set starting y-position for GUI elements on screen based on number of said elements.
    Screen layout is designed to adapt and fit up to 16 elements.
    ARGS:
        screen: PyGame window.
        elements: List/tuple or array to store GUI elements.
    RETURNS:
        elements_pos_y: Y-position for first GUI element on screen.
        pos_y_offset: Offset value to position following elements.
    """
    # Set reference variables for positioning.
    screen_center_y = screen.get_rect().centery
    n_elements: int = len(elements)
    # Check 'elements' for type and assign first element to variable as reference object for further positioning.
    ref_element = elements[0][0] if isinstance(elements[0], (list, tuple)) else elements[0]

    # Position 'ref_element' at the y-center axis for final 'element_pos_y' calculation further down. Exact position of
    # 'ref_element' based on evenness of 'n_elements'.
    if n_elements % 2 == 0:
        # Even number of elements in 'elements'.
        ref_element.text_rect.top = screen_center_y
    else:
        # Odd number of elements in 'elements'.
        ref_element.text_rect.centery = screen_center_y

    # Calculate offset multiplier for use in 'pos_y_offset' based on number of abilities in 'elements'.
    if n_elements <= 8:
        offset_multiplier: int | float = 2
    elif n_elements <= 11:
        offset_multiplier: int | float = 1.5
    else:
        offset_multiplier: int | float = 1

    # Set initial position on y-axis for ability score fields and offset value for spacing between each element.
    pos_y_offset = ref_element.text_rect.height * offset_multiplier
    element_pos_y = ref_element.text_rect.top - (int(n_elements / 2) * pos_y_offset)

    return element_pos_y, pos_y_offset


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
    else:
        if isinstance(elements, InteractiveText):
            elements.handle_mouse_interaction_info_panels(mouse_pos)


"""Background functions for title screen."""

def position_title_screen_elements(screen) -> None:
    """Position objects from 'gui_elements' for title screen.
    ARGS:
        screen: PyGame window.
    """
    # Assign gui_elements to variables.
    spacing: int = uisd.gui_elements["title_screen_spacing"]
    title = uisd.gui_elements["title_screen_fields"][0]
    subtitle = uisd.gui_elements["title_screen_fields"][1]
    copyright_notice = uisd.gui_elements["title_screen_fields"][2]
    progress_bar = uisd.gui_elements["title_screen_fields"][3]
    continue_to_main = uisd.gui_elements["title_screen_fields"][4]

    if not uisd.position_flag:
        # Position title, subtitle and copyright notice.
        title.text_rect.centerx = screen.get_rect().centerx
        title.text_rect.bottom = screen.get_rect().centery - spacing
        subtitle.text_rect.centerx = screen.get_rect().centerx
        subtitle.text_rect.top = screen.get_rect().centery + spacing
        copyright_notice.text_rect.centerx = screen.get_rect().centerx
        copyright_notice.text_rect.bottom = screen.get_rect().bottom - spacing
        progress_bar.container_rect.centery = screen.get_rect().height * 0.7
        continue_to_main.text_rect.centery = progress_bar.container_rect.centery
        uisd.position_flag = True


"""Background functions for main menu screen."""

def position_main_menu_screen_elements(screen) -> None:
    """Format and position objects from 'gui_elements' for main menu screen.
    ARGS:
        screen: PyGame window.
    """
    # Assign gui_elements to variables.
    spacing: int = uisd.gui_elements["title_screen_spacing"]
    button_spacing: int = uisd.gui_elements["button_spacing"]
    title = uisd.gui_elements["main_menu_title"]
    start = uisd.gui_elements["start_button"]
    menu_buttons = uisd.gui_elements["menu_buttons"]

    if not uisd.position_flag:
        # Format/position title text field and start button.
        title.text_rect.centery = screen.get_rect().height / 4
        title.text_rect.centerx = screen.get_rect().centerx
        start.button_rect.width = screen.get_rect().width / 4
        start.button_rect.centerx = screen.get_rect().centerx
        start.button_rect.bottom = screen.get_rect().centery - spacing

        # Format, position and draw additional menu buttons.
        for index, button in enumerate(menu_buttons):
            button.button_rect.width = screen.get_rect().width / 6
            button.button_rect.centerx = screen.get_rect().centerx

            if index == 0:
                button.button_rect.top = screen.get_rect().centery + spacing * 2
            else:
                button.button_rect.top = menu_buttons[index - 1].button_rect.bottom + button_spacing

        uisd.position_flag = True


"""Background functions for character menu screen."""

def position_character_menu_screen_elements(screen) -> None:
    """Position objects from 'gui_elements' for character menu screen.
    ARGS:
        screen: PyGame window.
    """
    # Assign gui_elements to variables.
    custom = uisd.gui_elements["custom"]
    random = uisd.gui_elements["random"]
    button_spacing: int = uisd.gui_elements["button_spacing"]

    if not uisd.position_flag:
    # Position buttons.
        custom.button_rect.centerx = screen.get_rect().centerx
        custom.button_rect.bottom = screen.get_rect().centery - (button_spacing / 2)
        random.button_rect.centerx = screen.get_rect().centerx
        random.button_rect.top = screen.get_rect().centery + (button_spacing / 2)

        uisd.position_flag = True


"""Background functions for ability scores screen."""

def position_ability_scores_screen_elements(screen, abilities_array: tuple[tuple[object, list[int]], ...],
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
    # X-positions for ability, score and bonus/penalty columns.
    ability_name_x: int = screen.get_rect().width / 3
    ability_score_x: int = screen.get_rect().width / 6 * 3.7
    bonus_penalty_x: int = screen.get_rect().width / 6 * 4
    # Get y-position for first ability object and position offset value for further objects.
    element_pos_y, pos_y_offset = set_elements_pos_y_values(screen, abilities_array)

    # Create instances of class 'TextField' to show ability scores and bonus/penalty on screen. Text string is placeholder
    # and text size is 'field_text_size' as retrieved from first 'gui_elements' entry in 'abilities_array' to ensure
    # correct scaling. Placeholder text is dynamically changed for each ability in for-loop further down.
    field_text_size: int = abilities_array[0][0].size
    ability_score_field = so.TextField(screen, "score", field_text_size)
    bonus_penalty_field = so.TextField(screen, "bonus_penalty", field_text_size)

    # Loop through each ability and corresponding stats to format, position and display the ability name, score and
    # bonus/penalty as they are grouped in 'abilities_array'.
    for ability_name, ability_score in abilities_array:
        # 'Pre-formatting' bonus/penalty to string for easier formatting and better code-readability further down.
        bonus_penalty: str = f"{ability_score[1]}"
        # Check bonus/penalty for positive or negative value to apply correct prefix in text field or give out an empty
        # string if bonus_penalty is 0.
        if ability_score[1] > 0:
            bonus_penalty: str = f"+{bonus_penalty}"
        elif ability_score[1] == 0:
            bonus_penalty: str = ""

        # Position and draw ability name on screen.
        ability_name.interactive_rect.top = element_pos_y
        ability_name.interactive_rect.left = ability_name_x
        ability_name.draw_interactive_text(mouse_pos)

        # Change contents and re-render 'TextField' instances for each ability score stat.
        ability_score_field.text = str(ability_score[0])
        ability_score_field.render_new_text_surface()
        bonus_penalty_field.text = bonus_penalty
        bonus_penalty_field.render_new_text_surface()

        # Position and draw ability score and bonus/penalty on screen.
        ability_score_field.text_rect.top = ability_name.interactive_rect.top
        ability_score_field.text_rect.right = ability_score_x
        bonus_penalty_field.text_rect.top = ability_score_field.text_rect.top
        bonus_penalty_field.text_rect.right = bonus_penalty_x
        ability_score_field.draw_text()
        bonus_penalty_field.draw_text()

        # Set new y-position for next element.
        element_pos_y += pos_y_offset


"""Background functions for race/class selection screen."""

def race_class_check(available_choices: dict[str, list[InteractiveText]], active_races: tuple[InteractiveText],
                     active_classes: tuple[InteractiveText], race_name: str, class_name: str) -> dict[str, list[InteractiveText]]:
    """Check 'active_races' and 'active_classes' and populate/return dict 'available_choices' with allowed race/class
    combinations for use in function 'get_available_choices()'.
    ARGS:
        available_choices: dict for instances of 'InteractiveText' for allowed race/class combinations.
        active_races: tuple containing 'InteractiveText' instances for all available races in game.
        active_classes: tuple containing 'InteractiveText' instances for all available classes in game.
        race_name: name of allowed race as string for check.
        class_name: name of allowed class as string for check.
    RETURNS:
        available_choices
    """
    # Check if the race matches.
    for race in active_races:
        if race.text == race_name:
            # Assuring only one instance of each object is added to dict.
            if race not in available_choices["races"]:
                available_choices["races"].append(race)
    # Check if the class matches.
    for cls in active_classes:
        if cls.text == class_name:
            # Assuring only one instance of each object is added to dict.
            if cls not in available_choices["classes"]:
                available_choices["classes"].append(cls)

    return available_choices


def get_available_choices(active_races: tuple[InteractiveText], active_classes: tuple[InteractiveText])\
        -> dict[str, list[InteractiveText]]:
    """Create dict and populate it with instances from 'active_races' and 'active_classes' using function
        'race_class_check()' if their 'text' attributes match entries in 'possible_characters' (first word for race,
        second for class) and return it in 'available_choices'.
    ARGS:
        active_races: entry from gui element dict 'gui_elements["active_races"]'.
        active_classes: entry from gui element dict 'gui_elements["active_classes"]'.
    RETURNS:
        available_choices: dict for instances of 'InteractiveText' for allowed race/class combinations.
    """
    # Dictionary for available race and class choices to be returned.
    available_choices: dict[str, list] = {
        "races": [],
        "classes": [],
    }

    for character in sd.possible_characters:
        # Split each possible character to get race and class.
        race_name, class_name = character.split()

        # Add all available races and classes to dict if none are selected.
        if not sd.selected_race and not sd.selected_class:
            available_choices = race_class_check(available_choices, active_races, active_classes, race_name, class_name)

        # Add only classes that are compatible with selected race to dict.
        elif sd.selected_race and sd.selected_race.text == race_name:
            available_choices = race_class_check(available_choices, active_races, active_classes, race_name, class_name)

        # Add only races that are compatible with selected class to dict.
        elif sd.selected_class and sd.selected_class.text == class_name:
            available_choices = race_class_check(available_choices, active_races, active_classes, race_name, class_name)

    return available_choices


def get_position_race_class_element(screen, race_class: InteractiveText | TextField, inactive_elements: list[TextField])\
        -> tuple[int, int]:
    """Get and return x and y values for GUI elements in function 'draw_available_choices()'.
    ARGS:
        screen: PyGame window.
        race_class: GUI element to be positioned.
        inactive_elements: list of text field instances for non-choose able races/classes. Used here only to be passed
            to function 'get_race_class_y_position()' for further y-coordinates calculations.
    RETURNS:
        x, y: x and y position on screen for 'race_class' object.
    """
    # Race and class specific variables for x-positioning.
    race_x_pos: int = int(screen.get_rect().width / 4)
    class_x_pos: int = race_x_pos * 3
    # Lists of races and classes from dict 'rc_dict' for checks and calculation of y-positions.
    races_list: list[str] = sd.rc_dict["races"]
    classes_list: list[str] = sd.rc_dict["classes"]

    # Check if 'race_class' represents a race or a class and retrieve correct x- and y-positions.
    if race_class.text in races_list:
        x = race_x_pos
        y = get_race_class_y_position(screen, race_class, races_list, inactive_elements)
    elif race_class.text in classes_list:
        x = class_x_pos
        y = get_race_class_y_position(screen, race_class, classes_list, inactive_elements)

    return x, y


def get_race_class_y_position(screen, race_class: InteractiveText | TextField, rc_dict_list: list[str],
                              inactive_elements: list[TextField]) -> int:
    """Helper function to get and return y value for GUI element in function 'get_position_race_class_element()'.
    ARGS:
        screen: pygame window.
        race_class: GUI element to be positioned.
        rc_dict_list: value of type 'list' from 'rc_dict' as assigned to variable in 'get_position_race_class_element()'.
        inactive_elements: list of text field instances for non-choose able races/classes. Used here only to be passed
            to function 'set_elements_pos_y_values()' for further y-coordinates calculations.
    RETURNS:
        y: y position on screen for 'race_class' object.
    """
    # Get dynamic y-positions for items in 'spells'.
    pos_y_start, pos_y_offset = set_elements_pos_y_values(screen, inactive_elements)

    for index, item in enumerate(rc_dict_list):
        if race_class.text == item:
            if index == 0:
                y = pos_y_start
            else:
                y = pos_y_start + pos_y_offset * index

    return y


def draw_available_choices(screen, available_choices: dict[str, list[InteractiveText]],
                           inactive_races: list[TextField], inactive_classes: list[TextField], mouse_pos) -> None:
    """Get position of text field items in dict 'available_choices' and draw them on screen.
    ARGS:
        screen: pygame window.
        available_choices: dict with instances of interactive text fields for race and class selection.
        inactive_races: list of text field instances for non-choose able races.
        inactive_classes: list of text field instances for non-choose able classes.
        mouse_pos: position of mouse on screen.
    """
    # Create list to check if inactive or selectable text field should be displayed.
    check_list: list[str] = [r.text for r in available_choices["races"]] + [c.text for c in available_choices["classes"]]

    # Position ALL selectable race/class text fields from 'gui_elements' at default position outside the screen to avoid
    # persistent on-screen position of fields that become unavailable during selection (i.e. races that are incompatible
    # with selected class or vice versa). Avoids said race/class fields still being selectable even when inactive.
    for race in uisd.gui_elements["active_races"]:
        race.interactive_rect.bottomright = screen.get_rect().topright
    for cls in uisd.gui_elements["active_classes"]:
        cls.interactive_rect.bottomright = screen.get_rect().topright

    # Position/draw race selection.
    for race in inactive_races:
        # Check if race.text attribute is in 'check_list', proceed with active UI object if so, inactive object otherwise.
        if race.text in check_list:
            for r in available_choices["races"]:
                r.interactive_rect.centerx, r.interactive_rect.centery = get_position_race_class_element(screen, r,
                                                                                                      inactive_races)
                r.draw_interactive_text(mouse_pos)
        else:
            race.text_rect.centerx, race.text_rect.centery = get_position_race_class_element(screen, race, inactive_races)
            race.draw_text()

    # Position/draw class selection.
    for cls in inactive_classes:
        # Check if class.text attribute is in 'check_list', proceed with active UI object if so, inactive object otherwise.
        if cls.text in check_list:
            for c in available_choices["classes"]:
                c.interactive_rect.centerx, c.interactive_rect.centery = get_position_race_class_element(screen, c,
                                                                                                      inactive_classes)
                c.draw_interactive_text(mouse_pos)
        else:
            cls.text_rect.centerx, cls.text_rect.centery = get_position_race_class_element(screen, cls, inactive_classes)
            cls.draw_text()


"""Background functions for spell selection screen."""

def position_spell_selection_screen_elements(screen, spells: tuple[InteractiveText, ...]) -> None:
    """Position elements for spell selection on screen.
    ARGS:
        screen: pygame window.
        spells: tuple containing instances of class 'InteractiveText' representing available spells.
    """
    # Get dynamic y-positions for items in 'spells'.
    pos_y_start, pos_y_offset = set_elements_pos_y_values(screen, spells)

    for index, spell in enumerate(spells):
        # Align element x-position at screen center.
        spell.interactive_rect.centerx = screen.get_rect().centerx
        # Assign dynamic y-positions to elements.
        if index == 0:
            spell.interactive_rect.centery = pos_y_start
        else:
            spell.interactive_rect.centery = pos_y_start + pos_y_offset * index


def draw_spell_selection_screen_elements(screen, spells: tuple[InteractiveText, ...], screen_note: TextField,
                                         mouse_pos) -> None:
    """Call positioning method 'position_spell_selection_screen_elements()' and draw item from tuple 'spells' on screen.
    ARGS:
        screen: pygame window.
        spells: tuple containing instances of class 'InteractiveText' representing available spells.
        screen_note: 'TextField' instance showing notes for spell selection.
        mouse_pos: position of mouse on screen.
    """
    # Position elements on screen.
    position_spell_selection_screen_elements(screen, spells)

    # Draw elements from 'spells'.
    for spell in spells:
        spell.draw_interactive_text(mouse_pos)

    # Draw further elements on screen.
    draw_screen_note(screen, screen_note)


"""Background functions for spell selection screen."""

def position_language_selection_screen_elements(screen, languages: tuple[InteractiveText, ...]) -> None:
    """Position elements for spell selection on screen.
    ARGS:
        screen: pygame window.
        languages: tuple containing instances of class 'InteractiveText' representing available languages.
    """
    # Get dynamic y-positions for items in 'languages'.
    pos_y_start, pos_y_offset = set_elements_pos_y_values(screen, languages)

    for index, language in enumerate(languages):
        # Align element x-position at screen center.
        language.interactive_rect.centerx = screen.get_rect().centerx
        # Assign dynamic y-positions to elements.
        if index == 0:
            language.interactive_rect.centery = pos_y_start
        else:
            language.interactive_rect.centery = pos_y_start + pos_y_offset * index


def draw_language_selection_screen_elements(screen, languages: tuple[InteractiveText, ...], screen_note: TextField,
                                            mouse_pos) -> None:
    """Call positioning method 'position_language_selection_screen_elements()' and draw item from tuple 'spells' on
    screen.
    ARGS:
        screen: pygame window.
        languages: tuple containing instances of class 'InteractiveText' representing available languages.
        screen_note: 'TextField' instance showing notes for language selection.
        mouse_pos: position of mouse on screen.
    """
    # Position elements on screen.
    position_language_selection_screen_elements(screen, languages)

    # Draw elements from 'languages'.
    for language in languages:
        language.draw_interactive_text(mouse_pos)

    # Draw further elements on screen.
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

        # Position final naming prompt on screen.
        naming_prompt.text_rect.centerx, naming_prompt.text_rect.centery = screen.get_rect().centerx, screen.get_rect().centery / 1.3

        uisd.position_flag = True


"""Background functions for starting money screen."""

def position_money_screen_elements(screen) -> None:
    """Position objects from 'gui_elements' for starting money screen.
    ARGS:
        screen: PyGame window.
    """
    if not uisd.position_flag:
        # Positioning of button instances.
        money_button_pos_y: int = screen.get_rect().height / 3
        random_money_button, custom_money_button = (uisd.gui_elements["starting_money_choices"][0],
                                                    uisd.gui_elements["starting_money_choices"][1])
        random_money_button.button_rect.top, random_money_button.button_rect.centerx = (money_button_pos_y,
                                                                                        screen.get_rect().centerx * 0.5)
        custom_money_button.button_rect.top, custom_money_button.button_rect.centerx = (money_button_pos_y,
                                                                                        screen.get_rect().centerx * 1.5)

        # Positioning of text input and text field instances.
        rolling_dice_money_field, random_money_field = (uisd.gui_elements["random_money"][0],
                                                        uisd.gui_elements["random_money"][1])
        rolling_dice_money_field.text_rect.centery, random_money_field.text_rect.centery = (screen.get_rect().centery * 1.1,
                                                                                            screen.get_rect().centery * 1.1)
        money_input_prompt: TextField = uisd.gui_elements["money_amount_input"][2]
        money_input_prompt.text_rect.centery = screen.get_rect().centery * 1.05
        money_amount_field: TextInputField = uisd.gui_elements["money_amount_input"][1]
        money_amount_field.input_bg_field.top = screen.get_rect().centery * 1.15

        uisd.position_flag = True


def choose_money_option(choices: list[Button], mouse_pos) -> None:
    """Choose option to either generate random amount of money or let user input a custom amount, return 'starting_money'
    if random amount is chosen, set and return 'random_money_flag'/'custom_money_flag' accordingly.
    ARGS:
        choices: List of instances of 'Button' class from dict 'gui_elements'.
        mouse_pos: position of mouse on screen.
    """
    if pygame.mouse.get_pressed()[0]:
        # Set flags to appropriate values based chosen option.
        if choices[0].button_rect.collidepoint(mouse_pos):
            sd.random_money_flag, sd.custom_money_flag = True, False
            # Set dice roll timer.
            uisd.dice_roll_start_time = time.time()
        if choices[1].button_rect.collidepoint(mouse_pos):
            sd.random_money_flag, sd.custom_money_flag = False, True


def draw_chosen_money_option(screen) -> None:
    """Draw message for random amount of starting money or show input field for custom amount on screen.
    ARGS:
        screen: PyGame window.
    """
    # Set duration for dice roll in seconds.
    dice_roll_duration: int | float = 1

    # Assign font size and text field instances from dict 'gui_elements' to variables.
    text_large: int = uisd.gui_elements["text_large"]
    # Random money fields.
    rolling_dice_money_field, random_money_field = (uisd.gui_elements["random_money"][0],
                                                    uisd.gui_elements["random_money"][1])
    # Money input fields.
    money_amount_field: TextInputField = uisd.gui_elements["money_amount_input"][1]
    money_input_prompt: TextField = uisd.gui_elements["money_amount_input"][2]

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
        text_large: font size instance for text rendering. Usually 'gui_elements["text_large"]' is used, but any 'int'
            can be passed.
        rolling: boolean flag to indicate if the dice roll is still ongoing.
            If 'True', displays a "rolling" message. If 'False', shows the final amount. Default is 'True'.
    """
    # Check if "rolling" message or final amount should be displayed.
    if rolling:
        # Build string 'starting_money_message' for use as argument in TextField instance 'random_money_result_field'.
        starting_money_message: str = str(sd.starting_money)
    else:
        # Build string 'starting_money_message' for use as argument in TextField instance 'random_money_result_field'.
        starting_money_message: str = str(sd.starting_money) + " gold pieces"

    # Create TextField instance 'random_money_result_field', and position and draw it on screen.
    random_money_result_field = so.TextField(screen, starting_money_message, text_large)
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
    # Assign spacing value from 'gui_elements' to variables.
    spacing: int = uisd.gui_elements["title_screen_spacing"]

    if not uisd.position_flag:
        # Position screen elements.
        completion_message.text_rect.bottom = screen.get_rect().centery - spacing
        show_character_sheet.button_rect.top = screen.get_rect().centery + spacing
        show_character_sheet.button_rect.centerx = screen.get_rect().centerx

        uisd.position_flag = True
