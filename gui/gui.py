import gui.ui_helpers as ui

"""Main GUI functions."""


def show_title_screen(screen, gui_elements):
    """Show title screen."""
    # Assign gui_elements to variables.
    title = gui_elements["title"]
    subtitle = gui_elements["subtitle"]
    copyright_notice = gui_elements["copyright_notice"]

    # Position title, subtitle and copyright notice.
    ui.position_title_screen_elements(screen, gui_elements)

    # Draw elements on screen.
    title.draw_text()
    subtitle.draw_text()
    copyright_notice.draw_text()


def show_main_menu(screen, gui_elements, mouse_pos):
    """Display main menu."""
    # Assign gui_elements to variables.
    title = gui_elements["main_menu_title"]
    start = gui_elements["start_button"]
    menu_buttons = gui_elements["menu_buttons"]

    # Position buttons and main menu title field.
    ui.position_main_menu_screen_elements(screen, gui_elements)

    # Draw elements on screen.
    title.draw_text()
    start.draw_button(mouse_pos)

    # Draw additional menu buttons on screen.
    for button in menu_buttons:
        button.draw_button(mouse_pos)


def show_character_menu(screen, gui_elements, mouse_pos):
    """Display character menu."""
    # Assign gui_elements to variables.
    custom = gui_elements["custom"]
    random = gui_elements["random"]
    back_button = gui_elements["back_button"]

    # Position buttons.
    ui.position_character_menu_screen_elements(screen, gui_elements)

    # Draw elements on screen.
    custom.draw_button(mouse_pos)
    random.draw_button(mouse_pos)
    back_button.draw_button(mouse_pos)


def show_ability_scores_screen(screen, character, gui_elements, mouse_pos):
    """Display ability scores from 'Character' class instance 'character' and bonus/penalty on screen.
    Screen layout is designed to adapt and fit up to 16 abilities."""
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = gui_elements["abilities_title"]
    reroll_button = gui_elements["reroll_button"]
    back_button = gui_elements["back_button"]
    continue_button = gui_elements["continue_button"]

    # Array of ability fields. Each item is a tuple with the GUI element at index 0 and the corresponding attribute from
    # character object at index 1. 'character.abilities[]' stores values in a dict as lists with base score at index 0
    # and bonus/penalty at index 1.
    abilities_array = (
        (gui_elements["strength"], character.abilities["str"]),
        (gui_elements["dexterity"], character.abilities["dex"]),
        (gui_elements["constitution"], character.abilities["con"]),
        (gui_elements["intelligence"], character.abilities["int"]),
        (gui_elements["wisdom"], character.abilities["wis"]),
        (gui_elements["charisma"], character.abilities["cha"]),
    )

    # Position and draw each ability pair from 'abilities_array' on screen.
    ui.position_ability_scores_screen_elements(screen, abilities_array, mouse_pos)

    # Draw title and buttons on screen.
    ui.draw_screen_title(screen, screen_title, gui_elements)
    ui.draw_special_button(screen, reroll_button, gui_elements, mouse_pos)
    back_button.draw_button(mouse_pos)
    continue_button.draw_button(mouse_pos)


def show_race_class_selection_screen(screen, rc_dict, possible_characters, selected_race, selected_class, gui_elements, mouse_pos):
    """Display race/class selection on screen.
    Screen layout is designed to adapt and fit up to 16 races/classes.
    ARGS:
        screen: PyGame window.
        rc_dict: dict containing all available races/classes in the game as lists of strings.
        possible_characters: list of possible race-class combinations as strings.
        selected_race: instance of 'InteractiveText' class representing chosen race.
        selected_class: instance of 'InteractiveText' class representing chosen class.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        selected_race
        selected_class
    """
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = gui_elements["race_class_title"]
    reset_button = gui_elements["reset_button"]
    back_button = gui_elements["back_button"]
    active_races = gui_elements["active_races"]
    active_classes = gui_elements["active_classes"]
    inactive_races = gui_elements["inactive_races"]
    inactive_classes = gui_elements["inactive_classes"]

    # Draw screen title.
    ui.draw_screen_title(screen, screen_title, gui_elements)

    # Get dict of race and class interactive text field instances 'available_choices', which are then ready to be drawn
    # on screen.
    available_choices = ui.get_available_choices(possible_characters, active_races, active_classes, selected_race,
                                                selected_class)

    # Position and draw instances from dict 'available_choices' on screen.
    ui.draw_available_choices(screen, rc_dict, available_choices, inactive_races, inactive_classes, mouse_pos)

    # Select race and class.
    selected_race, selected_class = ui.select_race_class(available_choices, selected_race, selected_class, reset_button, mouse_pos)

    # Draw buttons.
    ui.draw_special_button(screen, reset_button, gui_elements, mouse_pos)
    back_button.draw_button(mouse_pos)
    # Show continue button only if race AND class have been selected otherwise show inactive continue button.
    ui.draw_continue_button_inactive(selected_race, selected_class, gui_elements, mouse_pos, check_mode="all")

    return selected_race, selected_class


def show_naming_screen(screen, character, gui_elements, mouse_pos):
    """Display character naming screen and prompt user for input."""
    # Assign fields and buttons from 'gui_elements' to variables.
    naming_prompt = gui_elements["naming_prompt"]
    back_button = gui_elements["back_button"]
    continue_button = gui_elements["continue_button"]
    character_name_field = gui_elements["character_name_input"][1]

    # Create text attribute for naming prompt object to include chosen race and class, and position it on screen.
    ui.build_and_position_prompt(screen, naming_prompt, character)
    # Draw naming prompt.
    naming_prompt.draw_text()

    # Draw text input field with white background rect.
    character_name_field.draw_input_field()

    # Draw buttons on screen.
    back_button.draw_button(mouse_pos)
    continue_button.draw_button(mouse_pos)


def show_starting_money_screen(screen, gui_elements, random_money_flag, custom_money_flag, starting_money, mouse_pos):
    """Display money input screen and prompt user to choose random or custom amount of money.
    ARGS:
        screen: PyGame window.
        gui_elements: dict of gui elements as created in module 'gui_elements.py'.
        random_money_flag: boolean from 'state_manager.py' to reflect user choice.
        custom_money_flag: boolean from 'state_manager.py' to reflect user choice.
        starting_money: int amount of starting money.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    RETURNS:
        random_money_flag
        custom_money_flag
        starting_money
    """
    # Assign text fields and buttons from 'gui_elements' to variables.
    screen_title = gui_elements["starting_money_title"]
    back_button = gui_elements["back_button"]
    choices = gui_elements["starting_money_choices"]

    # Get positions for screen elements.
    ui.position_money_screen_elements(screen, gui_elements)

    # Draw screen title.
    ui.draw_screen_title(screen, screen_title, gui_elements)

    # Draw choices on screen.
    for choice in choices:
        choice.draw_button(mouse_pos)

    # Choose option to either generate random amount of money or let user input a custom amount.
    # Set 'random_money_flag' and 'custom_money_flag' accordingly.
    random_money_flag, custom_money_flag = ui.choose_money_option(choices, random_money_flag, custom_money_flag, mouse_pos)

    # Set and draw message for random amount of starting money or show input field for custom amount based on user choice above.
    starting_money = ui.draw_chosen_money_option(screen, starting_money, random_money_flag, custom_money_flag, gui_elements)

    # Draw buttons on screen.
    back_button.draw_button(mouse_pos)
    # Show continue button only if a money option has been selected otherwise show inactive continue button.
    ui.draw_continue_button_inactive(random_money_flag, custom_money_flag, gui_elements, mouse_pos)

    return random_money_flag, custom_money_flag, starting_money


def show_character_complete_screen(screen, gui_elements, mouse_pos):
    """Show message confirming completion of basic character creation and let user proceed to character sheet."""
    # Assign text field and button from 'gui_elements' to variables.
    completion_message = gui_elements["completion_message"]
    show_character_sheet = gui_elements["show_character_sheet"]

    # Position screen elements.
    ui.position_completion_screen_elements(screen, completion_message, show_character_sheet, gui_elements)

    # Draw screen elements on screen.
    completion_message.draw_text()
    show_character_sheet.draw_button(mouse_pos)
