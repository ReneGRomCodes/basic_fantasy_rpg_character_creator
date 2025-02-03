import gui.screen_objects as so
import gui.ui_helpers as ui

"""Screen functions."""


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
    settings = gui_elements["settings_button"]
    show_credits = gui_elements["credits_button"]

    # Position buttons and main menu title field.
    ui.position_main_menu_screen_elements(screen, gui_elements)

    # Draw elements on screen.
    title.draw_text()
    start.draw_button(mouse_pos)
    settings.draw_button(mouse_pos)
    show_credits.draw_button(mouse_pos)


def show_settings(screen, gui_elements, selected_window_size, mouse_pos):
    """Display settings screen."""
    # Assign gui_elements to variables.
    title = gui_elements["settings_title"]
    window_size_field = gui_elements["window_size"]
    window_size_buttons = gui_elements["window_size_buttons"]
    back_button = gui_elements["back_button"]

    # Format elements on screen.
    ui.format_settings_screen_elements(screen, gui_elements)

    # Select window size.
    selected_window_size = ui.select_window_size(window_size_buttons, selected_window_size, mouse_pos)

    # Draw basic elements on screen.
    ui.draw_screen_title(screen, title, gui_elements)
    back_button.draw_button(mouse_pos)
    # Draw window size selection on screen.
    window_size_field.draw_text()
    for button in window_size_buttons:
        button.draw_interactive_text(mouse_pos)

    return selected_window_size


def show_credits_screen(screen, gui_elements):
    """Display credits screen."""
    # Assign gui_elements to variables.
    title = gui_elements["credits_title"]

    # Draw elements on screen.
    ui.draw_screen_title(screen, title, gui_elements)


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
    """Display character ability scores and bonus/penalty on screen."""
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = gui_elements["abilities_title"]
    reroll_button = gui_elements["reroll_button"]
    back_button = gui_elements["back_button"]
    continue_button = gui_elements["continue_button"]

    # Assign further gui_elements to variables and add them to list 'abilities'.
    strength = gui_elements["strength"]
    dexterity = gui_elements["dexterity"]
    constitution = gui_elements["constitution"]
    intelligence = gui_elements["intelligence"]
    wisdom = gui_elements["wisdom"]
    charisma = gui_elements["charisma"]
    abilities = (strength, dexterity, constitution, intelligence, wisdom, charisma)
    # Assign dict 'character.abilities' to 'stats' to avoid confusion with tuple 'abilities' above.
    stats = character.abilities
    # Create instances of class 'TextField' to show ability scores on screen. Text size is taken from an instance in
    # 'gui_elements' to assure automatic scaling.
    ability_score_text = so.TextField(screen, "score", strength.size)
    bonus_penalty_text = so.TextField(screen, "bonus_penalty", strength.size)

    # Draw screen title.
    ui.draw_screen_title(screen, screen_title, gui_elements)

    # Set initial position on y-axis for ability score fields.
    element_pos_y = screen.get_rect().height / 4

    # Loop through each ability field and corresponding stat to format and display the ability name, score and bonus/penalty.
    # Align and position elements dynamically on the screen.
    for ability, key in zip(abilities, stats):
        # 'Pre-formatting' bonus/penalty to string for easier formatting and better code-readability further down.
        bonus_penalty = f"{stats[key][1]}"

        # Check bonus/penalty for positive or negative value to apply correct prefix in text field or give out an empty
        # string if bonus_penalty is 0.
        if stats[key][1] > 0:
            bonus_penalty = f"+{bonus_penalty}"
        elif stats[key][1] == 0:
            bonus_penalty = ""

        # Position and draw copied rect for item from list 'abilities'.
        ability_rect = ability.interactive_rect.copy()
        ability_rect.top = screen.get_rect().top + element_pos_y
        ability_rect.width = screen.get_rect().width / 6
        ability_rect.right = screen.get_rect().centerx
        # Position ability rect within copied rect for left-alignment.
        ability.interactive_rect.topleft = ability_rect.topleft
        ability.draw_interactive_text(mouse_pos)

        # Change contents and get rect of 'TextField' instances for each ability score stat.
        ability_score_text.text = str(stats[key][0])
        ui.render_new_text_image(ability_score_text)
        bonus_penalty_text.text = bonus_penalty
        ui.render_new_text_image(bonus_penalty_text)

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

        element_pos_y += ability_score_text.text_rect.height * 2

    # Draw buttons on screen.
    ui.draw_special_button(screen, reroll_button, gui_elements, mouse_pos)
    back_button.draw_button(mouse_pos)
    continue_button.draw_button(mouse_pos)


def show_race_class_selection_screen(screen, possible_characters, selected_race, selected_class, gui_elements, mouse_pos):
    """Display race/class selection on screen."""
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = gui_elements["race_class_title"]
    reset_button = gui_elements["reset_button"]
    back_button = gui_elements["back_button"]
    possible_races = gui_elements["possible_races"]
    possible_classes = gui_elements["possible_classes"]
    inactive_races = gui_elements["inactive_races"]
    inactive_classes = gui_elements["inactive_classes"]

    # Draw screen title.
    ui.draw_screen_title(screen, screen_title, gui_elements)

    # Get dict of race and class interactive text field instances 'available_choices', which are then ready to be drawn
    # on screen.
    available_choices = ui.get_available_choices(possible_characters, possible_races, possible_classes, selected_race,
                                                selected_class)

    # Position and draw instances from dict 'available_choices' on screen.
    ui.draw_available_choices(screen, available_choices, inactive_races, inactive_classes, mouse_pos)

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
    """Display character naming screen and prompt user for input."""
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
    starting_money, random_money_flag, custom_money_flag = ui.choose_money_option(choices, starting_money, random_money_flag,
                                                                                  custom_money_flag, mouse_pos)

    # Draw message for random amount of starting money or show input field for custom amount based on user choice above.
    ui.draw_chosen_money_option(screen, starting_money, random_money_flag, custom_money_flag, gui_elements)

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
