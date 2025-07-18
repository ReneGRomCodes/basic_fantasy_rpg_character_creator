"""
Main GUI functions.
"""
from core.shared_data import shared_data as sd

import gui.ui_helpers as ui
from .shared_data import ui_shared_data as uisd


def show_title_screen(screen) -> None:
    """Show title screen.
    ARGS:
        screen: PyGame window.
    """
    # Assign ui_registry to variables.
    title = uisd.ui_registry["title_screen_fields"][0]
    subtitle = uisd.ui_registry["title_screen_fields"][1]
    copyright_notice = uisd.ui_registry["title_screen_fields"][2]
    progress_bar = uisd.ui_registry["title_screen_fields"][3]
    continue_to_main = uisd.ui_registry["title_screen_fields"][4]

    # Position title, subtitle and copyright notice.
    ui.position_title_screen_elements(screen)

    # Draw elements on screen.
    title.draw_text()
    subtitle.draw_text()
    copyright_notice.draw_text()
    progress_bar.draw_progress_bar()
    # Draw continue message once loading progress bar is finished.
    if progress_bar.finished:
        continue_to_main.draw_text()


def show_main_menu(screen, mouse_pos) -> None:
    """Display main menu.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    # Assign ui_registry to variables.
    title = uisd.ui_registry["main_menu_title"]
    start = uisd.ui_registry["start_button"]
    menu_buttons = uisd.ui_registry["menu_buttons"]

    # Position buttons and main menu title field.
    ui.position_main_menu_screen_elements(screen)

    # Draw elements on screen.
    title.draw_text()
    start.draw_button(mouse_pos)

    # Draw additional menu buttons on screen.
    for button in menu_buttons:
        button.draw_button(mouse_pos)


def show_character_menu(screen, mouse_pos) -> None:
    """Display character menu.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    # Assign ui_registry to variables.
    custom = uisd.ui_registry["custom"]
    random = uisd.ui_registry["random"]
    back_button = uisd.ui_registry["back_button"]

    # Position buttons.
    ui.position_character_menu_screen_elements(screen)

    # Draw elements on screen.
    custom.draw_button(mouse_pos)
    random.draw_button(mouse_pos)
    back_button.draw_button(mouse_pos)


def show_ability_scores_screen(screen, mouse_pos) -> None:
    """Display ability scores from 'Character' class instance 'character' and bonus/penalty on screen.
    Screen layout is designed to adapt and fit up to 16 abilities.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    # Assign fields and buttons from 'ui_registry' to variables.
    screen_title = uisd.ui_registry["abilities_title"]
    reroll_button = uisd.ui_registry["reroll_button"]
    back_button = uisd.ui_registry["back_button"]
    continue_button = uisd.ui_registry["continue_button"]
    ability_fields = uisd.ui_registry["ability_fields"]

    # Array of ability fields. Each item is a tuple with the GUI element at index 0 and the corresponding attribute from
    # character object at index 1. 'character.abilities[]' stores values in a dict as lists with base score at index 0
    # and bonus/penalty at index 1.
    abilities_array: tuple[tuple[object, list[int]], ...] = (
        (ability_fields[0], sd.character.abilities["str"]),  # Strength
        (ability_fields[1], sd.character.abilities["dex"]),  # Dexterity
        (ability_fields[2], sd.character.abilities["con"]),  # Constitution
        (ability_fields[3], sd.character.abilities["int"]),  # Intelligence
        (ability_fields[4], sd.character.abilities["wis"]),  # Wisdom
        (ability_fields[5], sd.character.abilities["cha"]),  # Charisma
    )

    # Position and draw each ability pair from 'abilities_array' on screen.
    ui.position_ability_scores_screen_elements(screen, abilities_array, mouse_pos)

    # Draw title and buttons on screen.
    ui.draw_screen_title(screen, screen_title)
    ui.draw_special_button(screen, reroll_button, mouse_pos)
    back_button.draw_button(mouse_pos)
    continue_button.draw_button(mouse_pos)

    # Call helper function to properly handle info panels (see function and class docstrings for details).
    ui.show_info_panels(ability_fields, mouse_pos)


def show_race_class_selection_screen(screen, mouse_pos) -> None:
    """Display race/class selection on screen.
    Screen layout is designed to adapt and fit up to 16 races/classes.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    # Assign fields and buttons from 'ui_registry' to variables.
    screen_title = uisd.ui_registry["race_class_title"]
    reset_button = uisd.ui_registry["reset_button"]
    back_button = uisd.ui_registry["back_button"]
    active_races = uisd.ui_registry["active_races"]
    active_classes = uisd.ui_registry["active_classes"]
    inactive_races = uisd.ui_registry["inactive_races"]
    inactive_classes = uisd.ui_registry["inactive_classes"]

    # Draw screen title.
    ui.draw_screen_title(screen, screen_title)

    # Position and draw race/class selection elements on screen.
    ui.draw_race_class_selection_elements(screen, active_races, active_classes, inactive_races, inactive_classes, mouse_pos)

    # Draw buttons.
    ui.draw_special_button(screen, reset_button, mouse_pos)
    back_button.draw_button(mouse_pos)
    # Show continue button only if race AND class have been selected otherwise show inactive continue button.
    ui.draw_conditional_continue_button(mouse_pos, sd.selected_race, sd.selected_class, check_mode="all")

    # Call helper function to properly handle info panels (see function and class docstrings for details).
    ui.show_info_panels(active_races, mouse_pos)
    ui.show_info_panels(active_classes, mouse_pos)


def show_spell_selection_screen(screen, mouse_pos) -> None:
    """Display spell selection screen.
        ARGS:
            screen: PyGame window.
            mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    # Assign fields and buttons from 'ui_registry' to variables.
    screen_title = uisd.ui_registry["spell_title"]
    screen_note = uisd.ui_registry["spell_note"]
    back_button = uisd.ui_registry["back_button"]
    spells = uisd.ui_registry["spell_fields"]

    # Draw screen title and buttons.
    ui.draw_screen_title(screen, screen_title)
    back_button.draw_button(mouse_pos)
    # Show continue button only if spell selection has been made, display skip button otherwise.
    ui.draw_conditional_continue_button(mouse_pos, sd.selected_spell, alt_button="skip")

    # Position and draw spell selection elements on screen.
    ui.draw_spell_selection_screen_elements(screen, spells, screen_note, mouse_pos)

    # Call helper function to properly handle info panels (see function and class docstrings for details).
    ui.show_info_panels(spells, mouse_pos)


def show_language_selection_screen(screen, mouse_pos) -> None:
    """Display language selection screen.
            ARGS:
                screen: PyGame window.
                mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    # Assign fields and buttons from 'ui_registry' to variables.
    screen_title = uisd.ui_registry["lang_title"]
    screen_note = uisd.ui_registry["lang_note"]
    reset_button = uisd.ui_registry["reset_button"]
    back_button = uisd.ui_registry["back_button"]
    languages = uisd.ui_registry["lang_fields"]
    inactive_languages = uisd.ui_registry["inactive_language_fields"]

    # Draw screen title and buttons.
    ui.draw_screen_title(screen, screen_title)
    back_button.draw_button(mouse_pos)
    ui.draw_special_button(screen, reset_button, mouse_pos)
    # Show continue button only if language selection has been made, display skip button otherwise.
    ui.draw_conditional_continue_button(mouse_pos, sd.selected_languages, alt_button="skip")

    # Position and draw language selection elements on screen.
    ui.draw_language_selection_screen_elements(screen, languages, inactive_languages, screen_note, mouse_pos)


def show_naming_screen(screen, mouse_pos) -> None:
    """Display character naming screen and prompt user for input.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    # Assign fields and buttons from 'ui_registry' to variables.
    naming_prompt = uisd.ui_registry["naming_prompt"]
    back_button = uisd.ui_registry["back_button"]
    character_name = uisd.ui_registry["character_name_input"][0].manager.value
    character_name_field = uisd.ui_registry["character_name_input"][1]

    # Create text attribute for naming prompt object to include chosen race and class, and position it on screen.
    ui.build_and_position_prompt(screen, naming_prompt)
    # Draw naming prompt.
    naming_prompt.draw_text()

    # Draw text input field with white background rect.
    character_name_field.draw_input_field()

    # Draw buttons on screen.
    back_button.draw_button(mouse_pos)
    # Show continue button only if language selection has been made, display skip button otherwise.
    ui.draw_conditional_continue_button(mouse_pos, character_name, alt_button="skip")


def show_starting_money_screen(screen, mouse_pos) -> None:
    """Display money input screen and prompt user to choose random or custom amount of money.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    # Assign text fields and buttons from 'ui_registry' to variables.
    screen_title = uisd.ui_registry["starting_money_title"]
    back_button = uisd.ui_registry["back_button"]
    choices = uisd.ui_registry["starting_money_choices"]

    # Get positions for screen elements.
    ui.position_money_screen_elements(screen)

    # Draw screen title.
    ui.draw_screen_title(screen, screen_title)

    # Draw choices on screen.
    for choice in choices:
        choice.draw_button(mouse_pos)

    # Choose option to either generate random amount of money or let user input a custom amount.
    # Set 'random_money_flag' and 'custom_money_flag' accordingly.
    ui.choose_money_option(choices, mouse_pos)

    # Set and draw message for random amount of starting money or show input field for custom amount based on user choice above.
    ui.draw_chosen_money_option(screen)

    # Draw buttons on screen.
    back_button.draw_button(mouse_pos)
    # Show continue button only if a money option has been selected otherwise show inactive continue button.
    ui.draw_conditional_continue_button(mouse_pos, uisd.dice_roll_complete, sd.custom_money_flag)


def show_character_complete_screen(screen, mouse_pos) -> None:
    """Show message confirming completion of basic character creation and let user proceed to character sheet.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    # Assign text field and button from 'ui_registry' to variables.
    completion_message = uisd.ui_registry["completion_message"]
    show_character_sheet = uisd.ui_registry["show_character_sheet"]

    # Position screen elements.
    ui.position_completion_screen_elements(screen, completion_message, show_character_sheet)

    # Draw screen elements on screen.
    completion_message.draw_text()
    show_character_sheet.draw_button(mouse_pos)
