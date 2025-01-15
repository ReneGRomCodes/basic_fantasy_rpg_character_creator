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
    # Basic character info.
    name, xp, race, cls, level, next_level_xp = (cs_elements["name"], cs_elements["xp"], cs_elements["race"],
                                                 cs_elements["class"], cs_elements["level"], cs_elements["next_level_xp"])
    # Ability scores.
    abilities = cs_elements["abilities"]
    # Combat stats.
    armor_class, health_points, attack_bonus = (cs_elements["armor_class"], cs_elements["health_points"],
                                                cs_elements["attack_bonus"])

    return (screen_rect, title_spacing, spacing_screen_edge, title, name, xp, race, cls, level, next_level_xp, abilities,
            armor_class, health_points, attack_bonus)


def position_cs_elements(screen, cs_elements, gui_elements):
    (screen_rect, title_spacing, spacing_screen_edge, title, name, xp, race, cls, level, next_level_xp, abilities,
     armor_class, health_points, attack_bonus)\
        = get_element_variables(screen, cs_elements, gui_elements)

    name.text_rect.top, name.text_rect.left = title.text_rect.bottom + title_spacing, screen_rect.left + spacing_screen_edge


def show_character_sheet_screen(screen, cs_elements, gui_elements):
    (screen_rect, title_spacing, spacing_screen_edge, title, name, xp, race, cls, level, next_level_xp, abilities,
     armor_class, health_points, attack_bonus)\
        = get_element_variables(screen, cs_elements, gui_elements)

    position_cs_elements(screen, cs_elements, gui_elements)

    ui.draw_screen_title(screen, title, gui_elements)
    name.draw_text()
