import gui.ui_helpers as ui
"""Module containing functions for character sheet output on screen."""


def get_element_variables(screen, cs_elements, gui_elements):
    """Assign values from dicts 'cs_elements' and 'gui_elements' to variables and return them to avoid assigning them
    repeatedly in multiple functions within this module."""

    # Assign screen variables.
    screen_rect = screen.get_rect()
    # Assign 'gui_elements' variables.
    title_spacing = gui_elements["menu_title_spacing"]
    spacing_screen_edge = gui_elements["default_edge_spacing"]
    # Assign 'cs_elements' variables.
    title = cs_elements["title"]
    name = cs_elements["name"]

    return screen_rect, title_spacing, spacing_screen_edge, title, name


def position_cs_elements(screen, cs_elements, gui_elements):
    screen_rect, title_spacing, spacing_screen_edge, title, name = get_element_variables(screen, cs_elements, gui_elements)

    name.text_rect.top, name.text_rect.left = title.text_rect.bottom + title_spacing, screen_rect.left + spacing_screen_edge


def show_character_sheet_screen(screen, cs_elements, gui_elements):
    screen_rect, title_spacing, spacing_screen_edge, title, name = get_element_variables(screen, cs_elements, gui_elements)

    position_cs_elements(screen, cs_elements, gui_elements)

    ui.draw_screen_title(screen, title, gui_elements)
    name.draw_text()
