import pygame
from core.functions import set_starting_money
import gui.screen_objects as so
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


def draw_continue_button_inactive(condition_1, condition_2, gui_elements, mouse_pos, check_mode="any"):
    """Draw either active or inactive instance of continue button from module 'gui_elements'.
    ARGS:
        condition_1: first condition to be checked.
        condition_2: second condition to be checked.
        gui_elements: dict containing gui element instances.
        mouse_pos: mouse position on screen.
        check_mode: Determines whether one or both conditions must be met. Use 'any' to require at least one condition,
                    or 'all' to require both. Default is 'any'.
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


def render_new_text_image(element):
    """Re-render 'text_image' attribute from instance of class 'TextField' and get new 'text_rect'. This function is for
    use after an already created instance has its 'text' attribute changed to ensure further changes to, for example,
    its position are applied to the modified instance."""

    # Check if element has 'multi_line' attribute set to 'True' and render 'text_image' accordingly, using class method
    # '.render_multiline_image()' if element is multi line normal render method otherwise.
    if element.multi_line:
        element.text_image = element.render_multiline_image()
    else:
        element.text_image = element.font.render(element.text, True, element.text_color)

    element.text_rect = element.text_image.get_rect()


"""Background functions for title screen."""

def position_title_screen_elements(screen, gui_elements):
    """Position objects from 'gui_elements' for title screen."""
    # Assign gui_elements to variables.
    spacing = gui_elements["title_screen_spacing"]
    title = gui_elements["title"]
    subtitle = gui_elements["subtitle"]
    copyright_notice = gui_elements["copyright_notice"]

    # Position title, subtitle and copyright notice.
    title.text_rect.centerx = screen.get_rect().centerx
    title.text_rect.bottom = screen.get_rect().centery - spacing
    subtitle.text_rect.centerx = screen.get_rect().centerx
    subtitle.text_rect.top = screen.get_rect().centery + spacing
    copyright_notice.text_rect.centerx = screen.get_rect().centerx
    copyright_notice.text_rect.bottom = screen.get_rect().bottom - spacing


"""Background functions for main menu screen."""

def position_main_menu_screen_elements(screen, gui_elements):
    """Position objects from 'gui_elements' for main menu screen."""
    # Assign gui_elements to variables.
    spacing = gui_elements["title_screen_spacing"]
    title = gui_elements["main_menu_title"]
    start = gui_elements["start_button"]
    settings = gui_elements["settings_button"]
    show_credits = gui_elements["credits_button"]

    # Position buttons and title text field.
    title.text_rect.centery = screen.get_rect().height / 3
    title.text_rect.centerx = screen.get_rect().centerx
    start.button_rect.width = screen.get_rect().width / 3
    start.button_rect.centerx = screen.get_rect().centerx
    start.button_rect.bottom = screen.get_rect().centery - spacing
    settings.button_rect.width = screen.get_rect().width / 6
    settings.button_rect.centerx = screen.get_rect().centerx
    settings.button_rect.top = screen.get_rect().centery + spacing * 2
    show_credits.button_rect.width = screen.get_rect().width / 6
    show_credits.button_rect.centerx = screen.get_rect().centerx
    show_credits.button_rect.top = settings.button_rect.bottom


"""Background functions for character menu screen."""

def position_character_menu_screen_elements(screen, gui_elements):
    """Position objects from 'gui_elements' for character menu screen."""
    # Assign gui_elements to variables.
    custom = gui_elements["custom"]
    random = gui_elements["random"]

    # Position buttons.
    custom.button_rect.width = screen.get_rect().width / 3
    custom.button_rect.centerx = screen.get_rect().centerx
    custom.button_rect.bottom = screen.get_rect().centery
    random.button_rect.width = screen.get_rect().width / 3
    random.button_rect.centerx = screen.get_rect().centerx
    random.button_rect.top = screen.get_rect().centery


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
    'selected class'.
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


"""Background functions for character naming screen."""

def build_and_position_prompt(screen, naming_prompt, character):
    """Create text for 'TextField' instance 'naming_prompt' to include characters race and class, and position it on
    screen.
    ARGS:
        screen: pygame window.
        naming_prompt: instance of 'TextField' class prompting the user to input a character name.
        character: instance of 'Character' class.
    """

    # Add naming prompt to 'naming_prompt.text' attribute and render text_rect.
    naming_prompt.text = f"Name your {character.race_name} {character.class_name}"
    naming_prompt.text_image = naming_prompt.font.render(naming_prompt.text, True, naming_prompt.text_color)
    naming_prompt.text_rect = naming_prompt.text_image.get_rect()

    # Position final naming prompt on screen.
    naming_prompt.text_rect.centerx, naming_prompt.text_rect.centery = screen.get_rect().centerx, screen.get_rect().centery / 1.15


"""Background functions for starting money screen."""

def position_money_screen_elements(screen, gui_elements):
    """Position objects from 'gui_elements' for starting money screen."""
    # Positioning of button instances.
    money_button_width = screen.get_rect().width / 2.5
    money_button_pos_y = screen.get_rect().height / 3
    random_money_button, custom_money_button = gui_elements["starting_money_choices"][0], gui_elements["starting_money_choices"][1]
    random_money_button.button_rect.width = money_button_width
    custom_money_button.button_rect.width = money_button_width
    random_money_button.button_rect.top, random_money_button.button_rect.centerx = money_button_pos_y, screen.get_rect().centerx * 0.5
    custom_money_button.button_rect.top, custom_money_button.button_rect.centerx = money_button_pos_y, screen.get_rect().centerx * 1.5

    # Positioning of text input and text field instances.
    random_money_field = gui_elements["random_money"]
    random_money_field.text_rect.centery = screen.get_rect().centery * 1.1
    money_input_prompt = gui_elements["money_amount_input"][2]
    money_input_prompt.text_rect.centery = screen.get_rect().centery * 1.1
    money_amount_field = gui_elements["money_amount_input"][1]
    money_amount_field.input_bg_field.top = screen.get_rect().centery * 1.15


def choose_money_option(choices, starting_money, random_money_flag, custom_money_flag, mouse_pos):
    """Choose option to either generate random amount of money or let user input a custom amount, return 'starting_money'
    if random amount is chosen, set and return 'random_money_flag'/'custom_money_flag' accordingly.
    ARGS:
        choices: List of instances of 'Button' class from dict 'gui_elements'.
        starting_money: amount of starting money. Starting value is 'None', changes if 'random_money_flag' is 'True'
        random_money_flag: flag to indicate if randomly generated amount of money is chosen.
        custom_money_flag: flag to indicate if custom amount of money is chosen.
        mouse_pos: position of mouse on screen.
    """

    if pygame.mouse.get_pressed()[0]:
        # Set flags to appropriate values based chosen option.
        if choices[0].button_rect.collidepoint(mouse_pos):
            random_money_flag, custom_money_flag = True, False
            # Generate int value for 'starting_money' if random amount is chosen.
            starting_money = set_starting_money()
        if choices[1].button_rect.collidepoint(mouse_pos):
            random_money_flag, custom_money_flag = False, True

    return starting_money, random_money_flag, custom_money_flag


def draw_chosen_money_option(screen, starting_money, random_money_flag, custom_money_flag, gui_elements):
    """Draw message for random amount of starting money or show input field for custom amount on screen.
    ARGS:
        screen: Pygame window.
        starting_money: amount of starting money. Starting value is 'None', changes if 'random_money_flag' is 'True'
        random_money_flag: flag to indicate if randomly generated amount of money is chosen.
        custom_money_flag: flag to indicate if custom amount of money is chosen.
        gui_elements: dict containing gui element instances.
    """
    # Assign font size and text field instances from dict 'gui_elements' to variables.
    text_large = gui_elements["text_large"]
    random_money_field = gui_elements["random_money"]
    money_amount_field, money_input_prompt = gui_elements["money_amount_input"][1], gui_elements["money_amount_input"][2]

    if random_money_flag:
        random_money_field.draw_text()
        # Build string 'starting_money_message' for use as argument in TextField instance 'random_money_result_field'.
        starting_money_message = str(starting_money) + " gold pieces"
        # Create TextField instance 'random_money_result_field', and position and draw it on screen.
        random_money_result_field = so.TextField(screen, starting_money_message, text_large)
        random_money_result_field.text_rect.top = random_money_field.text_rect.bottom
        random_money_result_field.draw_text()
    elif custom_money_flag:
        money_input_prompt.draw_text()
        money_amount_field.draw_input_field()


"""Background functions for creation complete screen."""

def position_completion_screen_elements(screen, completion_message, show_character_sheet, gui_elements):
    """Position screen elements for 'character complete' screen.
    ARGS:
        screen: pygame window.
        completion_message: instance of class 'TextField' showing completion message.
        show_character_sheet: instance of class 'Button' to proceed to character sheet.
        gui_elements: dict containing gui element instances.
    """
    # Assign spacing value from 'gui_elements' to variables.
    spacing = gui_elements["title_screen_spacing"]

    # Position screen elements.
    completion_message.text_rect.bottom = screen.get_rect().centery - spacing
    show_character_sheet.button_rect.top = screen.get_rect().centery + spacing
    show_character_sheet.button_rect.centerx = screen.get_rect().centerx
