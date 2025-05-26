import pygame
from core.rules import roll_starting_money
import gui.screen_objects as so
import time
from gui.screen_objects import TextField, Button, InteractiveText, TextInputField
from gui.shared_data import ui_shared_data as sd

"""Background functions for GUI, i.e. value build/retrieval and object positioning functions for pygame screens."""


"""General functions."""

def draw_screen_title(screen, screen_title: TextField, gui_elements: dict) -> None:
    """Draw 'screen_title' object on screen at default position.
    ARGS:
        screen: PyGame window.
        screen_title: instance of class 'TextField()' representing the screen title.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
    """
    screen_title.text_rect.top = screen.get_rect().top + gui_elements["default_edge_spacing"]
    screen_title.text_rect.centerx = screen.get_rect().centerx
    screen_title.draw_text()


def draw_special_button(screen, button: Button, gui_elements: dict, mouse_pos) -> None:
    """Draw special use button (i.e. 'Roll Again' or 'Reset') at the bottom center of the screen.
    ARGS:
        screen: PyGame window.
        button: instance of class 'Button()' representing the special use button.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
        mouse_pos: position of mouse on screen.
    """
    button.button_rect.centerx = screen.get_rect().centerx
    button.button_rect.bottom = screen.get_rect().bottom - gui_elements["default_edge_spacing"]
    button.draw_button(mouse_pos)


def draw_continue_button_inactive(condition_1: object | bool, condition_2: object | bool, gui_elements: dict, mouse_pos,
                                  check_mode: str = "any") -> None:
    """Draw either active or inactive instance of continue button from module 'gui_elements'.
    ARGS:
        condition_1: first condition to be checked.
        condition_2: second condition to be checked.
        gui_elements: dict containing gui element instances.
        mouse_pos: mouse position on screen.
        check_mode: String to determine whether one or both conditions must be met. Use "any" to require at least one condition,
                    or "all" to require both. Default is "any".
    """
    # Assign buttons from dict 'gui_elements' to variables.
    continue_button, inactive_continue_button = gui_elements["continue_button"], gui_elements["inactive_continue_button"]

    # Check if condition_1 and/or condition_2 have valid values and draw appropriate (active/inactive) continue button on
    # screen.
    if check_mode == "any" and (condition_1 or condition_2):
        continue_button.draw_button(mouse_pos)
    elif check_mode == "all" and (condition_1 and condition_2):
        continue_button.draw_button(mouse_pos)
    else:
        inactive_continue_button.draw_button(mouse_pos)


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

def position_title_screen_elements(screen, gui_elements: dict) -> None:
    """Position objects from 'gui_elements' for title screen.
    ARGS:
        screen: PyGame window.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
    """
    # Assign gui_elements to variables.
    spacing: int = gui_elements["title_screen_spacing"]
    title = gui_elements["title_screen_fields"][0]
    subtitle = gui_elements["title_screen_fields"][1]
    copyright_notice = gui_elements["title_screen_fields"][2]
    progress_bar = gui_elements["title_screen_fields"][3]
    continue_to_main = gui_elements["title_screen_fields"][4]

    if not sd.position_flag:
        # Position title, subtitle and copyright notice.
        title.text_rect.centerx = screen.get_rect().centerx
        title.text_rect.bottom = screen.get_rect().centery - spacing
        subtitle.text_rect.centerx = screen.get_rect().centerx
        subtitle.text_rect.top = screen.get_rect().centery + spacing
        copyright_notice.text_rect.centerx = screen.get_rect().centerx
        copyright_notice.text_rect.bottom = screen.get_rect().bottom - spacing
        progress_bar.container_rect.centery = screen.get_rect().height * 0.7
        continue_to_main.text_rect.centery = progress_bar.container_rect.centery
        sd.position_flag = True


"""Background functions for main menu screen."""

def position_main_menu_screen_elements(screen, gui_elements: dict) -> None:
    """Format and position objects from 'gui_elements' for main menu screen.
    ARGS:
        screen: PyGame window.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
    """
    # Assign gui_elements to variables.
    spacing: int = gui_elements["title_screen_spacing"]
    button_spacing: int = gui_elements["button_spacing"]
    title = gui_elements["main_menu_title"]
    start = gui_elements["start_button"]
    menu_buttons = gui_elements["menu_buttons"]

    if not sd.position_flag:
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

        sd.position_flag = True


"""Background functions for character menu screen."""

def position_character_menu_screen_elements(screen, gui_elements: dict) -> None:
    """Position objects from 'gui_elements' for character menu screen.
    ARGS:
        screen: PyGame window.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
    """
    # Assign gui_elements to variables.
    custom = gui_elements["custom"]
    random = gui_elements["random"]
    button_spacing: int = gui_elements["button_spacing"]

    if not sd.position_flag:
    # Position buttons.
        custom.button_rect.centerx = screen.get_rect().centerx
        custom.button_rect.bottom = screen.get_rect().centery - (button_spacing / 2)
        random.button_rect.centerx = screen.get_rect().centerx
        random.button_rect.top = screen.get_rect().centery + (button_spacing / 2)

        sd.position_flag = True


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


def get_available_choices(possible_characters: list[str], active_races: tuple[InteractiveText],
                          active_classes: tuple[InteractiveText], selected_race: InteractiveText | None,
                          selected_class: InteractiveText | None) -> dict[str, list[InteractiveText]]:
    """Create dict and populate it with instances from 'active_races' and 'active_classes' using function
        'race_class_check()' if their 'text' attributes match entries in 'possible_characters' (first word for race,
        second for class) and return it in 'available_choices'.
    ARGS:
        possible_characters: list of possible race-class combinations as strings.
        active_races: entry from gui element dict 'gui_elements["active_races"]'.
        active_classes: entry from gui element dict 'gui_elements["active_classes"]'.
        selected_race: instance of 'InteractiveText' class representing chosen race. 'None' if no race is selected.
        selected_class: instance of 'InteractiveText' class representing chosen class. 'None' if no class is selected.
    RETURNS:
        available_choices: dict for instances of 'InteractiveText' for allowed race/class combinations.
    """
    # Dictionary for available race and class choices to be returned.
    available_choices: dict[str, list] = {
        "races": [],
        "classes": [],
    }

    for character in possible_characters:
        # Split each possible character to get race and class.
        race_name, class_name = character.split()

        # Add all available races and classes to dict if none are selected.
        if not selected_race and not selected_class:
            available_choices = race_class_check(available_choices, active_races, active_classes, race_name, class_name)

        # Add only classes that are compatible with selected race to dict.
        elif selected_race and selected_race.text == race_name:
            available_choices = race_class_check(available_choices, active_races, active_classes, race_name, class_name)

        # Add only races that are compatible with selected class to dict.
        elif selected_class and selected_class.text == class_name:
            available_choices = race_class_check(available_choices, active_races, active_classes, race_name, class_name)

    return available_choices


def get_position_race_class_element(screen, race_class: InteractiveText | TextField, inactive_elements: list[TextField],
                                    rc_dict: dict[str, list[str]]) -> tuple[int, int]:
    """Get and return x and y values for GUI elements in function 'draw_available_choices()'.
    ARGS:
        screen: PyGame window.
        race_class: GUI element to be positioned.
        inactive_elements: list of text field instances for non-choose able races/classes. Used here only to be passed
            to function 'get_race_class_y_position()' for further y-coordinates calculations.
        rc_dict: dict containing all available races/classes in the game as lists of strings.
    RETURNS:
        x, y: x and y position on screen for 'race_class' object.
    """
    # Race and class specific variables for x-positioning.
    race_x_pos: int = int(screen.get_rect().width / 4)
    class_x_pos: int = race_x_pos * 3
    # Lists of races and classes from dict 'rc_dict' for checks and calculation of y-positions.
    races_list: list[str] = rc_dict["races"]
    classes_list: list[str] = rc_dict["classes"]

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

    for index, item in enumerate(rc_dict_list):
        pos_y_start, pos_y_offset = set_elements_pos_y_values(screen, inactive_elements)
        if race_class.text == item:
            if index == 0:
                y = pos_y_start
            else:
                y = pos_y_start + pos_y_offset * index

    return y


def draw_available_choices(screen, rc_dict: dict[str, list[str]], available_choices: dict[str, list[InteractiveText]],
                           inactive_races: list[TextField], inactive_classes: list[TextField], mouse_pos) -> None:
    """Get position of text field items in dict 'available_choices' and draw them on screen.
    ARGS:
        screen: pygame window.
        rc_dict: dict containing all available races/classes in the game as lists of strings.
        available_choices: dict with instances of interactive text fields for race and class selection.
        inactive_races: list of text field instances for non-choose able races.
        inactive_classes: list of text field instances for non-choose able classes.
        mouse_pos: position of mouse on screen.
    """
    # Create list to check if inactive or selectable text field should be displayed.
    check_list: list[str] = [r.text for r in available_choices["races"]] + [c.text for c in available_choices["classes"]]

    # Draw race selection.
    for race in inactive_races:
        # Check if race.text attribute is in 'check_list', proceed with active UI object if so, inactive object otherwise.
        if race.text in check_list:
            for r in available_choices["races"]:
                r.interactive_rect.centerx, r.interactive_rect.centery = get_position_race_class_element(screen, r,
                                                                                                      inactive_races, rc_dict)
                r.draw_interactive_text(mouse_pos)
        else:
            race.text_rect.centerx, race.text_rect.centery = get_position_race_class_element(screen, race, inactive_races,
                                                                                          rc_dict)
            race.draw_text()

    # Draw class selection.
    for cls in inactive_classes:
        # Check if class.text attribute is in 'check_list', proceed with active UI object if so, inactive object otherwise.
        if cls.text in check_list:
            for c in available_choices["classes"]:
                c.interactive_rect.centerx, c.interactive_rect.centery = get_position_race_class_element(screen, c,
                                                                                                      inactive_classes, rc_dict)
                c.draw_interactive_text(mouse_pos)
        else:
            cls.text_rect.centerx, cls.text_rect.centery = get_position_race_class_element(screen, cls, inactive_classes,
                                                                                        rc_dict)
            cls.draw_text()


def select_race_class(gui_elements: dict, selected_race: InteractiveText | None, selected_class: InteractiveText | None,
                      reset_button: Button, mouse_pos) -> tuple[InteractiveText | None, InteractiveText | None]:
    """Selection logic for characters race and class and return selected text field instances in 'selected_race' and
    'selected class'.
    ARGS:
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
        selected_race: instance of 'InteractiveText' class representing chosen race. 'None' if no race is selected.
        selected_class: instance of 'InteractiveText' class representing chosen class. 'None' if no class is selected.
        reset_button: entry from gui element dict 'gui_elements["reset_button"]'.
        mouse_pos: position of mouse on screen.
    RETURNS:
        selected_race
        selected_class
    """
    # Assign entries from 'gui_elements' to variables.
    races: tuple[InteractiveText, ...] = gui_elements["active_races"]
    classes: tuple[InteractiveText, ...] = gui_elements["active_classes"]

    # Check if the left mouse button is pressed before proceeding with selection logic.
    if pygame.mouse.get_pressed()[0]:
        # Reset selected race/class if 'reset button' is clicked.
        if reset_button.button_rect.collidepoint(mouse_pos):
            if selected_race:
                selected_race.selected = False
                selected_race = None
            if selected_class:
                selected_class.selected = False
                selected_class = None
            for item in races + classes:
                item.selected = False

        # Loop through each available race and class option to see if any were clicked.
        for race in races:
            if race.text_rect.collidepoint(mouse_pos):
                selected_race = race
                break
        for cls in classes:
            if cls.text_rect.collidepoint(mouse_pos):
                selected_class = cls
                break

        if selected_race:
            # Unselect the previous selected race, if any.
            for race in races:
                if race.selected:
                    race.selected = False  # Set the selected attribute of the previously selected race to False.
            # Select the new race.
            selected_race.selected = True
        if selected_class:
            # Unselect the previous selected class, if any.
            for cls in classes:
                if cls.selected:
                    cls.selected = False  # Set the selected attribute of the previously selected class to False.
            # Select the new class.
            selected_class.selected = True

    return selected_race, selected_class


"""Background functions for spell selection screen."""

def position_spell_selection_screen_elements(screen, spells: tuple[InteractiveText, ...],
                                             screen_notes: tuple[TextField, ...]) -> None:
    """Position elements for spell selection on screen.
    ARGS:
        screen: pygame window.
        spells: tuple containing instances of class 'InteractiveText' representing available spells.
        screen_notes: tuple of 'TextField' instances showing notes for spell selection.
    """
    # Position notes at the screen bottom.
    for note in screen_notes:
        note.text_rect.centerx = screen.get_rect().centerx
    screen_notes[0].text_rect.bottom = screen.get_rect().bottom - screen.get_rect().height / 10
    screen_notes[1].text_rect.top = screen_notes[0].text_rect.bottom

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


def select_spell(spells: tuple[InteractiveText, ...], mouse_pos) -> None:
    """Selection logic for character's spell and return selected text field instances in 'selected_spell'.
    ARGS:
        spells: tuple with instances of interactive text fields for spell selection.
        mouse_pos: position of mouse on screen.
    RETURNS:
        selected_spell
    """
    # TEMPORARY VARIABLE FOR SELECTED SPELL.
    selected_spell = None

    # Create new tuple that excludes the first element. That element represents the default spell 'Read Magic', known by
    # all Magic-Users and cannot be selected/unselected.
    selectable_spells: tuple[InteractiveText, ...] = spells[1:]
    # Check if the left mouse button is pressed before proceeding with selection logic.
    if pygame.mouse.get_pressed()[0]:

        # Loop through each available spell option to see if any were clicked.
        for spell in selectable_spells:
            if spell.text_rect.collidepoint(mouse_pos):
                selected_spell = spell
                break

        if selected_spell:
            # Unselect the previous selected spell, if any.
            for spell in selectable_spells:
                if spell.selected:
                    spell.selected = False  # Set the selected attribute of the previously selected spell to False.
            # Select the new spell.
            selected_spell.selected = True


def draw_spell_selection_screen_elements(screen, spells: tuple[InteractiveText, ...], screen_notes: tuple[TextField, ...],
                                         mouse_pos) -> None:
    """Call positioning method 'position_spell_selection_screen_elements()' and draw item from tuple 'spells' on screen.
    ARGS:
        screen: pygame window.
        spells: tuple containing instances of class 'InteractiveText' representing available spells.
        screen_notes: tuple of 'TextField' instances showing notes for spell selection.
        mouse_pos: position of mouse on screen.
    """
    # Position elements on screen.
    position_spell_selection_screen_elements(screen, spells, screen_notes)
    # Draw elements from 'spells'.
    for spell in spells:
        spell.draw_interactive_text(mouse_pos)

    # Draw further elements on screen.
    for note in screen_notes:
        note.draw_text()


"""Background functions for character naming screen."""

def build_and_position_prompt(screen, naming_prompt: TextField, character: object) -> None:
    """Create text for 'TextField' instance 'naming_prompt' to include character's race and class, and position it on
    screen.
    ARGS:
        screen: PyGame window.
        naming_prompt: instance of 'TextField' class prompting the user to input a character name.
        character: instance of 'Character' class.
    """
    if not sd.position_flag:
        # Add naming prompt to 'naming_prompt.text' attribute and render text_rect.
        naming_prompt.text = f"Name your {character.race_name} {character.class_name}"
        naming_prompt.text_surface = naming_prompt.font.render(naming_prompt.text, True, naming_prompt.text_color)
        naming_prompt.text_rect = naming_prompt.text_surface.get_rect()

        # Position final naming prompt on screen.
        naming_prompt.text_rect.centerx, naming_prompt.text_rect.centery = screen.get_rect().centerx, screen.get_rect().centery / 1.3

        sd.position_flag = True


"""Background functions for starting money screen."""

def position_money_screen_elements(screen, gui_elements: dict) -> None:
    """Position objects from 'gui_elements' for starting money screen.
    ARGS:
        screen: PyGame window.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
    """
    if not sd.position_flag:
        # Positioning of button instances.
        money_button_pos_y: int = screen.get_rect().height / 3
        random_money_button, custom_money_button = gui_elements["starting_money_choices"][0], gui_elements["starting_money_choices"][1]
        random_money_button.button_rect.top, random_money_button.button_rect.centerx = money_button_pos_y, screen.get_rect().centerx * 0.5
        custom_money_button.button_rect.top, custom_money_button.button_rect.centerx = money_button_pos_y, screen.get_rect().centerx * 1.5

        # Positioning of text input and text field instances.
        rolling_dice_money_field, random_money_field = gui_elements["random_money"][0], gui_elements["random_money"][1]
        rolling_dice_money_field.text_rect.centery, random_money_field.text_rect.centery = (screen.get_rect().centery * 1.1,
                                                                                            screen.get_rect().centery * 1.1)
        money_input_prompt: TextField = gui_elements["money_amount_input"][2]
        money_input_prompt.text_rect.centery = screen.get_rect().centery * 1.05
        money_amount_field: TextInputField = gui_elements["money_amount_input"][1]
        money_amount_field.input_bg_field.top = screen.get_rect().centery * 1.15

        sd.position_flag = True


def choose_money_option(choices: list[Button], random_money_flag: bool, custom_money_flag: bool, mouse_pos) -> tuple[bool, bool]:
    """Choose option to either generate random amount of money or let user input a custom amount, return 'starting_money'
    if random amount is chosen, set and return 'random_money_flag'/'custom_money_flag' accordingly.
    ARGS:
        choices: List of instances of 'Button' class from dict 'gui_elements'.
        random_money_flag: flag to indicate if randomly generated amount of money is chosen.
        custom_money_flag: flag to indicate if custom amount of money is chosen.
        mouse_pos: position of mouse on screen.
    RETURNS:
        random_money_flag
        custom_money_flag
    """
    if pygame.mouse.get_pressed()[0]:
        # Set flags to appropriate values based chosen option.
        if choices[0].button_rect.collidepoint(mouse_pos):
            random_money_flag, custom_money_flag = True, False
            # Set dice roll timer.
            sd.dice_roll_start_time = time.time()
        if choices[1].button_rect.collidepoint(mouse_pos):
            random_money_flag, custom_money_flag = False, True

    return random_money_flag, custom_money_flag


def draw_chosen_money_option(screen, starting_money: int, random_money_flag: bool, custom_money_flag: bool,
                             gui_elements: dict) -> int:
    """Draw message for random amount of starting money or show input field for custom amount on screen.
    ARGS:
        screen: PyGame window.
        starting_money: amount of starting money. Default value is '0'.
        random_money_flag: flag to indicate if randomly generated amount of money is chosen.
        custom_money_flag: flag to indicate if custom amount of money is chosen.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
    """
    # Set duration for dice roll in seconds.
    dice_roll_duration: int | float = 1

    # Assign font size and text field instances from dict 'gui_elements' to variables.
    text_large: int = gui_elements["text_large"]
    # Random money fields.
    rolling_dice_money_field, random_money_field = gui_elements["random_money"][0], gui_elements["random_money"][1]
    # Money input fields.
    money_amount_field: TextInputField = gui_elements["money_amount_input"][1]
    money_input_prompt: TextField = gui_elements["money_amount_input"][2]

    if random_money_flag:
        # Check timer to allow for dice roll effect.
        if time.time() - sd.dice_roll_start_time < dice_roll_duration:
            rolling_dice_money_field.draw_text()
            # Generate random int value for 'starting_money'.
            starting_money = roll_starting_money()
            starting_money_dice_roll(screen, starting_money, random_money_field, text_large)
        # Show final value after timer runs out.
        else:
            random_money_field.draw_text()
            starting_money_dice_roll(screen, starting_money, random_money_field, text_large, rolling=False)
            # Reset global dice roll timer. Not strictly necessary, but better safe than sorry.
            sd.dice_roll_start_time = 0
    elif custom_money_flag:
        money_input_prompt.draw_text()
        money_amount_field.draw_input_field()

    return starting_money


def starting_money_dice_roll(screen, starting_money: int, random_money_field: TextField, text_large: object | int,
                             rolling: bool = True) -> None:
    """Display the rolling or final amount of starting money on screen.
    ARGS:
        screen: PyGame window.
        starting_money: amount of starting money to display.
        random_money_field: reference text field to position the money display correctly.
        text_large: font size instance for text rendering. Usually 'gui_elements["text_large"]' is used, but any 'int'
            can be passed.
        rolling: boolean flag to indicate if the dice roll is still ongoing.
            If 'True', displays a "rolling" message. If 'False', shows the final amount. Default is 'True'.
    """
    # Check if "rolling" message or final amount should be displayed.
    if rolling:
        # Build string 'starting_money_message' for use as argument in TextField instance 'random_money_result_field'.
        starting_money_message: str = str(starting_money)
    else:
        # Build string 'starting_money_message' for use as argument in TextField instance 'random_money_result_field'.
        starting_money_message: str = str(starting_money) + " gold pieces"

    # Create TextField instance 'random_money_result_field', and position and draw it on screen.
    random_money_result_field = so.TextField(screen, starting_money_message, text_large)
    random_money_result_field.text_rect.top = random_money_field.text_rect.bottom
    random_money_result_field.draw_text()


"""Background functions for creation complete screen."""

def position_completion_screen_elements(screen, completion_message: TextField, show_character_sheet: Button,
                                        gui_elements: dict) -> None:
    """Position screen elements for 'character complete' screen.
    ARGS:
        screen: PyGame window.
        completion_message: instance of class 'TextField' showing completion message.
        show_character_sheet: instance of class 'Button' to proceed to character sheet.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
    """
    # Assign spacing value from 'gui_elements' to variables.
    spacing: int = gui_elements["title_screen_spacing"]

    if not sd.position_flag:
        # Position screen elements.
        completion_message.text_rect.bottom = screen.get_rect().centery - spacing
        show_character_sheet.button_rect.top = screen.get_rect().centery + spacing
        show_character_sheet.button_rect.centerx = screen.get_rect().centerx

        sd.position_flag = True
