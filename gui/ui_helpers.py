import pygame
"""Background functions for GUI, i.e. value build/retrieval and object positioning functions for pygame screens."""


"""General functions."""

def draw_screen_title(screen, screen_title, gui_elements):
    """Draw 'screen_title' object on screen at default position."""
    screen_title.text_rect.top = screen.get_rect().top + gui_elements["default_edge_spacing"]
    screen_title.text_rect.centerx = screen.get_rect().centerx
    screen_title.draw_text()


def draw_special_button(screen, button, gui_elements, mouse_pos):
    """Draw special button (i.e. 'Roll Again' or 'Reset') at the bottom center of the screen."""
    button.button_rect.width = gui_elements["default_button_width"]
    button.button_rect.centerx = screen.get_rect().centerx
    button.button_rect.bottom = screen.get_rect().bottom - gui_elements["default_edge_spacing"]
    button.draw_button(mouse_pos)


"""Background functions for race/class selection screen."""

def race_class_check(available_choices, possible_races, possible_classes, race_name, class_name):
    """Check 'possible_races' and 'possible_classes' and populate and return dict 'available_choices' with allowed
    race/class combinations for use in function 'get_available_choices()'."""
    # Check if the race matches.
    for race in possible_races:
        if race.text == race_name:
            # Assuring only one instance of each object is added to dict.
            if race not in available_choices["races"]:
                available_choices["races"].append(race)
    # Check if the class matches.
    for cls in possible_classes:
        if cls.text == class_name:
            # Assuring only one instance of each object is added to dict.
            if cls not in available_choices["classes"]:
                available_choices["classes"].append(cls)

    return available_choices


def get_available_choices(possible_characters, possible_races, possible_classes, selected_race, selected_class):
    """Create dict and populate it with instances from 'possible_races' and 'possible_classes' using function
        'race_class_check()' if their 'text' attributes match entries in 'possible_characters' (first word for race,
        second for class) and return it in 'available_choices'.
    ARGS:
        possible_characters: list of possible race-class combinations as strings.
        possible_races: entry from gui element dict 'gui_elements["possible_races"]'.
        possible_classes: entry from gui element dict 'gui_elements["possible_classes"]'.
        selected_race: instance of 'InteractiveText' class representing chosen race.
        selected_class: instance of 'InteractiveText' class representing chosen class.
    """
    # Dictionary for available race and class choices to be returned.
    available_choices = {
        "races": [],
        "classes": [],
    }

    for character in possible_characters:
        # Split each possible character to get race and class.
        race_name, class_name = character.split()

        # Add all available races and classes to dict if none are selected.
        if not selected_race and not selected_class:
            available_choices = race_class_check(available_choices, possible_races, possible_classes, race_name, class_name)

        # Add only classes that are compatible with selected race to dict.
        elif selected_race and selected_race.text == race_name:
            available_choices = race_class_check(available_choices, possible_races, possible_classes, race_name, class_name)

        # Add only races that are compatible with selected class to dict.
        elif selected_class and selected_class.text == class_name:
            available_choices = race_class_check(available_choices, possible_races, possible_classes, race_name, class_name)

    return available_choices


def position_race_class_elements(screen, race_class, inactive_races):
    """Get and return x and y values for GUI elements in function 'draw_available_choices()'.
    ARGS:
        screen: pygame window.
        race_class: string variable for race or class check.
        inactive_races: list of text field instances for non-choose able races. Only used here to calculate value for
        variable 'text_field_height'.
    """
    # General variables for element positioning.
    screen_center_y = screen.get_rect().centery
    text_field_height = inactive_races[0].text_rect.height  # Value taken from list item for consistent field height.
    text_field_y_offset = text_field_height * 2
    race_field_block_height = 4 * text_field_height
    race_field_centerx = int(screen.get_rect().width / 4)
    race_field_centery_start = screen_center_y - race_field_block_height
    class_field_block_height = 6 * text_field_height
    class_field_centerx = race_field_centerx * 3
    class_field_centery_start = screen_center_y - class_field_block_height

    # Text field positions.
    # Races.
    human_pos_x, human_pos_y = race_field_centerx, race_field_centery_start
    elf_pos_x, elf_pos_y = race_field_centerx, human_pos_y + text_field_y_offset
    dwarf_pos_x, dwarf_pos_y = race_field_centerx, elf_pos_y + text_field_y_offset
    halfling_pos_x, halfling_pos_y = race_field_centerx, dwarf_pos_y + text_field_y_offset
    # Classes.
    fighter_pos_x, fighter_pos_y = class_field_centerx, class_field_centery_start
    cleric_pos_x, cleric_pos_y = class_field_centerx, fighter_pos_y + text_field_y_offset
    magic_user_pos_x, magic_user_pos_y = class_field_centerx, cleric_pos_y + text_field_y_offset
    thief_pos_x, thief_pos_y = class_field_centerx, magic_user_pos_y + text_field_y_offset
    fighter_magic_user_pos_x, fighter_magic_user_pos_y = class_field_centerx, thief_pos_y + text_field_y_offset
    magic_user_thief_pos_x, magic_user_thief_pos_y = class_field_centerx, fighter_magic_user_pos_y + text_field_y_offset

    # Check 'race_class' and assign correct x and y value for each specific race/class.
    if race_class.text == "Human":
        x, y = human_pos_x, human_pos_y
    elif race_class.text == "Elf":
        x, y = elf_pos_x, elf_pos_y
    elif race_class.text == "Dwarf":
        x, y = dwarf_pos_x, dwarf_pos_y
    elif race_class.text == "Halfling":
        x, y = halfling_pos_x, halfling_pos_y
    elif race_class.text == "Fighter":
        x, y = fighter_pos_x, fighter_pos_y
    elif race_class.text == "Cleric":
        x, y = cleric_pos_x, cleric_pos_y
    elif race_class.text == "Magic-User":
        x, y = magic_user_pos_x, magic_user_pos_y
    elif race_class.text == "Thief":
        x, y = thief_pos_x, thief_pos_y
    elif race_class.text == "Fighter/Magic-User":
        x, y = fighter_magic_user_pos_x, fighter_magic_user_pos_y
    elif race_class.text == "Magic-User/Thief":
        x, y = magic_user_thief_pos_x, magic_user_thief_pos_y

    return x, y


def draw_available_choices(screen, available_choices, inactive_races, inactive_classes, mouse_pos):
    """Get position of text field items in dict 'available_choices' and draw them on screen.
    ARGS:
        screen: pygame window.
        available_choices: dict with instances of interactive text fields for race and class selection.
        inactive_races: list of text field instances for non-choose able races.
        inactive_classes: list of text field instances for non-choose able classes.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """

    # Create list to check if inactive or selectable text field should be displayed.
    check_list = []
    for r in available_choices["races"]:
        check_list.append(r.text)
    for c in available_choices["classes"]:
        check_list.append(c.text)

    # Draw race selection.
    for race in inactive_races:
        if race.text in check_list:
            for r in available_choices["races"]:
                r.text_rect.centerx, r.text_rect.centery = position_race_class_elements(screen, r, inactive_races)
                r.draw_interactive_text(mouse_pos)
        else:
            race.text_rect.centerx, race.text_rect.centery = position_race_class_elements(screen, race, inactive_races)
            race.draw_text()

    # Draw class selection.
    for cls in inactive_classes:
        if cls.text in check_list:
            for c in available_choices["classes"]:
                c.text_rect.centerx, c.text_rect.centery = position_race_class_elements(screen, c, inactive_races)
                c.draw_interactive_text(mouse_pos)
        else:
            cls.text_rect.centerx, cls.text_rect.centery = position_race_class_elements(screen, cls, inactive_races)
            cls.draw_text()


def select_race_class(available_choices, selected_race, selected_class, reset_button, mouse_pos):
    """Selection logic for characters race and class and return selected text field instances in 'selected_race' and
    selected class.
    ARGS:
        available_choices: dict with instances of interactive text fields for race and class selection.
        selected_race: instance of 'InteractiveText' class representing chosen race.
        selected_class: instance of 'InteractiveText' class representing chosen class.
        reset_button: entry from gui element dict 'gui_elements["reset_button"]'.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
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

        # Loop through each available race and class option to see if any were clicked.
        for race in available_choices["races"]:
            if race.text_rect.collidepoint(mouse_pos):
                selected_race = race
                break
        for cls in available_choices["classes"]:
            if cls.text_rect.collidepoint(mouse_pos):
                selected_class = cls
                break

        if selected_race:
            # Unselect the previous selected race, if any.
            for race in available_choices["races"]:
                if race.selected:
                    race.selected = False  # Set the selected attribute of the previously selected race to False.
            # Select the new race.
            selected_race.selected = True
        if selected_class:
            # Unselect the previous selected class, if any.
            for cls in available_choices["classes"]:
                if cls.selected:
                    cls.selected = False  # Set the selected attribute of the previously selected class to False.
            # Select the new class.
            selected_class.selected = True

    return selected_race, selected_class


"""Background functions for starting money screen."""

def position_money_screen_elements(screen, gui_elements):
    """Position and draw objects from 'gui_elements' for starting money screen."""
    # Positioning of button instances.
    gold_button_width = screen.get_rect().width / 3
    gold_button_pos_y = screen.get_rect().height / 3
    random_gold_button, custom_gold_button = gui_elements["starting_money_choices"][0], gui_elements["starting_money_choices"][1]
    random_gold_button.button_rect.width = gold_button_width
    custom_gold_button.button_rect.width = gold_button_width
    random_gold_button.button_rect.top, random_gold_button.button_rect.centerx = gold_button_pos_y, screen.get_rect().centerx * 0.5
    custom_gold_button.button_rect.top, custom_gold_button.button_rect.centerx = gold_button_pos_y, screen.get_rect().centerx * 1.5

    # Positioning of text input and text field instances.
    money_input_prompt = gui_elements["money_amount_input"][2]
    money_input_prompt.text_rect.centery = screen.get_rect().centery * 1.1
    money_amount_field = gui_elements["money_amount_input"][1]
    money_amount_field.input_bg_field.top = screen.get_rect().centery * 1.15
