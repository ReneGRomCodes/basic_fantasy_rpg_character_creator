import pygame
from core.rules import set_starting_money
import gui.screen_objects as so
from gui.gui_elements import initialize_screen_elements
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
    """Format and position objects from 'gui_elements' for main menu screen."""
    # Assign gui_elements to variables.
    spacing = gui_elements["title_screen_spacing"]
    title = gui_elements["main_menu_title"]
    start = gui_elements["start_button"]
    menu_buttons = gui_elements["menu_buttons"]

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
            button.button_rect.top = menu_buttons[index - 1].button_rect.bottom


"""Background functions for settings screen."""

def format_settings_screen_elements(screen, gui_elements):
    """Format and position objects from 'gui_elements' for settings screen."""
    # Assign elements to variables.
    window_size_field = gui_elements["window_size"]
    window_size_buttons = gui_elements["window_size_buttons"]
    spacing = gui_elements["default_edge_spacing"]
    screen_x = screen.get_rect().centerx
    screen_y = screen.get_rect().centery
    # Assign anchor object 'window_size_buttons[0].interactive_rect' (small window) and further options to variables for
    # easier positioning and better readability.
    window_size_anchor = window_size_buttons[0].interactive_rect
    window_size_medium = window_size_buttons[1].interactive_rect
    window_size_large = window_size_buttons[2].interactive_rect
    window_size_full = window_size_buttons[3].interactive_rect

    # Set button size.
    for button in window_size_buttons:
        button.interactive_rect.width, button.interactive_rect.height = screen.get_rect().width / 8, screen.get_rect().height  / 12

    # Position window size section label.
    window_size_field.text_rect.centery = screen_y
    window_size_field.text_rect.right = screen_x - spacing
    # Position selection fields for window sizes. 'window_size_anchor' is placed first as anchor for positioning
    # of further buttons. To move the entire block only the anchor has to be moved.
    window_size_anchor.left, window_size_anchor.bottom = screen_x + spacing, screen_y - spacing / 2
    window_size_medium.left, window_size_medium.bottom = window_size_anchor.right + spacing, window_size_anchor.bottom
    window_size_large.left, window_size_large.top = window_size_anchor.left, window_size_anchor.bottom + spacing
    window_size_full.left, window_size_full.top = window_size_anchor.right + spacing, window_size_anchor.bottom + spacing


def select_window_size(screen, settings, gui_elements, window_size_buttons, selected_window_size, mouse_pos):
    """Selection logic for programs window size and return selected text field instances in 'selected_window_size'.
    ARGS:
        screen: PyGame window.
        settings: instance of class 'Settings'.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
        window_size_buttons: list with instances of interactive text fields for window size selection.
        selected_window_size: instance of 'InteractiveText' class representing chosen window size.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        Re-initialized dict 'gui_elements'.
        Instance of newly selected window size to appear as selected on screen.
    """
    # Tuple to store window size UI objects and corresponding 'settings' attributes. Last item represents full screen,
    # and has no settings attribute assigned, instead using 'pygame.FULLSCREEN' when setting window size.
    object_attribute_pairs = ((window_size_buttons[0], settings.small_screen), (window_size_buttons[1], settings.medium_screen),
                              (window_size_buttons[2], settings.large_screen), (window_size_buttons[3], False))

    # Set 'window_sizes[0].selected' to 'True' to show default selection in settings menu when screen is first shown.
    if settings.screen_size == settings.default_settings[0]:
        window_size_buttons[0].selected = True

    # Assign default object (small window) to 'selected_window_size' if it is 'None' in case of first access to the
    # settings screen.
    if not selected_window_size:
        selected_window_size = object_attribute_pairs[0][0]

    # Check if the left mouse button is pressed before proceeding with selection logic.
    if pygame.mouse.get_pressed()[0]:
        # Loop through each available window size option to see which one is selected.
        for size in window_size_buttons:
            if size.interactive_rect.collidepoint(mouse_pos):
                selected_window_size = size
                break

    # Iterate through 'object_attribute_pairs' and check if currently selected UI object corresponds with window size set
    # in 'Settings' object. Change 'settings.screen_size' and change 'pygame.display' to selected value if pairs don't
    # correspond.
    for pair in object_attribute_pairs:

        if pair[0].selected == True and pair[1] != settings.screen_size:
            settings.screen_size = pair[1]
            # Check if 'pair[1]' has a window size assigned, otherwise set window to full screen.
            if pair[1]:
                pygame.display.set_mode(settings.screen_size)
            else:
                pygame.display.set_mode((0,0), pygame.FULLSCREEN)
            # Wait 200ms to avoid immediate click registration directly after new window size is set. Window could be
            # accidentally changed again otherwise.
            pygame.time.wait(200)

            # Re-initialize dict 'gui_elements' for proper size and positions of gui objects based on screen size.
            gui_elements = initialize_screen_elements(screen, settings)

        # Re-assign window size to 'selected_window_size' by comparing 'text' attributes with 'pair[0]', replacing
        # 'selected_window_size' with equivalent object and set its attribute to 'True'. Re-initialization of dict
        # 'gui_elements' above leads to 'selected_window_size' pointing to obsolete object otherwise.
        if selected_window_size.text == pair[0].text:
            selected_window_size = pair[0]
            selected_window_size.selected = True

    return gui_elements, selected_window_size


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



"""Background functions for ability scores screen."""

def position_ability_scores_screen_elements(screen, abilities_array, mouse_pos):
    """Position and draw objects for ability scores screen. 'abilities_array' stores ability objects in function
    'show_ability_scores_screen()'."""

    # Create instances of class 'TextField' to show ability scores and bonus/penalty on screen. Text string is placeholder
    # and text size is 'field_text_size' as retrieved from first 'gui_elements' entry in 'abilities_array' to ensure
    # correct scaling. Placeholder text is dynamically changed for each ability in for-loop further down.
    field_text_size = abilities_array[0][0].size
    ability_score_text = so.TextField(screen, "score", field_text_size)
    bonus_penalty_text = so.TextField(screen, "bonus_penalty", field_text_size)


    # Set reference variables for adaptive positioning.
    screen_center_y = screen.get_rect().height / 2
    n_abilities = len(abilities_array)

    # Find item in, or after, the middle position in 'abilities_array' as reference object for further positioning.
    if n_abilities % 2 == 0:
        # Even number of elements in 'abilities_array'.
        center_object_index = int(n_abilities / 2)
        abilities_array[center_object_index][0].text_rect.top = screen_center_y
    else:
        # Odd number of elements in 'abilities_array'.
        center_object_index = n_abilities // 2
        abilities_array[center_object_index][0].text_rect.centery = screen_center_y

    # Draw line on screens center-y for test and reference. REMOVE LATER!!!
    pygame.draw.line(screen, (0,0,0), (0, screen_center_y), (500, screen_center_y))

    # Set initial position on y-axis for ability score fields and offset value for spacing between elements.
    element_position_offset = ability_score_text.text_rect.height * 2
    element_pos_y = abilities_array[center_object_index][0].text_rect.top - (int(n_abilities / 2) * element_position_offset)


    # Loop through each ability field (as they are grouped in 'abilities_array') and corresponding stats to format,
    # position and display the ability name, score and bonus/penalty as they are grouped in 'abilities_array'.
    for ability_ui, ability_attribute in abilities_array:
        # 'Pre-formatting' bonus/penalty to string for easier formatting and better code-readability further down.
        bonus_penalty = f"{ability_attribute[1]}"

        # Check bonus/penalty for positive or negative value to apply correct prefix in text field or give out an empty
        # string if bonus_penalty is 0.
        if ability_attribute[1] > 0:
            bonus_penalty = f"+{bonus_penalty}"
        elif ability_attribute[1] == 0:
            bonus_penalty = ""

        # Position and draw copied rect for item from list 'abilities'.
        ability_rect = ability_ui.interactive_rect.copy()
        ability_rect.top = element_pos_y
        ability_rect.width = screen.get_rect().width / 6
        ability_rect.right = screen.get_rect().centerx
        # Position ability rect within copied rect for left-alignment.
        ability_ui.interactive_rect.topleft = ability_rect.topleft
        ability_ui.draw_interactive_text(mouse_pos)

        # Change contents and get rect of 'TextField' instances for each ability score stat.
        ability_score_text.text = str(ability_attribute[0])
        ability_score_text.render_new_text_image()
        bonus_penalty_text.text = bonus_penalty
        bonus_penalty_text.render_new_text_image()

        # Position and draw copied rects for each stat and bonus/penalty field.
        ability_score_rect = ability_score_text.text_rect.copy()
        ability_score_rect.width = screen.get_rect().width / 12
        ability_score_rect.topleft = ability_rect.topright
        bonus_penalty_rect = bonus_penalty_text.text_rect.copy()
        bonus_penalty_rect.width = screen.get_rect().width / 12
        bonus_penalty_rect.topleft = ability_score_rect.topright
        # Position stat and bonus/penalty rects within copied rects for right-alignment.
        ability_score_text.text_rect.topright = ability_score_rect.topright
        bonus_penalty_text.text_rect.topright = bonus_penalty_rect.topright

        ability_score_text.draw_text()
        bonus_penalty_text.draw_text()

        element_pos_y += element_position_offset


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
                r.interactive_rect.centerx, r.interactive_rect.centery = position_race_class_elements(screen, r, inactive_races)
                r.draw_interactive_text(mouse_pos)
        else:
            race.text_rect.centerx, race.text_rect.centery = position_race_class_elements(screen, race, inactive_races)
            race.draw_text()

    # Draw class selection.
    for cls in inactive_classes:
        if cls.text in check_list:
            for c in available_choices["classes"]:
                c.interactive_rect.centerx, c.interactive_rect.centery = position_race_class_elements(screen, c, inactive_races)
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
