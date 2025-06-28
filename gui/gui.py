import gui.ui_helpers as ui
from core.shared_data import shared_data as sd
from gui.shared_data import ui_shared_data as uisd

"""Main GUI functions."""


def show_title_screen(screen) -> None:
    """Show title screen.
    ARGS:
        screen: PyGame window.
    """
    # Assign gui_elements to variables.
    title = uisd.gui_elements["title_screen_fields"][0]
    subtitle = uisd.gui_elements["title_screen_fields"][1]
    copyright_notice = uisd.gui_elements["title_screen_fields"][2]
    progress_bar = uisd.gui_elements["title_screen_fields"][3]
    continue_to_main = uisd.gui_elements["title_screen_fields"][4]

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
    # Assign gui_elements to variables.
    title = uisd.gui_elements["main_menu_title"]
    start = uisd.gui_elements["start_button"]
    menu_buttons = uisd.gui_elements["menu_buttons"]

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
    # Assign gui_elements to variables.
    custom = uisd.gui_elements["custom"]
    random = uisd.gui_elements["random"]
    back_button = uisd.gui_elements["back_button"]

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
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = uisd.gui_elements["abilities_title"]
    reroll_button = uisd.gui_elements["reroll_button"]
    back_button = uisd.gui_elements["back_button"]
    continue_button = uisd.gui_elements["continue_button"]
    ability_fields = uisd.gui_elements["ability_fields"]

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
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = uisd.gui_elements["race_class_title"]
    reset_button = uisd.gui_elements["reset_button"]
    back_button = uisd.gui_elements["back_button"]
    active_races = uisd.gui_elements["active_races"]
    active_classes = uisd.gui_elements["active_classes"]
    inactive_races = uisd.gui_elements["inactive_races"]
    inactive_classes = uisd.gui_elements["inactive_classes"]

    # Draw screen title.
    ui.draw_screen_title(screen, screen_title)

    # Get dict of race and class interactive text field instances 'available_choices', which are then ready to be drawn
    # on screen.
    available_choices = ui.get_available_choices(active_races, active_classes)

    # Position and draw instances from dict 'available_choices' on screen.
    ui.draw_available_choices(screen, available_choices, inactive_races, inactive_classes, mouse_pos)

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
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = uisd.gui_elements["spell_title"]
    screen_note = uisd.gui_elements["spell_note"]
    back_button = uisd.gui_elements["back_button"]
    spells = uisd.gui_elements["spell_fields"]

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
    # Assign fields and buttons from 'gui_elements' to variables.
    screen_title = uisd.gui_elements["lang_title"]
    screen_note = uisd.gui_elements["lang_note"]
    back_button = uisd.gui_elements["back_button"]
    languages = uisd.gui_elements["lang_fields"]
    inactive_languages = uisd.gui_elements["inactive_language_fields"]

    # Draw screen title and buttons.
    ui.draw_screen_title(screen, screen_title)
    back_button.draw_button(mouse_pos)
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
    # Assign fields and buttons from 'gui_elements' to variables.
    naming_prompt = uisd.gui_elements["naming_prompt"]
    back_button = uisd.gui_elements["back_button"]
    character_name = uisd.gui_elements["character_name_input"][0].manager.value
    character_name_field = uisd.gui_elements["character_name_input"][1]

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
    # Assign text fields and buttons from 'gui_elements' to variables.
    screen_title = uisd.gui_elements["starting_money_title"]
    back_button = uisd.gui_elements["back_button"]
    choices = uisd.gui_elements["starting_money_choices"]

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
    # Assign text field and button from 'gui_elements' to variables.
    completion_message = uisd.gui_elements["completion_message"]
    show_character_sheet = uisd.gui_elements["show_character_sheet"]

    # Position screen elements.
    ui.position_completion_screen_elements(screen, completion_message, show_character_sheet)

    # Draw screen elements on screen.
    completion_message.draw_text()
    show_character_sheet.draw_button(mouse_pos)
