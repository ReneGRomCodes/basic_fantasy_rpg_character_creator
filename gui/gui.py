"""
Main GUI functions.
"""
from core.shared_data import shared_data as sd
from core.rules import ABILITIES

import gui.ui_helpers as ui
from .shared_data import ui_shared_data as uisd


def show_title_screen(screen) -> None:
    """Show title screen.
    ARGS:
        screen: PyGame window.
    """
    title = uisd.ui_registry["title_screen_fields"][0]
    subtitle = uisd.ui_registry["title_screen_fields"][1]
    copyright_notice = uisd.ui_registry["title_screen_fields"][2]
    progress_bar = uisd.ui_registry["title_screen_fields"][3]
    continue_to_main = uisd.ui_registry["title_screen_fields"][4]

    ui.position_title_screen_elements(screen)

    ui.draw_single_element_background_image(screen, title, "ornate_wood")
    ui.draw_single_element_background_image(screen, subtitle, "wood")
    ui.draw_single_element_background_image(screen, copyright_notice, "ornate_wood")
    title.draw_text()
    subtitle.draw_text()
    copyright_notice.draw_text()
    progress_bar.draw_progress_bar()

    if progress_bar.finished:
        ui.draw_single_element_background_image(screen, continue_to_main, "wood")
        continue_to_main.draw_text()


def show_main_menu(screen, mouse_pos) -> None:
    """Display main menu.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    title = uisd.ui_registry["main_menu_title"]
    start = uisd.ui_registry["start_button"]
    menu_buttons = uisd.ui_registry["menu_buttons"]

    ui.position_main_menu_screen_elements(screen)

    ui.draw_single_element_background_image(screen, title, "ornate_wood")
    title.draw_text()
    uisd.ui_registry["program_version"].draw_text()

    ui.draw_single_element_background_image(screen, start, "wood")
    start.draw_button(mouse_pos)

    for button in menu_buttons:
        ui.draw_single_element_background_image(screen, button, "wood")
        button.draw_button(mouse_pos)


def show_character_menu(screen, mouse_pos) -> None:
    """Display character menu.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    custom = uisd.ui_registry["custom"]
    random = uisd.ui_registry["random"]
    back_button = uisd.ui_registry["back_button"]

    ui.position_character_menu_screen_elements(screen)

    ui.draw_single_element_background_image(screen, custom, "wood")
    ui.draw_single_element_background_image(screen, random, "wood")
    ui.draw_single_element_background_image(screen, back_button, "wood")
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
    screen_title = uisd.ui_registry["abilities_title"]
    reroll_button = uisd.ui_registry["reroll_button"]
    back_button = uisd.ui_registry["back_button"]
    continue_button = uisd.ui_registry["continue_button"]
    ability_fields = uisd.ui_registry["ability_fields"]

    # Array of ability fields. Each item is a tuple with the GUI element at index 0 and the corresponding attribute from
    # character object at index 1.
    abilities_array: tuple[tuple[object, list[int]], ...] = (
        (ability_fields[0], sd.character.abilities[ABILITIES[0]]),  # Strength
        (ability_fields[1], sd.character.abilities[ABILITIES[1]]),  # Dexterity
        (ability_fields[2], sd.character.abilities[ABILITIES[2]]),  # Constitution
        (ability_fields[3], sd.character.abilities[ABILITIES[3]]),  # Intelligence
        (ability_fields[4], sd.character.abilities[ABILITIES[4]]),  # Wisdom
        (ability_fields[5], sd.character.abilities[ABILITIES[5]]),  # Charisma
    )

    ui.draw_ability_scores_screen_elements(screen, abilities_array, mouse_pos)
    ui.draw_screen_title(screen, screen_title)

    ui.draw_single_element_background_image(screen, back_button, "wood")
    ui.draw_single_element_background_image(screen, continue_button, "wood")
    ui.draw_special_button(screen, reroll_button, mouse_pos)
    back_button.draw_button(mouse_pos)
    continue_button.draw_button(mouse_pos)

    ui.show_info_panels(ability_fields, mouse_pos)


def show_race_class_selection_screen(screen, mouse_pos) -> None:
    """Display race/class selection on screen.
    Screen layout is designed to adapt and fit up to 16 races/classes.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    screen_title = uisd.ui_registry["race_class_title"]
    reset_button = uisd.ui_registry["reset_button"]
    back_button = uisd.ui_registry["back_button"]
    active_races = uisd.ui_registry["active_races"]
    active_classes = uisd.ui_registry["active_classes"]
    inactive_races = uisd.ui_registry["inactive_races"]
    inactive_classes = uisd.ui_registry["inactive_classes"]

    ui.draw_screen_title(screen, screen_title)
    ui.draw_race_class_selection_elements(screen, active_races, active_classes, inactive_races, inactive_classes, mouse_pos)

    ui.draw_special_button(screen, reset_button, mouse_pos)
    ui.draw_single_element_background_image(screen, back_button, "wood")
    back_button.draw_button(mouse_pos)
    # Show continue button only if race AND class have been selected otherwise show inactive continue button.
    ui.draw_conditional_continue_button(screen, mouse_pos, sd.selected_race, sd.selected_class, check_mode="all")

    ui.show_info_panels(active_races, mouse_pos)
    ui.show_info_panels(active_classes, mouse_pos)


def show_spell_selection_screen(screen, mouse_pos) -> None:
    """Display spell selection screen.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    screen_title = uisd.ui_registry["spell_title"]
    screen_note = uisd.ui_registry["spell_note"]
    back_button = uisd.ui_registry["back_button"]
    spells = uisd.ui_registry["spell_fields"]

    ui.draw_screen_title(screen, screen_title)

    ui.draw_single_element_background_image(screen, back_button, "wood")
    back_button.draw_button(mouse_pos)
    # Show continue button only if spell selection has been made, display skip button otherwise.
    ui.draw_conditional_continue_button(screen, mouse_pos, sd.selected_spell, alt_button="skip")

    ui.draw_spell_selection_screen_elements(screen, spells, screen_note, mouse_pos)

    ui.show_info_panels(spells, mouse_pos)


def show_language_selection_screen(screen, mouse_pos) -> None:
    """Display language selection screen.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    screen_title = uisd.ui_registry["lang_title"]
    screen_note = uisd.ui_registry["lang_note"]
    reset_button = uisd.ui_registry["reset_button"]
    back_button = uisd.ui_registry["back_button"]
    languages = uisd.ui_registry["lang_fields"]
    inactive_languages = uisd.ui_registry["inactive_language_fields"]

    ui.draw_screen_title(screen, screen_title)

    ui.draw_single_element_background_image(screen, back_button, "wood")
    back_button.draw_button(mouse_pos)
    ui.draw_special_button(screen, reset_button, mouse_pos)
    # Show continue button only if language selection has been made, display skip button otherwise.
    ui.draw_conditional_continue_button(screen, mouse_pos, sd.selected_languages, alt_button="skip")

    ui.draw_language_selection_screen_elements(screen, languages, inactive_languages, screen_note, mouse_pos)


def show_naming_screen(screen, mouse_pos) -> None:
    """Display character naming screen and prompt user for input.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    naming_prompt = uisd.ui_registry["naming_prompt"]
    back_button = uisd.ui_registry["back_button"]
    character_name = uisd.ui_registry["character_name_input"][0].manager.value
    character_name_field = uisd.ui_registry["character_name_input"][1]

    ui.build_and_position_prompt(screen, naming_prompt)
    ui.draw_single_element_background_image(screen, naming_prompt, "ornate_wood")
    naming_prompt.draw_text()

    character_name_field.draw_input_field()

    ui.draw_single_element_background_image(screen, back_button, "wood")
    back_button.draw_button(mouse_pos)
    # Show continue button only if language selection has been made, display skip button otherwise.
    ui.draw_conditional_continue_button(screen, mouse_pos, character_name, alt_button="skip")


def show_starting_money_screen(screen, mouse_pos) -> None:
    """Display money input screen and prompt user to choose random or custom amount of money.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    screen_title = uisd.ui_registry["starting_money_title"]
    back_button = uisd.ui_registry["back_button"]
    choices = uisd.ui_registry["starting_money_choices"]

    ui.position_money_screen_elements(screen)
    ui.draw_screen_title(screen, screen_title)

    for choice in choices:
        ui.draw_single_element_background_image(screen, choice, "wood")
        choice.draw_button(mouse_pos)

    ui.choose_money_option(choices, mouse_pos)
    ui.draw_chosen_money_option(screen)

    ui.draw_single_element_background_image(screen, back_button, "wood")
    back_button.draw_button(mouse_pos)
    # Show continue button only if a money option has been selected otherwise show inactive continue button.
    ui.draw_conditional_continue_button(screen, mouse_pos, uisd.dice_roll_complete, sd.custom_money_flag)


def show_created_character_confirmation_screen(screen, mouse_pos) -> None:
    """Display confirmation screen. Giving user final chance to make changes or proceed to final character sheet creation.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    confirmation_message = uisd.ui_registry["confirm_character_message"]
    choices = uisd.ui_registry["confirm_character_buttons"]

    ui.position_confirm_created_character_elements(screen)

    ui.draw_single_element_background_image(screen, confirmation_message, "parchment", parchment=1)
    confirmation_message.draw_text()

    for choice in choices:
        ui.draw_single_element_background_image(screen, choice, "wood")
        choice.draw_button(mouse_pos)


def show_building_character_sheet_screen(screen) -> None:
    """Show screen with character sheet creation 'progress'.
    Honestly it's not much more than a ProgressBar instance that does absolutely nothing except looking busy...
    seriously! There is no actual process running in the background. But that's the spot in the program where the user
    should get the impression that something is processed, so like in any office job: look busy when the boss is
    watching ;)
    ARGS:
        screen: PyGame window.
    """
    progress_bar = uisd.ui_registry["creation_progress_bar"]

    ui.position_character_sheet_creation_screen(screen)
    progress_bar.draw_progress_bar()


def show_character_complete_screen(screen, mouse_pos) -> None:
    """Show message confirming completion of basic character creation and let user proceed to character sheet.
    ARGS:
        screen: PyGame window.
        mouse_pos: position of mouse on screen. Handed down by pygame from main loop.
    """
    completion_message = uisd.ui_registry["completion_message"]
    show_character_sheet = uisd.ui_registry["show_character_sheet"]

    ui.position_completion_screen_elements(screen, completion_message, show_character_sheet)

    ui.draw_single_element_background_image(screen, completion_message, "ornate_wood")
    ui.draw_single_element_background_image(screen, show_character_sheet, "wood")
    completion_message.draw_text()
    show_character_sheet.draw_button(mouse_pos)
