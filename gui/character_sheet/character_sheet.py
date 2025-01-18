import gui.ui_helpers as ui
"""Module containing functions for character sheet output on screen."""


def show_character_sheet_screen(screen, cs_sheet, gui_elements):
    # Draw screen title.
    ui.draw_screen_title(screen, cs_sheet.title, gui_elements)

    cs_sheet.position_cs_elements()

    # Draw character sheet elements on screen.
    # Basic character info fields.
    cs_sheet.name_field.draw_text()
    cs_sheet.name_char.draw_text()
    cs_sheet.xp_field.draw_text()
    cs_sheet.xp_char.draw_text()
    cs_sheet.race_field.draw_text()
    cs_sheet.race_char.draw_text()
    cs_sheet.class_field.draw_text()
    cs_sheet.class_char.draw_text()
    cs_sheet.level_field.draw_text()
    cs_sheet.level_char.draw_text()
    cs_sheet.next_lvl_xp_field.draw_text()
    cs_sheet.next_lvl_xp_char.draw_text()
