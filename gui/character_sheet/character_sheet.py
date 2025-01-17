import gui.ui_helpers as ui
"""Module containing functions for character sheet output on screen."""


def get_element_variables(screen, cs_elements, gui_elements):
    """Assign values from dicts 'cs_elements' and 'gui_elements' to variables and return them to avoid assigning them
    repeatedly in multiple functions within this module."""

    # Assign screen rect variable.
    screen_rect = screen.get_rect()
    screen_height, screen_width = screen_rect.height, screen_rect.width

    # Assign 'gui_elements' variables.
    title_spacing = gui_elements["menu_title_spacing"]
    spacing_screen_edge = gui_elements["default_edge_spacing"]

    # Assign 'cs_elements' variables.
    title = cs_elements["title"]
    # Basic character info.
    name_field, name_char = cs_elements["name"]
    xp_field, xp_char = cs_elements["xp"]
    level_field, level_char = cs_elements["level"]
    race_field, race_char = cs_elements["race"]
    class_field, class_char = cs_elements["class"]
    next_lvl_xp_field, next_lvl_xp_char = cs_elements["next_level_xp"]
    # Ability scores.
    abilities = cs_elements["abilities"]
    # Combat stats.
    armor_class, health_points, attack_bonus = (cs_elements["armor_class"], cs_elements["health_points"],
                                                cs_elements["attack_bonus"])

    return (screen_rect, screen_height, screen_width, title_spacing, spacing_screen_edge, title, name_field, name_char,
            xp_field, xp_char, race_field, race_char, class_field, class_char, level_field, level_char, next_lvl_xp_field,
            next_lvl_xp_char, abilities, armor_class, health_points, attack_bonus)


def position_cs_elements(screen, cs_elements, gui_elements):
    (screen_rect, screen_height, screen_width, title_spacing, spacing_screen_edge, title, name_field, name_char,
     xp_field, xp_char, race_field, race_char, class_field, class_char, level_field, level_char, next_lvl_xp_field,
     next_lvl_xp_char, abilities, armor_class, health_points, attack_bonus)\
        = get_element_variables(screen, cs_elements, gui_elements)

    # Positioning for basic character info fields. Primary 'anchor' object for positioning all elements is 'name_field'.
    name_field.text_rect.top, name_field.text_rect.left = title.text_rect.bottom + title_spacing, screen_rect.left + spacing_screen_edge
    name_char.text_rect.top, name_char.text_rect.left = name_field.text_rect.top, name_field.text_rect.right
    xp_field.text_rect.top, xp_field.text_rect.left = name_field.text_rect.top, screen_width * 0.75
    xp_char.text_rect.top, xp_char.text_rect.left = xp_field.text_rect.top, xp_field.text_rect.right
    race_field.text_rect.top, race_field.text_rect.left = name_field.text_rect.bottom, name_field.text_rect.left
    race_char.text_rect.top, race_char.text_rect.left = race_field.text_rect.top, race_field.text_rect.right
    class_field.text_rect.top, class_field.text_rect.left = race_char.text_rect.top, screen_width * 0.25
    class_char.text_rect.top, class_char.text_rect.left = class_field.text_rect.top, class_field.text_rect.right
    level_field.text_rect.top, level_field.text_rect.left = class_char.text_rect.top, screen_width * 0.5
    level_char.text_rect.top, level_char.text_rect.left = level_field.text_rect.top, level_field.text_rect.right
    next_lvl_xp_field.text_rect.top, next_lvl_xp_field.text_rect.left = level_char.text_rect.top, screen_width * 0.75
    next_lvl_xp_char.text_rect.top, next_lvl_xp_char.text_rect.left = next_lvl_xp_field.text_rect.top, next_lvl_xp_field.text_rect.right


def show_character_sheet_screen(screen, cs_elements, gui_elements):
    (screen_rect, screen_height, screen_width, title_spacing, spacing_screen_edge, title, name_field, name_char,
     xp_field, xp_char, race_field, race_char, class_field, class_char, level_field, level_char, next_lvl_xp_field,
     next_lvl_xp_char, abilities, armor_class, health_points, attack_bonus)\
        = get_element_variables(screen, cs_elements, gui_elements)

    position_cs_elements(screen, cs_elements, gui_elements)

    # Draw screen title.
    ui.draw_screen_title(screen, title, gui_elements)

    # Draw character sheet elements on screen.
    # Basic character info fields.
    name_field.draw_text()
    name_char.draw_text()
    xp_field.draw_text()
    xp_char.draw_text()
    race_field.draw_text()
    race_char.draw_text()
    class_field.draw_text()
    class_char.draw_text()
    level_field.draw_text()
    level_char.draw_text()
    next_lvl_xp_field.draw_text()
    next_lvl_xp_char.draw_text()
