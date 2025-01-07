import gui.ui_helpers as ui
"""Module containing function for character sheet output on screen."""


def show_character_sheet_screen(screen, cs_elements, gui_elements):
    screen_title = cs_elements["title"]

    ui.draw_screen_title(screen, screen_title, gui_elements)
